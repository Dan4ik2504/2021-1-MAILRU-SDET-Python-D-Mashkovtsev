import logging
import os
import shutil
import sys

import allure
import pytest

import settings
from utils.paths import paths

from database.fixtures import *

logger = logging.getLogger(settings.LOGGING.LOGGER_NAME)


def is_master(config):
    return not hasattr(config, 'workerinput')


def pytest_addoption(parser):
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    debug_log = request.config.getoption('--debug_log')
    return {'debug_log': debug_log}


def create_test_dir(base_test_dir):
    if os.path.exists(base_test_dir):
        shutil.rmtree(base_test_dir)
    os.makedirs(base_test_dir)


def pytest_configure(config):
    base_test_dir = settings.LOGGING.BASE_TEST_DIR_WINDOWS if sys.platform.startswith('win') \
        else settings.LOGGING.BASE_TEST_DIR_LINUX

    config.base_test_dir = base_test_dir

    if is_master(config):
        recreate_db()
        create_test_dir(base_test_dir)

    return config


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = paths.different_os_path(request._pyfuncitem.nodeid)
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    log_formatter = logging.Formatter(settings.LOGGING.LOG_STRING_FORMAT)
    log_file = os.path.join(test_dir, settings.LOGGING.TEST_LOG_FILE_NAME)

    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger(settings.LOGGING.LOGGER_NAME)
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), settings.LOGGING.TEST_LOG_FILE_NAME, attachment_type=allure.attachment_type.TEXT)