import time
import random
import logging
from prometheus_client import Gauge, start_http_server

import logging_loki
from logging_loki import LokiHandler

cpu_load_gauge = Gauge('cpu_load', 'Database CPU load')

logging.basicConfig(level=logging.INFO)
logging_loki.emitter.LokiEmitter.level_tag = "level"

loki_handler = LokiHandler(
    "http://host.docker.internal:3100/loki/api/v1/push",
    version="1",
    tags={"job": "cpu_monitor", "service": "monitoring-app"}
    )
loki_handler.setLevel(logging.INFO)

logger = logging.getLogger("my-logger")
logger.addHandler(loki_handler)
logger.setLevel(logging.INFO)

try:
    start_http_server(8001)
    logger.info("Prometheus HTTP server started on port 8001")
except Exception as e:
    logger.error(f"Failed to start Prometheus HTTP server: {e}")
    exit(1)
    
start_time = time.time()

while True:
    if int(random.uniform(0, 60)) == 5:
        cpu_load = random.uniform(90, 100)
        logger.warning(f"High CPU load detected: {cpu_load}")
    else:
        cpu_load = random.uniform(20, 30)
    
    cpu_load_gauge.set(cpu_load)
    logger.info(f"New CPU load: {cpu_load}")
    logger.info(f"Logging to Loki: CPU load is {cpu_load}")
    
    time.sleep(5)
