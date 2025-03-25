#!/bin/bash

# Ensure required tools are installed
check_dependencies() {
    local deps=("kind" "kubectl" "docker")
    for cmd in "${deps[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            log_info "Error: $cmd is not installed"
            exit 1
        fi
    done
}

# Function to print logs in bold for clarity
log_info() {
    echo -e "\033[1;34m[INFO]\033[0m \033[1m$(date '+%Y-%m-%d %H:%M:%S') - $1\033[0m"
}

# Function to print errors in red
log_error() {
    echo -e "\033[1;31m[ERROR]\033[0m \033[1m$(date '+%Y-%m-%d %H:%M:%S') - $1\033[0m"
}

# Function to check pod health
check_pod_health() {
    log_info "Checking pod health..."
    # Wait for all pods to be running
    if ! kubectl wait --for=condition=Ready pods --all --timeout=600s; then
        log_error "Some pods are not healthy."
        kubectl get pods
        return 1
    else
        log_info "All pods are healthy."
        return 0
    fi
}

# Main script
main() {
    # Check dependencies first
    check_dependencies

    # Create a Kind cluster if it doesn't exist
    log_info "Checking if the Kind cluster exists..."
    if ! kind get clusters | grep -q "kind"; then
        log_info "Creating Kind cluster..."
        if ! kind create cluster --name kind; then
            log_error "Failed to create Kind cluster"
            exit 1
        fi
    else
        log_info "Kind cluster already exists."
    fi

    # Build Docker images with error checking
    log_info "Building the Docker images..."
    if ! docker build -f ./simple-logger/Dockerfile -t simple-logger .; then
        log_error "Docker image build failed"
        exit 1
    fi

    # Load the Docker images into the Kind cluster
    log_info "Loading the Docker images into the Kind cluster..."
    if ! kind load docker-image simple-logger:latest; then
        log_error "Failed to load Docker image into Kind cluster"
        exit 1
    fi

    # Deploy services
    log_info "Deploying services to the Kind cluster..."
    deployment_files=(
        "deployments/grafana-deployment.yaml"
        "deployments/prometheus-deployment.yaml"
        "deployments/loki-deployment.yaml"
        "deployments/simple-logger-deployment.yaml"
    )

    for file in "${deployment_files[@]}"; do
        if ! kubectl apply -f "$file"; then
            log_error "Failed to apply deployment: $file"
            exit 1
        fi
    done

    # Check pod health
    if ! check_pod_health; then
        log_error "Pod health check failed"
        exit 1
    fi

    # Store background PID for port-forwarding
    local pids=()

    # Port-forward Grafana and Loki
    log_info "Port-forwarding Grafana to localhost:3000..."
    kubectl port-forward --address 0.0.0.0 svc/grafana 3000:3000 &
    pids+=($!)

    log_info "Port-forwarding Loki to localhost:3100..."
    kubectl port-forward --address 0.0.0.0 svc/loki 3100:3100 &
    pids+=($!)

    # Graceful shutdown handling
    trap 'handle_shutdown "${pids[@]}"' SIGINT SIGTERM

    log_info "Press Ctrl+C to stop and delete the resources."
    wait
}

# Shutdown handler
handle_shutdown() {
    local pids=("$@")
    echo -e "\nCaught interruption signal!"
    
    # Terminate port-forwarding processes
    for pid in "${pids[@]}"; do
        kill "$pid" 2>/dev/null
    done

    echo "Do you want to delete the deployed resources? (y/n)"
    read -r answer
    if [[ "$answer" == "y" ]]; then
        kubectl delete --all pods --namespace=default
        kubectl delete deployment --all
    fi
}

# Run the main function
main