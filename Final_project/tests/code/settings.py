from logging import INFO as LOG_LEVEL_INFO
from utils.paths import paths
import sys
import inspect

IN_DOCKER = '--in_docker' in sys.argv
WITH_SELENOID = '--selenoid' in sys.argv or '--selenoid_vnc' in sys.argv


# App settings

class _BASE_APP_CLASS:
    HOST_DEFAULT = 'localhost'
    HOST_DOCKER = None
    PORT = None
    URL_BASE = 'http://{host}:{port}'

    @property
    def HOST(self):
        if IN_DOCKER:
            return self.HOST_DOCKER
        else:
            return self.HOST_DEFAULT

    @property
    def URL(self):
        return self.URL_BASE.format(host=self.HOST, port=self.PORT)


class _DATABASE_SETTINGS(_BASE_APP_CLASS):
    HOST_DOCKER = 'myapp_db'
    PORT = 3306
    USER = 'root'
    PASSWORD = 'pass'
    URL_BASE = f'mysql+pymysql://{USER}:{PASSWORD}' + '@{host}:{port}'


DATABASE_SETTINGS = _DATABASE_SETTINGS()


class _MOCK_SETTINGS(_BASE_APP_CLASS):
    HOST_DOCKER = 'vk_api'
    PORT = '8008'
    DB_NAME = 'vk_api_db'
    TABLE_VK_ID_NAME = 'vk_id_table'


MOCK_SETTINGS = _MOCK_SETTINGS()


class _APP_SETTINGS(_BASE_APP_CLASS):
    HOST_DOCKER = 'myapp'
    PORT = '8070'
    DB_NAME = 'myapp_db'
    TABLE_USERS_NAME = 'test_users'

    @property
    def HOST(self):
        if IN_DOCKER or WITH_SELENOID:
            return self.HOST_DOCKER
        else:
            return self.HOST_DEFAULT


APP_SETTINGS = _APP_SETTINGS()


class _URLS:
    LOGIN = '/login'
    REGISTRATION = '/reg'
    MAIN = '/welcome/'
    LOGOUT = '/logout'

    def __init__(self, url):
        attrs = inspect.getmembers(self)
        attrs = [a for a in attrs if isinstance(a[1], str) and not a[0].startswith('_')]

        for k, v in attrs:
            setattr(self, k, url + v)


APP_SETTINGS.URLS = _URLS(APP_SETTINGS.URL)


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
    PORT = '4444'
    URL_BASE = "http://{host}:{port}/wd/hub"
    CHROME_LATEST = 'latest'
    CHROME_DEFAULT_VERSION = '90.0'
    CHROME_DEFAULT_VERSION_VNC = '90.0_vnc'


SELENOID = _SELENOID()


class RANDOMIZER:
    DEFAULT_LENGTH = 10


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
    LOGS_FOLDER = paths.different_os_path('/myapp_tests_logs/' if IN_DOCKER
                                          else '/tmp/myapp_tests_logs')
    LEVEL = LOG_LEVEL_INFO
    DEFAULT_FORMAT = '%(asctime)s - %(filename)-15s - %(levelname)-8s - %(message)s'
    MAX_RESPONSE_LENGTH = 200


LOGGERS_LIST = (
    (TESTS.LOGGER_NAME, TESTS.LOG_FILE_NAME),
)
