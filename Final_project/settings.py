from logging import INFO as LOG_LEVEL_INFO
from utils.paths import paths

BASE_URL = 'http://localhost'


# App settings

class DATABASE_SETTINGS:
    HOST = 'myapp_db'
    PORT = 3306
    USER = 'root'
    PASSWORD = 'pass'


class MOCK_SETTINGS:
    HOST = '0.0.0.0'
    PORT = '8008'
    URL = f'{BASE_URL}:{PORT}'
    DB_NAME = 'vk_api_db'

    class LOGGING:
        LOG_FILE_PATH = paths.different_os_path('/tmp/mock_logs.log')
        LOGGER_NAME = 'vk_api_mock_logger'


class APP_SETTINGS:
    HOST = '0.0.0.0'
    PORT = '8070'
    URL = f'{BASE_URL}:{PORT}'


# Tests settings

class TESTS:
    LOGGER_NAME = 'myapp_test'
    LOG_FILE_NAME = 'test.log'


class BROWSER:
    SCREENSHOT_FILE_NAME = 'failure.png'
    LOG_FILE_NAME = 'browser.log'


class UI:
    DEFAULT_TIMEOUT = 10
    DEFAULT_CHECKING_INTERVAL = 0.1
    CLICK_RETRY = 3


class API_CLIENT:
    class COOKIES:
        SESSION = 'session'


class GLOBAL_LOGGING:
    LOGS_FOLDER = paths.different_os_path('/tmp/myapp_tests_logs/')
    LEVEL = LOG_LEVEL_INFO
    DEFAULT_FORMAT = '%(asctime)s - %(filename)-15s - %(levelname)-8s - %(message)s'


class SELENOID:
    URL = "http://127.0.0.1:4444/wd/hub"
    CHROME_LATEST = 'latest'
    CHROME_DEFAULT_VERSION = '90.0'
    CHROME_DEFAULT_VERSION_VNC = '90.0_vnc'


LOGGERS_LIST = (
    (TESTS.LOGGER_NAME, TESTS.LOG_FILE_NAME),
)
