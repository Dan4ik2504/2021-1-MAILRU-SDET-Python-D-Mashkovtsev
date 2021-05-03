import os
from utils.paths import paths


class Basic:
    DEFAULT_TIMEOUT = 10
    DEFAULT_CHECKING_INTERVAL = 0.1
    CLICK_RETRY = 3
    MAX_SWIPES = 5
    DEFAULT_SWIPE_TIME_MS = 200
    DEFAULT_INDENT_PERCENT = 0.2
    TEST_FILES_DIR = 'files'
    TEMPORARY_FILES_DIR = 'temporary_files'
    APP_PATH = os.path.abspath(os.path.join(TEST_FILES_DIR, "Marussia_v1.39.1.apk"))


class App:
    NAME = "Marussia_v1.39.1.apk"


class Device:
    VERSION = '8.1'


class Appium:
    URL = 'http://127.0.0.1:4723/wd/hub'
    DESIRED_CAPS = {
        "platformName": "Android",
        "platformVersion": "8.1",
        "automationName": "Appium",
        "appPackage": "ru.mail.search.electroscope",
        "appActivity": ".ui.activity.AssistantActivity",
        "app": os.path.abspath(os.path.join(paths.repo_root, Basic.TEST_FILES_DIR, App.NAME)),
        "orientation": "PORTRAIT",
        "autoGrantPermissions": True
    }
    VERSION = '1.20'


class Logging:
    BASE_TEST_DIR_LINUX = '/tmp/selenium_tests'
    BASE_TEST_DIR_WINDOWS = 'C:\\tmp\\selenium_tests'
    TEST_LOG_FILE_NAME = 'test.log'
    SCREENSHOT_FILE_NAME = 'failure.png'
    LOGGER_NAME = 'marussia_android_app_test'
    ALLURE_ENVIRONMENT_PROPERTIES_DICT = {
        'Appium': Appium.VERSION,
        'Android_emulator': Device.VERSION,
        'App': App.NAME,
    }
