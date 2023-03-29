import logging
import sys

from logging.handlers import RotatingFileHandler
from helpers.helper_config import get_config

__logger: logging.Logger = None

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    __logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

def get_logger() -> logging.Logger:
    global __logger
    if __logger is None:
        config = get_config()
        __logger = logging.getLogger(config.bot_name)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        rotating_file_handler = RotatingFileHandler(
            config.logging_filename,
            maxBytes=config.logging_max_bytes,
            backupCount=config.logging_backup_count,
        )
        rotating_file_handler.setFormatter(formatter)
        __logger.addHandler(rotating_file_handler)
        __logger.setLevel(config.logging_level)
        sys.excepthook = handle_exception

    return __logger
