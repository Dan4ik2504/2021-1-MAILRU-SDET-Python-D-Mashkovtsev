import sys
import os
from utils.paths import paths


def different_os_path(path: str):
    """Changing the path to be able to work on different operating systems"""
    if sys.platform.startswith('win'):
        return "".join(("C:\\tests", path.replace("/", "\\")))
    return path


class Basic:
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
        "appActivity": "ru.mail.search.electroscope.ui.activity.AssistantActivity",
        "app": os.path.abspath(os.path.join(paths.repo_root, Basic.TEST_FILES_DIR, App.NAME)),
        "orientation": "PORTRAIT"
    }
    VERSION = '1.20'


class Logging:
    BASE_TEST_DIR = different_os_path('/tmp/selenium_tests')
    TEST_LOG_FILE_NAME = 'test.log'
    SCREENSHOT_FILE_NAME = 'failure.png'
    LOGGER_NAME = 'marussia_android_app_test'
    ALLURE_ENVIRONMENT_PROPERTIES_DICT = {
        'Appium': Appium.VERSION,
        'Android_emulator': Device.VERSION,
        'App': App.NAME,
    }
