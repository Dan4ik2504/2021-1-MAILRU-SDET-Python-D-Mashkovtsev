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


def is_master_process(config):
    if hasattr(config, 'workerinput'):
        return False
    return True


def start_app(config):
    app_path = os.path.join(paths.repo_root, 'app', 'app.py')

    app_out = open(settings.APP_SETTINGS.LOG_STDOUT, 'w')
    app_err = open(settings.APP_SETTINGS.LOG_STDERR, 'w')

    env = copy(os.environ)
    env['APP_HOST'] = settings.APP_SETTINGS.HOST
    env['APP_PORT'] = settings.APP_SETTINGS.PORT

    env['STUB_HOST'] = settings.STUB_SETTINGS.HOST
    env['STUB_PORT'] = settings.STUB_SETTINGS.PORT

    env['MOCK_HOST'] = settings.MOCK_SETTINGS.HOST
    env['MOCK_PORT'] = settings.MOCK_SETTINGS.PORT

    env['PYTHONPATH'] = paths.repo_root

    proc = subprocess.Popen([settings.PYTHON_SHELL_COMMAND, app_path], stdout=app_out, stderr=app_err, env=env,
                            cwd=paths.repo_root)

    config.app_proc = proc
    config.app_out = app_out
    config.app_err = app_err

    timeout = 5
    try:
        wait(requests.get, url=settings.APP_SETTINGS.URL, timeout=timeout, interval=0.1, error=ConnectionError)
    except exceptions.WaitTimeoutException:
        raise exceptions.AppConnectionError(f"Connection error. App did not started in {timeout} seconds")


def start_stub(config):
    stub_path = os.path.join(paths.repo_root, 'mocks', 'app_stub.py')

    stub_out = open(settings.STUB_SETTINGS.LOG_STDOUT, 'w')
    stub_err = open(settings.STUB_SETTINGS.LOG_STDERR, 'w')

    env = copy(os.environ)
    env['STUB_HOST'] = settings.STUB_SETTINGS.HOST
    env['STUB_PORT'] = settings.STUB_SETTINGS.PORT

    env['PYTHONPATH'] = paths.repo_root

    proc = subprocess.Popen([settings.PYTHON_SHELL_COMMAND, stub_path], stdout=stub_out, stderr=stub_err, env=env,
                            cwd=paths.repo_root)

    config.stub_proc = proc
    config.stub_out = stub_out
    config.stub_err = stub_err

    timeout = 5
    try:
        wait(requests.get, url=settings.STUB_SETTINGS.URL, timeout=timeout, interval=0.1, error=ConnectionError)
    except exceptions.WaitTimeoutException:
        raise exceptions.StubConnectionError(f"Connection error. Stub did not started in {timeout} seconds")


def start_mock():
    app_mock.run_mock()

    timeout = 5
    try:
        wait(requests.get, url=settings.MOCK_SETTINGS.URL, timeout=timeout, interval=0.1, error=ConnectionError)
    except exceptions.WaitTimeoutException:
        raise exceptions.MockConnectionError(f"Connection error. Mock did not started in {timeout} seconds")


def pytest_configure(config):
    is_master = is_master_process(config)

    if is_master:
        create_test_dir()
        start_mock()
        start_stub(config)
        start_app(config)

    config.base_test_dir = settings.LOGGING.BASE_TEST_DIR
    config.is_master_process = is_master


def stop_app(config):
    if hasattr(config, 'app_proc'):
        config.app_proc.send_signal(signal.SIGINT)
        exit_code = config.app_proc.wait()

        config.app_out.close()
        config.app_err.close()

        assert exit_code == 0


def stop_stub(config):
    if hasattr(config, 'stub_proc'):
        config.stub_proc.send_signal(signal.SIGINT)
        config.stub_proc.wait()

        config.stub_out.close()
        config.stub_err.close()


def stop_mock():
    requests.get(f'{settings.MOCK_SETTINGS.URL}/shutdown')


def pytest_unconfigure(config):
    if is_master_process(config):
        stop_app(config)
        stop_stub(config)
        stop_mock()


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
def logger(test_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-20s - %(levelname)-6s - %(message)s')
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

    log_files = (
        log_file,
        settings.APP_SETTINGS.LOG_STDOUT,
        settings.APP_SETTINGS.LOG_STDERR,
        settings.MOCK_SETTINGS.LOG_STDOUT,
        settings.MOCK_SETTINGS.LOG_STDERR,
        settings.STUB_SETTINGS.LOG_STDOUT,
        settings.STUB_SETTINGS.LOG_STDERR
    )

    for log_file_name in log_files:
        file_path = Path(log_file_name)
        if file_path.is_file():
            with open(log_file_name, 'r') as f:
                allure.attach(f.read(), log_file_name, attachment_type=allure.attachment_type.TEXT)
