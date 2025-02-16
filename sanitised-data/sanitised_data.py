import time
import random
import logging
from prometheus_client import Gauge, start_http_server

logging.basicConfig(level=logging.INFO)

cpu_load_gauge = Gauge('cpu_load', 'Database CPU load')

try:
    start_http_server(8001)
    logging.info("Prometheus HTTP server started on port 8001")
except Exception as e:
    logging.error(f"Failed to start Prometheus HTTP server: {e}")
    exit(1)
    
start_time = time.time()

while True:
   
    if int(random.uniform(0, 60)) == 5:
        cpu_load = random.uniform(90, 100)
    else:
        cpu_load = random.uniform(20, 30)
    
    cpu_load_gauge.set(cpu_load)
    logging.info(f"New CPU load: {cpu_load}")
    
    time.sleep(5)
