import time
import random
import logging
import os
from prometheus_client import Gauge, start_http_server
from logging_loki import LokiHandler

cpu_load_gauge = Gauge("cpu_load", "Database CPU load")

LOKI_URL = os.getenv("LOKI_URL", "http://loki:3100/loki/api/v1/push")
LOG_FORMAT = (
    '{"timestamp": "%(asctime)s", "level": "%(levelname)s", '
    '"filename": "%(filename)s", "line": %(lineno)d, "message": "%(message)s"}'
)

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("cpu_monitor_logger")
logger.setLevel(logging.INFO)

loki_handler = LokiHandler(
    LOKI_URL,
    version="1",
    tags={"job": "cpu_monitor", "service": "monitoring-app"},
)

formatter = logging.Formatter(LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")
loki_handler.setFormatter(formatter)
logger.addHandler(loki_handler)

try:
    start_http_server(8001)
    logger.info("Prometheus HTTP server started", extra={"event": "server_start"})
except Exception as e:
    logger.error("Failed to start Prometheus HTTP server", extra={"error": str(e)})
    exit(1)

while True:
    if int(random.uniform(0, 60)) == 5:
        cpu_load = random.uniform(90, 100)
    else:
        cpu_load = random.uniform(20, 100)
    cpu_load_gauge.set(cpu_load)

    log_metadata = {"cpu_load": str(cpu_load), "event": "cpu_usage_check"}

    if cpu_load >= 90:
        logger.warning("High CPU load detected", extra={**log_metadata, "alert": "warning"})
        logger.error("Kubernetes pod in danger", extra={**log_metadata, "alert": "error"})
        logger.critical("Critical CPU condition", extra={**log_metadata, "alert": "critical"})
    else:
        logger.info("CPU load normal", extra=log_metadata)
    
    logger.info("CPU load updated", extra=log_metadata)

    time.sleep(1)
