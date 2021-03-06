import os
import sys
from logging import INFO as LOG_LEVEL_INFO

from utils.paths import paths


class _EXTERNAL_SETTINGS:
    _with_selenoid = False

    @property
    def WITH_SELENOID(self):
        if not self._with_selenoid:
            self._with_selenoid = bool(int(os.environ.get('TESTS_WITH_SELENOID', False))) or '--selenoid' in sys.argv \
                                  or '--selenoid_vnc' in sys.argv
        return self._with_selenoid


EXTERNAL_SETTINGS = _EXTERNAL_SETTINGS()


# App settings

class _BASE_APP_CLASS:
    HOST = 'localhost'
    PORT = None
    URL_BASE = 'http://{host}:{port}/'

    @property
    def URL(self):
        return self.URL_BASE.format(host=self.HOST, port=self.PORT)


class _DATABASE_SETTINGS(_BASE_APP_CLASS):
    PORT = os.environ.get("MYAPP_DB_PORT", 3306)
    USER = 'root'
    PASSWORD = 'pass'
    URL_BASE = f'mysql+pymysql://{USER}:{PASSWORD}' + '@{host}:{port}'


DATABASE_SETTINGS = _DATABASE_SETTINGS()


class _MOCK_SETTINGS(_BASE_APP_CLASS):
    PORT = os.environ.get("VK_API_PORT", '8008')
    DB_NAME = 'vk_api_db'
    TABLE_VK_ID_NAME = 'vk_id_table'


MOCK_SETTINGS = _MOCK_SETTINGS()


class _APP_SETTINGS(_BASE_APP_CLASS):
    PORT = os.environ.get("MYAPP_PROXY_PORT", '8070')
    HOST_DOCKER = 'myapp_proxy'
    PORT_DOCKER = '8070'
    DB_NAME = 'myapp_db'
    TABLE_USERS_NAME = 'test_users'

    class URLS:
        LOGIN = '/login'
        REGISTRATION = '/reg'
        MAIN = '/welcome/'
        LOGOUT = '/logout'

    class API_URLS:
        API_PREFIX = '/api'
        ADD_USER = API_PREFIX + '/add_user'
        DELETE_USER = API_PREFIX + '/del_user/{username}'
        BLOCK_USER = API_PREFIX + '/block_user/{username}'
        ACCEPT_USER = API_PREFIX + '/accept_user/{username}'
        APP_STATUS = '/status'

    @property
    def URL_API(self):
        return self.URL_BASE.format(host=self.HOST, port=self.PORT)

    @property
    def URL(self):
        if EXTERNAL_SETTINGS.WITH_SELENOID:
            return self.URL_BASE.format(host=self.HOST_DOCKER, port=self.PORT_DOCKER)
        else:
            return self.URL_API


APP_SETTINGS = _APP_SETTINGS()


class EXTERNAL_URLS:
    WHAT_IS_AN_API = "https://en.wikipedia.org/wiki/API"
    FUTURE_OF_INTERNET = "https://www.popularmechanics.com/technology/infrastructure/a29666802/future-of-the-internet/"
    SMTP = "https://ru.wikipedia.org/wiki/SMTP"
    PYTHON = "https://www.python.org/"
    PYTHON_HISTORY = "https://en.wikipedia.org/wiki/History_of_Python"
    FLASK = "https://flask.palletsprojects.com/en/1.1.x/#"
    CENTOS_7 = "http://isoredirect.centos.org/centos/7/isos/x86_64/"
    WIRESHARK_NEWS = "https://www.wireshark.org/news/"
    WIRESHARK_DOWNLOAD = "https://www.wireshark.org/#download"
    TCPDUMP_EXAMPLES = "https://hackertarget.com/tcpdump-examples/"


# Tests settings

class _SELENOID(_BASE_APP_CLASS):
    HOST_DOCKER = 'selenoid'
    PORT = os.environ.get("SELENOID_PORT", '4444')
    URL_BASE = "http://{host}:{port}/wd/hub"
    CHROME_LATEST = 'latest'
    CHROME_DEFAULT_VERSION = '90.0'
    CHROME_DEFAULT_VERSION_VNC = '90.0_vnc'


SELENOID = _SELENOID()


class RANDOMIZER:
    DEFAULT_LENGTH = 10
    MAX_RETRIES = 20


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
    LOGS_FOLDER = paths.different_os_path(os.environ.get('WORKSPACE', '/tmp') + '/myapp_tests_logs/')
    LEVEL = LOG_LEVEL_INFO
    DEFAULT_FORMAT = '%(asctime)s - %(filename)-15s - %(levelname)-8s - %(message)s'
    MAX_RESPONSE_LENGTH = 200


LOGGERS_LIST = (
    (TESTS.LOGGER_NAME, TESTS.LOG_FILE_NAME),
)
