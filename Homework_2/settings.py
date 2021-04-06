import sys


def different_os_path(path: str):
    """Changing the path to be able to work on different operating systems"""
    if sys.platform.startswith('win'):
        return "".join(("C:\\tests", path.replace("/", "\\")))
    return path


class Basic:
    """Основные настройки"""
    DEFAULT_TIMEOUT = 10
    DEFAULT_CHECKING_INTERVAL = 0.1
    CLICK_RETRY = 3
    BROWSER_DOWNLOAD_DIR = different_os_path("/tmp/browser_downloads")
    TEST_FILES_DIR = 'test_files'
    TEMPORARY_FILES_DIR = 'temporary_files'


class Logging:
    """Настройки логгирования"""
    BASE_TEST_DIR = different_os_path('/tmp/selenium_tests')
    TEST_LOG_FILE_NAME = 'test.log'
    SCREENSHOT_FILE_NAME = 'failure.png'
    BROWSER_LOG_FILE_NAME = 'browser.log'
    LOGGER_NAME = 'mytarget_test'


class Url:
    """Ссылки"""
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
    DASHBOARD = BASE + _PATHS["dashboard"]
    SEGMENTS = BASE + _FULL_PATHS["segments"]
    SEGMENT_CREATING = SEGMENTS + "/new"
    BILLING = BASE + _PATHS["billing"]
    STATISTICS = BASE + _PATHS["statistics"]
    PRO = BASE + _PATHS["pro"]
    PROFILE = BASE + _PATHS["profile"]
    TOOLS = BASE + _PATHS["tools"]
    HELP = BASE + _PATHS["help"]

    NEW_CAMPAIGN = BASE + _FULL_PATHS["new_campaign"]


class User:
    """Данные о пользователе"""
    LOGIN = "tebivan222@bombaya.com"
    PASSWORD = "Qwerty123456"
    USERNAME = "Тестов Тест Тестович"
    PHONE = "+70000000000"
