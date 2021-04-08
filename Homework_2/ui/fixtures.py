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
        dashboard_page.stop_page_loading()
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


def get_driver(browser_name='chrome', download_dir=settings.Basic.BROWSER_DOWNLOAD_DIR, page_load_strategy=None):
    if browser_name == 'chrome':
        options = ChromeOptions()
        options.add_experimental_option("prefs", {"download.default_directory": download_dir})
        if page_load_strategy:
            options.page_load_strategy = page_load_strategy

        manager = ChromeDriverManager(version='latest')
        browser = webdriver.Chrome(executable_path=manager.install(), options=options)
        return browser
    elif browser_name == 'firefox':
        manager = GeckoDriverManager(version='latest', log_level=0)
        browser = webdriver.Firefox(executable_path=manager.install())
        return browser
    else:
        raise UnsupportedBrowserType(f'Unsupported browser {browser_name}')


@pytest.fixture(scope='function')
def driver(config, test_dir):
    browser_name = config['browser']

    browser = get_driver(browser_name, download_dir=settings.Basic.BROWSER_DOWNLOAD_DIR)

    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture(scope='function', params=['chrome', 'firefox'])
def all_drivers(config, request, test_dir):
    browser = get_driver(request.param, download_dir=settings.Basic.BROWSER_DOWNLOAD_DIR)

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
