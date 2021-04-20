import shutil
import logging

import allure
import pytest
import os

import settings
from app.fixtures import *

logger = logging.getLogger(settings.Logging.LOGGER_NAME)


def is_master_process(config):
    if hasattr(config, 'workerinput'):
        return False
    return True


def pytest_addoption(parser):
    parser.addoption('--debug_log', action='store_true')
    parser.addoption('--appium', default=settings.Appium.URL)


@pytest.fixture(scope='session')
def config(request):
    debug_log = request.config.getoption('--debug_log')
    appium_url = request.config.getoption('--appium')

    return {'debug_log': debug_log, "appium_url": appium_url}


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


@pytest.fixture(scope='session', autouse=True)
def add_allure_environment_property(request):
    """Add environment properties to allure log directory"""
    alluredir = request.config.getoption('--alluredir')
    if alluredir:
        env_props = settings.Logging.ALLURE_ENVIRONMENT_PROPERTIES_DICT
        if not os.path.exists(alluredir):
            os.makedirs(alluredir)
        allure_env_path = os.path.join(alluredir, 'environment.properties')

        with open(allure_env_path, 'w') as f:
            for key, value in list(env_props.items()):
                f.write(f'{key}={value}\n')
