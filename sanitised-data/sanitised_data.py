import random
import time
import logging
from prometheus_client import start_http_server, Gauge

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create a Prometheus Gauge metric for CPU load
cpu_load_gauge = Gauge('cpu_load', 'Simulated CPU Load')

# Start the HTTP server on port 8001
try:
    start_http_server(8001)
    logging.info("Prometheus HTTP server started on port 8001")
except Exception as e:
    logging.error(f"Failed to start Prometheus HTTP server: {e}")
    exit(1)

# Simulate historical data with a spike
logging.info("Generating 100 historical data points with a spike...")
timestamps = [time.time() - (60 * i) for i in range(99, -1, -1)]  # Last hour

for i, ts in enumerate(timestamps):
    if 45 <= i <= 55:  # Introduce a spike in the middle
        cpu_load = random.uniform(80, 100)
    else:
        cpu_load = random.uniform(20, 50)

    cpu_load_gauge.set(cpu_load)  # Update metric
    logging.info(f"Timestamp: {ts}, CPU Load: {cpu_load}")
    time.sleep(0.1)  # Small delay to simulate loading historical data

# Continue generating live data
while True:
    logging.info("Generating and pushing new CPU load data")
    cpu_load = random.uniform(20, 50)  # Normal load range
    cpu_load_gauge.set(cpu_load)
    logging.info(f"New CPU load: {cpu_load}")
    time.sleep(5)  # Update every 5 seconds
