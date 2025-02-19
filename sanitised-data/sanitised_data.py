"""sanitised_data.py"""

import time
import random
import logging
from prometheus_client import Gauge, start_http_server
# from logging_loki import LokiHandler  # You will need to install the 'logging-loki' library

logging.basicConfig(level=logging.INFO)

# Prometheus Gauge for CPU load
cpu_load_gauge = Gauge('cpu_load', 'Database CPU load')

# Setup Loki logging handler
# loki_handler = LokiHandler("http://loki:3100/loki/api/v1/push")  # Assuming Loki is running on localhost and port 3100
# loki_handler.setLevel(logging.INFO)
# logging.getLogger().addHandler(loki_handler)

try:
    # Start the Prometheus HTTP server
    start_http_server(8001)
    logging.info("Prometheus HTTP server started on port 8001")
except Exception as e:
    logging.error(f"Failed to start Prometheus HTTP server: {e}")
    exit(1)
    
start_time = time.time()

while True:
    # Simulate random CPU load values
    if int(random.uniform(0, 60)) == 5:
        cpu_load = random.uniform(90, 100)
    else:
        cpu_load = random.uniform(20, 30)
    
    # Set the CPU load gauge value for Prometheus
    cpu_load_gauge.set(cpu_load)
    logging.info(f"New CPU load: {cpu_load}")
    
    # Send logs to Loki
    logging.info(f"Logging to Loki: CPU load is {cpu_load}")
    
    time.sleep(5)
