import logging

unwanted_loggers = [
    logging.getLogger("urllib3.connectionpool"),
]

for logger in unwanted_loggers:
    logger.disabled = True

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(filename)s] %(levelname)s: %(message)s")