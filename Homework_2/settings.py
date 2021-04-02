class Basic:
    """Основные настройки"""
    DEFAULT_TIMEOUT = 10
    DEFAULT_CHECKING_INTERVAL = 0.1
    CLICK_RETRY = 3
    SELENIUM_DRIVER_DOWNLOAD_DIR = "/opt/WebDriver/bin/"
    TEST_FILES_DIR = 'test_files'
    TEMPORARY_FILES_DIR = 'temporary_files'


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
    EMAIL = "qwertyuiop@bombaya.com"

class Js_code:
    is_visible = """
    function isVisible(elem) {
        if (!(elem instanceof Element)) throw Error('DomUtil: elem is not an element.');
        const style = getComputedStyle(elem);
        if (style.display === 'none') return false;
        if (style.visibility !== 'visible') return false;
        if (style.opacity < 0.1) return false;
        if (elem.offsetWidth + elem.offsetHeight + elem.getBoundingClientRect().height +
            elem.getBoundingClientRect().width === 0) {
            return false;
        }
        const elemCenter   = {
            x: elem.getBoundingClientRect().left + elem.offsetWidth / 2,
            y: elem.getBoundingClientRect().top + elem.offsetHeight / 2
        };
        if (elemCenter.x < 0) return false;
        if (elemCenter.x > (document.documentElement.clientWidth || window.innerWidth)) return false;
        if (elemCenter.y < 0) return false;
        if (elemCenter.y > (document.documentElement.clientHeight || window.innerHeight)) return false;
        let pointContainer = document.elementFromPoint(elemCenter.x, elemCenter.y);
        do {
            if (pointContainer === elem) return true;
        } while (pointContainer = pointContainer.parentNode);
        return false;
    }
    return isVisible(arguments[0]);
    """