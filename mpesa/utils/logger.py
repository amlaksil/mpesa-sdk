#!/usr/bin/python3
"""
This module sets up a logger with a rotating file handler and a stream handler.
Logs are written to the (MPESA_LOG_DIR) or 'logs' directory with a
configurable log level that can be set via the 'LOG_LEVEL' environment
variable. The log file size is managed with a rotating file handler, which
limits the file size and keeps backup logs to avoid unbounded growth.

Key Features:
- Log level can be dynamically configured (default: DEBUG).
- Logs are saved in the 'logs' directory.
- RotatingFileHandler ensures log file management with a
maximum size of 10MB and keeps up to 5 backup logs.
- StreamHandler outputs logs to the console for real-time monitoring.
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from mpesa.config import Config

log_dir = Config.MPESA_LOG_DIR if Config.MPESA_LOG_DIR else os.path.join(
    os.getcwd(), "logs")
log_file_path = os.path.join(log_dir, "mpesa.log")


def get_logger(name: str) -> logging.Logger:
    """
    This function creates a logger that is module-specific, allowing
    logs to be traced back to the module that generated them.

    Args:
        name (str): The name of the module.

    Returns:
        logging.Logger: The logger instance for the calling module.
    """
    formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger(name)

    if not logger.handlers:
        log_level = 'DEBUG' if not Config.LOG_LEVEL else Config.LOG_LEVEL
        logger.setLevel(getattr(logging, log_level, logging.DEBUG))
        os.makedirs(log_dir, exist_ok=True)

        file_handler = RotatingFileHandler(
                log_file_path, maxBytes=10 * 1024 * 1024, backupCount=5
                )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        if Config.ENVIRONMENT != 'TEST':
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

    return logger


if __name__ == '__main__':
    logger = get_logger(__name__)
    logger.info(
            "Logger configured successfully. Log file path: %s", log_file_path)
