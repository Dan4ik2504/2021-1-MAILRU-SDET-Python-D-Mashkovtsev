import shutil
from pathlib import Path

from ui.fixtures import *
from utils.logging_utils import set_up_logger
from utils.random_values import random_equal_values, random_different_values
import settings


def is_master_process(config):
    if hasattr(config, 'workerinput'):
        return False
    return True


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--debug_log', action='store_true')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--selenoid_vnc', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    browser = request.config.getoption('--browser')
    debug_log = request.config.getoption('--debug_log')

    selenoid = None
    with_selenoid = False
    vnc = False

    option_selenoid = request.config.getoption('--selenoid')
    option_selenoid_vnc = request.config.getoption('--selenoid_vnc')
    if option_selenoid or option_selenoid_vnc:
        selenoid = settings.SELENOID.URL
        with_selenoid = True

        if option_selenoid_vnc:
            vnc = True

    os.environ['TESTS_WITH_SELENOID'] = str(int(with_selenoid))

    return {'browser': browser, 'debug_log': debug_log, 'selenoid': selenoid, 'vnc': vnc}


def create_test_dir():
    base_test_dir = settings.GLOBAL_LOGGING.LOGS_FOLDER
    if os.path.exists(base_test_dir):
        shutil.rmtree(base_test_dir)
    os.makedirs(base_test_dir)


def pytest_configure(config):
    is_master = is_master_process(config)
    if is_master:
        create_test_dir()
    config.base_test_dir = settings.GLOBAL_LOGGING.LOGS_FOLDER
    config.is_master_process = is_master

    random_equal_values.init_random_seed(config)
    random_different_values.init_random_seed(config)


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')[:255]
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
        loggers_list.append(logger_obj)

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
    return logging.getLogger(settings.TESTS.LOGGER_NAME)
