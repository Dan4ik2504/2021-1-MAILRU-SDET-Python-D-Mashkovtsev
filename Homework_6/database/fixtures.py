import logging
import os

import allure
import pytest

import settings
from database.client import MysqlClient


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user=settings.DB.USER, password=settings.DB.PASSWORD, db_name=settings.DB.DB_NAME)
    mysql_client.connect()

    yield mysql_client

    mysql_client.connection.close()


def recreate_db():
    mysql_client = MysqlClient(user=settings.DB.USER, password=settings.DB.PASSWORD, db_name=settings.DB.DB_NAME)
    mysql_client.recreate_db()

    mysql_client.connect()
    mysql_client.create_tables_for_log_analyzer()

    mysql_client.connection.close()


@pytest.fixture(scope='function')
def sqlalchemy_logs(test_dir, config):
    log_level = logging.DEBUG if config['debug_log'] else logging.INFO
    logger_names = ['sqlalchemy.engine', 'sqlalchemy.pool', 'sqlalchemy.dialects', 'sqlalchemy.orm']
    log_formatter = logging.Formatter(settings.LOGGING.LOG_STRING_FORMAT)
    sql_loggers = []

    for logger_name in logger_names:
        sql_logger = logging.getLogger(logger_name)
        sql_logger.setLevel(log_level)
        sql_logger.propagate = False
        sql_logger.handlers.clear()

        log_file_path = os.path.join(test_dir, logger_name + ".log")
        file_handler = logging.FileHandler(log_file_path, 'w')
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(log_level)
        sql_logger.addHandler(file_handler)

        sql_loggers.append(sql_logger)

    yield

    for sql_logger in sql_loggers:
        for handler in sql_logger.handlers:
            handler.close()

    for logger_name in logger_names:
        log_file_name = logger_name + ".log"
        log_file_path = os.path.join(test_dir, log_file_name)

        with open(log_file_path, 'r') as f:
            allure.attach(f.read(), log_file_name, attachment_type=allure.attachment_type.TEXT)
