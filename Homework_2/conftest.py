import logging
import shutil
import pytest
import os

import allure

from ui.fixtures import *
import settings
from utils import random_values


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')
    debug_log = request.config.getoption('--debug_log')
    return {'browser': browser, 'debug_log': debug_log}


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.pardir))


def is_master(config):
    if hasattr(config, 'workerinput'):
        return False
    return True


def create_test_dir(config):
    base_test_dir = settings.Logging.BASE_TEST_DIR
    if os.path.exists(base_test_dir):
        shutil.rmtree(base_test_dir)
    os.makedirs(base_test_dir)


def pytest_configure(config):

    if is_master(config):
        create_test_dir(config)
        random_values.Caching.create_cache()
    else:
        random_values.Caching.read_cache_from_json()

    config.base_test_dir = settings.Logging.BASE_TEST_DIR


@pytest.fixture(scope='function')
def test_dir(request):
    test_dir = os.path.join(request.config.base_test_dir, request._pyfuncitem.nodeid)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, settings.Logging.TEST_LOG_FILE_NAME)

    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger(settings.Logging.LOGGER_NAME)
    log.propagate = False
    log.setLevel(log_level)
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()

    with open(log_file, 'r') as f:
        allure.attach(f.read(), settings.Logging.TEST_LOG_FILE_NAME, attachment_type=allure.attachment_type.TEXT)
