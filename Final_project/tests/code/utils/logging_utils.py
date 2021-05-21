import logging

import settings


def set_up_logger(logger, log_file_path, log_level=logging.INFO, log_format=settings.GLOBAL_LOGGING.DEFAULT_FORMAT):
    log_formatter = logging.Formatter(log_format)

    logger.propagate = False
    logger.setLevel(log_level)
    logger.handlers.clear()

    file_handler = logging.FileHandler(log_file_path, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    logger.addHandler(file_handler)

    return logger
