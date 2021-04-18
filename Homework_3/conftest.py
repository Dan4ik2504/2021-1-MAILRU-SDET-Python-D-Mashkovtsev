import shutil
import logging

import allure
import pytest
import os

import settings
from utils.random_values import random_values

from api.fixtures import *

logger = logging.getLogger(settings.Logging.LOGGER_NAME)


def is_master_process(config):
    if hasattr(config, 'workerinput'):
        return False
    return True


def pytest_addoption(parser):
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    debug_log = request.config.getoption('--debug_log')

    return {'debug_log': debug_log}


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


def create_test_dir():
    base_test_dir = settings.Logging.BASE_TEST_DIR
    if os.path.exists(base_test_dir):
        shutil.rmtree(base_test_dir)
    os.makedirs(base_test_dir)


def pytest_configure(config):
    is_master = is_master_process(config)
    if is_master:
        create_test_dir()
    config.base_test_dir = settings.Logging.BASE_TEST_DIR
    config.is_master_process = is_master

    random_values.init_random_seed(config)


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-20s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, settings.Logging.TEST_LOG_FILE_NAME)

    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger(settings.Logging.LOGGER_NAME)
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), settings.Logging.TEST_LOG_FILE_NAME, attachment_type=allure.attachment_type.TEXT)
