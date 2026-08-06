# app/core/logger.py
import logging
from app.config import settings

def configure_logging():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )