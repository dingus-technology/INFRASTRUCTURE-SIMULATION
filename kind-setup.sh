# kind-setup.sh: A script to setup a Kind cluster and deploy the services to it.
#!/bin/bash

# Function to print logs in bold for clarity
log_info() {
    echo -e "\033[1;34m[INFO]\033[0m \033[1m$(date '+%Y-%m-%d %H:%M:%S') - $1\033[0m"
}

# Create a Kind cluster if it doesn't exist
log_info "Checking if the Kind cluster exists..."
if ! kind get clusters | grep -q "kind"; then
  log_info "Creating Kind cluster..."
  kind create cluster --name kind 
  echo "Kind cluster created"
else
  log_info "Kind cluster already exists."
fi

# Check if the .kube directory exists
if [ ! -d "$HOME/.kube" ]; then
  log_info "Creating ~/.kube directory."
  mkdir -p "$HOME/.kube"
fi

# Check if the kubeconfig file exists
if [ -f "$HOME/.kube/config" ]; then
  log_info "Checking if 'kind' context already exists in the kubeconfig."
  
  # Check if the 'kind-kind' context already exists
  if ! kubectl config get-contexts | grep -q "kind-kind"; then
    log_info "Appending kind kubeconfig to existing config."
    kind get kubeconfig --name kind >> "$HOME/.kube/config"
  else
    log_info "'kind' context already exists, skipping append."
  fi
else
  log_info "Creating a new kubeconfig file for kind."
  kind get kubeconfig --name kind > "$HOME/.kube/config"
fi

# List available contexts
log_info "Listing available contexts:"
kubectl config get-contexts

# Switch to the 'kind-kind' context
log_info "Switching to the 'kind-kind' context."
kubectl config use-context kind-kind

# Verify the current context
log_info "Verifying the current context:"
kubectl config current-context

# Build the Docker images
log_info "Building the Docker images..."
docker build -f ./simple-logger/Dockerfile -t simple-logger .

# Load the Docker images into the Kind cluster
log_info "Loading the Docker images into the Kind cluster..."
kind load docker-image simple-logger:latest

# Deploy the services to the Kind cluster
log_info "Deploying services to the Kind cluster..."
kubectl apply -f deployments/monitoring-deployment.yaml # Grafana, Prometheus, Loki
kubectl apply -f deployments/simple-logger-deployment.yaml # Simple Logger
# kubectl apply -f deployments/sanitised-data-deployment.yaml

# List available pods after deployment
log_info "Listing available pods:"
kubectl get pods

# Port-forward Grafana to localhost
log_info "Port-forwarding Grafana to localhost:3000..."
kubectl port-forward --address 0.0.0.0 svc/grafana 3000:3000