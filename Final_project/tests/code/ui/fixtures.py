import logging
import os

import pytest
import allure

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

import settings
import exceptions
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage

logger = logging.getLogger(settings.TESTS.LOGGER_NAME)


@pytest.fixture(scope='function')
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture(scope='function')
def main_page(driver):
    return MainPage(driver=driver)


@allure.step('Creating "{browser_name}" driver')
def get_driver(config, browser_name='chrome',  page_load_strategy=None):
    selenoid = config['selenoid']
    vnc = config['vnc']

    if browser_name == 'chrome':
        options = ChromeOptions()
        if page_load_strategy:
            options.page_load_strategy = page_load_strategy

        if selenoid is not None:
            caps = {'browserName': browser_name,
                    'platform': 'ANY',
                    "selenoid:options": {
                        "enableVNC": False,
                        "enableVideo": False
                    }
                    }

            if vnc:
                caps['version'] = settings.SELENOID.CHROME_DEFAULT_VERSION_VNC
                caps["selenoid:options"]["enableVNC"] = True
            else:
                caps['version'] = settings.SELENOID.CHROME_LATEST

            browser = webdriver.Remote(selenoid, options=options, desired_capabilities=caps)
            logger.info(f'Chrome driver for remote launch created. Chrome version: "{caps["version"]}"')
        else:
            chrome_version = 'latest'
            manager = ChromeDriverManager(version=chrome_version)
            browser = webdriver.Chrome(executable_path=manager.install(), options=options)
            logger.info(f'Chrome driver for local launch created. Chrome version: "{chrome_version}"')

        if page_load_strategy:
            logger.debug(f'Page loading strategy: "{page_load_strategy}"')
        else:
            logger.debug('Page loading strategy: "normal"')

        return browser

    elif browser_name == 'firefox':
        if selenoid:
            logger.warning('Sorry, but there is no way to launch Firefox remotely yet')
        firefox_version = 'latest'
        manager = GeckoDriverManager(version=firefox_version, log_level=0)
        browser = webdriver.Firefox(executable_path=manager.install())
        logger.info(f'Firefox driver for local launch created. Firefox version: "{firefox_version}"')
        return browser
    else:
        raise exceptions.UnsupportedBrowserType(f'Unsupported browser: "{browser_name}"')


@pytest.fixture(scope='function')
def driver(config, test_dir):
    browser_name = config['browser']

    browser = get_driver(config, browser_name)

    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', params=['chrome', 'firefox'])
def all_drivers(config, request, test_dir):
    browser = get_driver(config, request.param)

    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def ui_report(driver, request, test_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, settings.BROWSER.SCREENSHOT_FILE_NAME)
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, settings.BROWSER.SCREENSHOT_FILE_NAME,
                           attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, settings.BROWSER.LOG_FILE_NAME)
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), settings.BROWSER.LOG_FILE_NAME, attachment_type=allure.attachment_type.TEXT)
