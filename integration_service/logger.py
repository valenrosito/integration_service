
from loguru import logger
import os
from .config import SETTINGS

def configure_logger():
    os.makedirs(SETTINGS.log_dir, exist_ok=True)
    log_path = os.path.join(SETTINGS.log_dir, "service.log")
    logger.remove()
    logger.add(log_path, rotation="10 MB", retention="14 days", enqueue=True, level="INFO")
    logger.add(lambda msg: print(msg, end=""), level="INFO")
    return logger
