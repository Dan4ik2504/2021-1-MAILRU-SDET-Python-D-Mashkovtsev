class Basic:
    """Основные настройки"""
    DEFAULT_TIMEOUT = 10
    DEFAULT_CHECKING_INTERVAL = 0.1
    CLICK_RETRY = 3
    SELENIUM_DRIVER_DOWNLOAD_DIR = "/opt/WebDriver/bin/"


class Logging:
    """Настройки логгирования"""
    BASE_TEST_DIR = '/tmp/selenium_tests'
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
    }

    LOGIN = "https://account.my.com/login"
    DASHBOARD = BASE + _PATHS["dashboard"]
    SEGMENTS = BASE + _FULL_PATHS["segments"]
    BILLING = BASE + _PATHS["billing"]
    STATISTICS = BASE + _PATHS["statistics"]
    PRO = BASE + _PATHS["pro"]
    PROFILE = BASE + _PATHS["profile"]
    TOOLS = BASE + _PATHS["tools"]
    HELP = BASE + _PATHS["help"]


class User:
    """Данные о пользователе"""
    LOGIN = "tebivan222@bombaya.com"
    PASSWORD = "Qwerty123456"
    USERNAME = "Тестов Тест Тестович"
    PHONE = "+70000000000"
    EMAIL = "qwertyuiop@bombaya.com"
