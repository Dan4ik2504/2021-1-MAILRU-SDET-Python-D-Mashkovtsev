import sys
from urllib.parse import urljoin


def different_os_path(path: str):
    """Changing the path to be able to work on different operating systems"""
    if sys.platform.startswith('win'):
        return "".join(("C:\\tests", path.replace("/", "\\")))
    return path


class Basic:
    TEST_FILES_DIR = 'test_files'
    TEMPORARY_FILES_DIR = 'temporary_files'


class TestFiles:
    ICON_NAME = "icon_256x256"
    ICON_FILE = "256x256.jpg"
    IMAGE_NAME = "image_600x600"
    IMAGE_FILE = "600x600.jpg"
    LARGE_IMAGE_NAME = "image_1080x607"
    LARGE_IMAGE_FILE = "1080x607.jpg"


class Logging:
    BASE_TEST_DIR = different_os_path('/tmp/selenium_tests')
    TEST_LOG_FILE_NAME = 'test.log'
    SCREENSHOT_FILE_NAME = 'failure.png'
    BROWSER_LOG_FILE_NAME = 'browser.log'
    LOGGER_NAME = 'mytarget_test'
    MAX_RESPONSE_LENGTH = 200


class Url:
    BASE = "https://target.my.com/"

    _PATHS = {
        "dashboard": "dashboard",
        "segments": "segments",
        "billing": "billing",
        "statistics": "statistics",
        "pro": "pro",
        "profile": "profile",
        "tools": "tools",
        "help": "help/advertisers/ru",
    }

    _FULL_PATHS = {
        "segments": "segments/segments_list",
        "new_campaign": "campaign/new"
    }

    LOGIN = "https://account.my.com/login"
    POST_LOGIN = 'https://auth-ac.my.com/auth'
    CSRF = urljoin(BASE, "csrf/")
    LOGOUT = urljoin(BASE, "logout")
    DASHBOARD = urljoin(BASE, _PATHS["dashboard"])
    SEGMENTS = urljoin(BASE, _FULL_PATHS["segments"])
    SEGMENT_CREATING = urljoin(SEGMENTS, "/new")
    BILLING = urljoin(BASE, _PATHS["billing"])
    STATISTICS = urljoin(BASE, _PATHS["statistics"])
    PRO = urljoin(BASE, _PATHS["pro"])
    PROFILE = urljoin(BASE, _PATHS["profile"])
    TOOLS = urljoin(BASE, _PATHS["tools"])
    HELP = urljoin(BASE, _PATHS["help"])

    NEW_CAMPAIGN = urljoin(BASE, _FULL_PATHS["new_campaign"])

    class Api:
        BASE = "https://target.my.com/api/v2/"
        MEDIATEKA_GET_BY_ID = urljoin(BASE, "mediateka/{id}.json")
        MEDIATEKA_POST = urljoin(BASE, "mediateka.json")
        STATIC_POST = urljoin(BASE, "content/static.json")
        CAMPAIGNS_POST = urljoin(BASE, "campaigns.json")
        REGISTER_URL_GET = "https://target.my.com/api/v1/urls/"


class User:
    LOGIN = "tebivan222@bombaya.com"
    PASSWORD = "Qwerty123456"
    USERNAME = "Тестов Тест Тестович"
    PHONE = "+70000000000"