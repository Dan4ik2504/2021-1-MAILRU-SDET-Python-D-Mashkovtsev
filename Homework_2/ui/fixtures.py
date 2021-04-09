import errno
import json
import logging
import os

import pytest
import allure

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from api.client import ApiClient
from ui.pages.main_page_no_auth import MainPageNoAuth
from ui.pages.dashboard_page import DashboardPage
from ui.pages.nav_panel import NavPanel
import settings

logger = logging.getLogger(settings.Logging.LOGGER_NAME)


@pytest.fixture(scope='session')
@allure.step('Getting authorization cookies')
def cookies(config):
    api_client = ApiClient()
    api_client.post_login()
    return api_client.cookies_list


@pytest.fixture(scope='function')
@allure.step("Authorization")
def login(driver, cookies, ui_report):
    logger.info("Authorization")

    log_msg = 'Getting the start page'
    logger.info(log_msg)
    with allure.step(log_msg):
        driver.get(settings.Url.BASE)

    log_msg = 'Setting cookies'
    logger.info(log_msg)
    with allure.step(log_msg):
        for cookie in cookies:
            driver.add_cookie(cookie)

    log_msg = 'Dashboard page opening'
    logger.info(log_msg)
    with allure.step(log_msg):
        dashboard_page = DashboardPage(driver=driver)
        dashboard_page.open_page()
        return dashboard_page


@pytest.fixture(scope='function')
def main_page_no_auth(driver):
    return MainPageNoAuth(driver=driver)


@pytest.fixture(scope='function')
def nav_panel(driver):
    return NavPanel(driver=driver)


class UnsupportedBrowserType(Exception):
    pass


@allure.step('Creating "{browser_name}" driver')
def get_driver(config, browser_name='chrome', download_dir=settings.Basic.BROWSER_DOWNLOAD_DIR,
               page_load_strategy=None):
    selenoid = config['selenoid']
    vnc = config['vnc']

    if browser_name == 'chrome':
        options = ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": download_dir})
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
                caps['version'] = settings.Selenoid.CHROME_DEFAULT_VERSION_VNC
                caps["selenoid:options"]["enableVNC"] = True
            else:
                caps['version'] = settings.Selenoid.CHROME_LATEST

            browser = webdriver.Remote(selenoid, options=options, desired_capabilities=caps)
            logger.info(f'Chrome driver for remote launch created. Chrome version: "{caps["version"]}"')
        else:
            chrome_version = 'latest'
            manager = ChromeDriverManager(version=chrome_version)
            browser = webdriver.Chrome(executable_path=manager.install(), options=options)
            logger.info(f'Chrome driver for local launch created. Chrome version: "{chrome_version}"')

        logger.debug(f'Browser download dir: {download_dir}')
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
        raise UnsupportedBrowserType(f'Unsupported browser: "{browser_name}"')


@pytest.fixture(scope='function')
def driver(config, test_dir):
    browser_name = config['browser']

    browser = get_driver(config, browser_name, download_dir=settings.Basic.BROWSER_DOWNLOAD_DIR)

    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', params=['chrome', 'firefox'])
def all_drivers(config, request, test_dir):
    browser = get_driver(config, request.param, download_dir=settings.Basic.BROWSER_DOWNLOAD_DIR)

    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function')
def ui_report(driver, request, test_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(test_dir, settings.Logging.SCREENSHOT_FILE_NAME)
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, settings.Logging.SCREENSHOT_FILE_NAME,
                           attachment_type=allure.attachment_type.PNG)

        browser_logfile = os.path.join(test_dir, settings.Logging.BROWSER_LOG_FILE_NAME)
        with open(browser_logfile, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n\n")

        with open(browser_logfile, 'r') as f:
            allure.attach(f.read(), settings.Logging.BROWSER_LOG_FILE_NAME, attachment_type=allure.attachment_type.TEXT)
