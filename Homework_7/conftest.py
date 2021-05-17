import logging
import os
import shutil
import signal
import subprocess
from copy import copy
from pathlib import Path

import allure
import pytest
import requests
from requests.exceptions import ConnectionError

import exceptions
from mocks import app_mock
import settings
from utils.paths import paths
from utils.wait import wait
from utils.logging_utils import set_up_logger


def is_master_process(config):
    if hasattr(config, 'workerinput'):
        return False
    return True


@pytest.fixture(scope='session')
def start_app(config):
    app_path = os.path.join(paths.repo_root, 'app', 'app.py')

    env = copy(os.environ)
    env['APP_HOST'] = settings.APP_SETTINGS.HOST
    env['APP_PORT'] = settings.APP_SETTINGS.PORT

    env['STUB_HOST'] = settings.STUB_SETTINGS.HOST
    env['STUB_PORT'] = settings.STUB_SETTINGS.PORT

    env['MOCK_HOST'] = settings.MOCK_SETTINGS.HOST
    env['MOCK_PORT'] = settings.MOCK_SETTINGS.PORT

    env['PYTHONPATH'] = paths.repo_root

    env['WERKZEUG_RUN_MAIN'] = 'true'

    proc = subprocess.Popen([settings.PYTHON_SHELL_COMMAND, app_path], env=env, stdout=subprocess.DEVNULL,
                            cwd=paths.repo_root)

    timeout = 5
    try:
        wait(requests.get, url=settings.APP_SETTINGS.URL, timeout=timeout, interval=0.1, error=ConnectionError)
    except exceptions.WaitTimeoutException:
        raise exceptions.AppConnectionError(f"Connection error. App did not started in {timeout} seconds")

    yield

    proc.send_signal(signal.SIGINT)
    exit_code = proc.wait()

    assert exit_code == 0


@pytest.fixture(scope='session')
def start_stub(config):
    stub_path = os.path.join(paths.repo_root, 'mocks', 'app_stub.py')

    env = copy(os.environ)
    env['STUB_HOST'] = settings.STUB_SETTINGS.HOST
    env['STUB_PORT'] = settings.STUB_SETTINGS.PORT

    env['PYTHONPATH'] = paths.repo_root

    env['WERKZEUG_RUN_MAIN'] = 'true'

    proc = subprocess.Popen([settings.PYTHON_SHELL_COMMAND, stub_path], env=env, stdout=subprocess.DEVNULL,
                            cwd=paths.repo_root)

    timeout = 5
    try:
        wait(requests.get, url=settings.STUB_SETTINGS.URL, timeout=timeout, interval=0.1, error=ConnectionError)
    except exceptions.WaitTimeoutException:
        raise exceptions.StubConnectionError(f"Connection error. Stub did not started in {timeout} seconds")

    yield

    proc.send_signal(signal.SIGINT)
    proc.wait()


@pytest.fixture(scope='session')
def start_mock():
    app_mock.run_mock()

    timeout = 5
    try:
        wait(requests.get, url=settings.MOCK_SETTINGS.URL, timeout=timeout, interval=0.1, error=ConnectionError)
    except exceptions.WaitTimeoutException:
        raise exceptions.MockConnectionError(f"Connection error. Mock did not started in {timeout} seconds")

    yield

    requests.get(f'{settings.MOCK_SETTINGS.URL}/shutdown')


def pytest_configure(config):
    is_master = is_master_process(config)

    if is_master:
        create_test_dir()

    config.base_test_dir = settings.LOGGING.BASE_TEST_DIR
    config.is_master_process = is_master


def pytest_addoption(parser):
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    debug_log = request.config.getoption('--debug_log')

    return {'debug_log': debug_log}


def create_test_dir():
    base_test_dir = settings.LOGGING.BASE_TEST_DIR
    if os.path.exists(base_test_dir):
        shutil.rmtree(base_test_dir)
    os.makedirs(base_test_dir)


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def loggers_init(test_dir, config):
    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

    loggers_list = []
    log_files = []

    for logger_name, log_file_name in settings.LOGGERS_LIST:
        log_file_path = os.path.join(test_dir, log_file_name)
        log_files.append((log_file_name, log_file_path))
        logger_obj = logging.getLogger(logger_name)
        set_up_logger(logger_obj, log_file_path, log_level=log_level)

    yield

    for log in loggers_list:
        for handler in log.handlers:
            handler.close()

    for log_file_name, log_file_path in log_files:
        file_path = Path(log_file_path)
        if file_path.is_file():
            with open(log_file_path, 'r') as f:
                allure.attach(f.read(), log_file_name, attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope='function')
def logger(test_dir, config):
    return logging.getLogger(settings.LOGGING.LOGGER_NAME)
