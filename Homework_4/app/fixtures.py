import os

from appium import webdriver
import pytest
import allure
import settings
from app.pages.base_page import BasePage
from app.pages.assistant_page import AssistantPage


@pytest.fixture(scope='function')
def base_page(driver):
    return BasePage(driver)


@pytest.fixture(scope='function')
def assistant_page(driver):
    return AssistantPage(driver)


@allure.step('Creating driver. Remote URL: {appium_url}')
def get_driver(appium_url):
    desired_caps = settings.Appium.DESIRED_CAPS
    driver = webdriver.Remote(appium_url, desired_capabilities=desired_caps)
    return driver


@pytest.fixture(scope='function')
def driver(config):
    appium_url = config['appium_url']
    browser = get_driver(appium_url)
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
