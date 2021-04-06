import logging
import shutil
import dataclasses
import pytest
import os

import allure

from ui.fixtures import *
import settings
from utils import random_values


def is_master_process(config):
    if hasattr(config, 'workerinput'):
        return False
    return True


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


def create_test_dir(config):
    base_test_dir = settings.Logging.BASE_TEST_DIR
    if os.path.exists(base_test_dir):
        shutil.rmtree(base_test_dir)
    os.makedirs(base_test_dir)


def pytest_configure(config):
    is_master = is_master_process(config)
    if is_master:
        create_test_dir(config)
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
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
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


class RandomValues:
    _cache = None
    CACHE_FILENAME = "random_values_cache.json"

    data = {
        "password": random_values.password,
        "email": random_values.email,
        "phone_number": random_values.phone_number,
        "incorrect_login": random_values.incorrect_login,
    }

    class NoCacheException(Exception):
        pass

    @dataclasses.dataclass(frozen=True)
    class CacheClass:
        password: str
        email: str
        phone_number: str
        incorrect_login: str

    def __init__(self, config, random_values_cache_file_path):
        self.random_values_init_cache(config, random_values_cache_file_path)

    @property
    def cache(self):
        if self._cache:
            return self._cache
        raise self.NoCacheException("The cache was not created in the fixture")

    @cache.setter
    def cache(self, value: dict):
        self._cache = self.CacheClass(**value)

    def random_values_init_cache(self, config, random_values_cache_file_path):
        if is_master_process(config):
            self.random_values_create_cache(random_values_cache_file_path)
        else:
            self.random_values_load_cache(random_values_cache_file_path)

    def random_values_load_cache(self, random_values_cache_file_path):
        with open(random_values_cache_file_path, 'r') as f:
            result = json.load(f)
        if result:
            self.cache = result
        else:
            raise self.NoCacheException("Cache file is empty")

    def random_values_create_cache(self, random_values_cache_file_path):
        for key in self.data.keys():
            self.data[key] = self.data[key]()
        self.cache = self.data
        self.create_file(random_values_cache_file_path)
        with open(random_values_cache_file_path, 'w') as f:
            json.dump(dataclasses.asdict(self.cache), f)

    @staticmethod
    def create_file(path):
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise


@pytest.fixture(scope='session')
def random_data(config, random_values_cache_file_path):
    return RandomValues(config, random_values_cache_file_path).cache


@pytest.fixture(scope='session')
def random_values_cache_file_path(repo_root):
    return os.path.abspath(
        os.path.join(repo_root, settings.Basic.TEMPORARY_FILES_DIR, RandomValues.CACHE_FILENAME))


@pytest.fixture(scope='session')
def random_email(random_data):
    return random_data.email


@pytest.fixture(scope='session')
def random_phone_number(random_data):
    return random_data.phone_number


@pytest.fixture(scope='session')
def random_password(random_data):
    return random_data.password


@pytest.fixture(scope='session')
def random_incorrect_login(random_data):
    return random_data.incorrect_login
