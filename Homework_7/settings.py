import os

from utils.paths import paths


class LOGGING:
    BASE_TEST_DIR = paths.different_os_path('/tmp/app_tests')
    LOG_FILE_NAME = 'test.log'
    LOG_FILE_PATH = os.path.join(BASE_TEST_DIR, LOG_FILE_NAME)
    LOGGER_NAME = 'app_test'
    DEFAULT_FORMAT = '%(asctime)s - %(filename)-15s - %(levelname)-8s - %(message)s'


class FLASK_SETTINGS:
    LOG_FORMAT = '%(message)s'


class APP_SETTINGS:
    HOST = '127.0.0.1'
    PORT = '8081'
    URL = f'http://{HOST}:{PORT}'
    FILE_PATH = os.path.join(paths.repo_root, 'app', 'app.py')
    FLASK_LOG_FILE_PATH = os.path.join(LOGGING.BASE_TEST_DIR, 'app_flask.log')
    LOG_FILE_PATH = os.path.join(LOGGING.BASE_TEST_DIR, 'app.log')


class STUB_SETTINGS:
    HOST = '127.0.0.1'
    PORT = '8082'
    URL = f'http://{HOST}:{PORT}'
    FILE_PATH = os.path.join(paths.repo_root, 'mocks', 'app_stub.py')
    FLASK_LOG_FILE_PATH = os.path.join(LOGGING.BASE_TEST_DIR, 'stub_flask.log')
    LOG_FILE_PATH = os.path.join(LOGGING.BASE_TEST_DIR, 'stub.log')


class MOCK_SETTINGS:
    HOST = '127.0.0.1'
    PORT = '8083'
    URL = f'http://{HOST}:{PORT}'
    USER_ACTIONS_URL = URL + '/last_name'
    USER_ACTIONS_URL_BASE = USER_ACTIONS_URL + "/{}"
    FLASK_LOG_FILE_PATH = os.path.join(LOGGING.BASE_TEST_DIR, 'mock_flask.log')
    LOG_FILE_PATH = os.path.join(LOGGING.BASE_TEST_DIR, 'mock.log')


class HTTP_CLIENT_SETTINGS:
    LOGGER_NAME = 'http_client_logger'
    LOG_FILE_NAME = 'http_client.log'
    LOG_FILE_PATH = os.path.join(LOGGING.BASE_TEST_DIR, LOG_FILE_NAME)


LOGGERS_LIST = [
    (LOGGING.LOGGER_NAME, LOGGING.LOG_FILE_NAME),
    (HTTP_CLIENT_SETTINGS.LOGGER_NAME, HTTP_CLIENT_SETTINGS.LOG_FILE_NAME)
]

PYTHON_SHELL_COMMAND = "python3"
