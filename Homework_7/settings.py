import os

from utils.paths import paths


class LOGGING:
    BASE_TEST_DIR = paths.different_os_path('/tmp/app_tests')
    TEST_LOG_FILE_NAME = 'test.log'
    LOGGER_NAME = 'app_test'


class APP_SETTINGS:
    HOST = '127.0.0.1'
    PORT = '8081'
    URL = f'http://{HOST}:{PORT}'
    LOG_STDOUT = os.path.join(LOGGING.BASE_TEST_DIR, 'app_stdout.log')
    LOG_STDERR = os.path.join(LOGGING.BASE_TEST_DIR, 'app_stderr.log')


class STUB_SETTINGS:
    HOST = '127.0.0.1'
    PORT = '8082'
    URL = f'http://{HOST}:{PORT}'
    LOG_STDOUT = os.path.join(LOGGING.BASE_TEST_DIR, 'stub_stdout.log')
    LOG_STDERR = os.path.join(LOGGING.BASE_TEST_DIR, 'stub_stderr.log')


class MOCK_SETTINGS:
    HOST = '127.0.0.1'
    PORT = '8083'
    URL = f'http://{HOST}:{PORT}'
    LOG_STDOUT = os.path.join(LOGGING.BASE_TEST_DIR, 'mock_stdout.log')
    LOG_STDERR = os.path.join(LOGGING.BASE_TEST_DIR, 'mock_stderr.log')


PYTHON_SHELL_COMMAND = "python3"
