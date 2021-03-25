import pytest
from selenium import webdriver
from ui.pages.base_page_no_auth import BasePageNoAuth
from ui.pages.main_page_no_auth import MainPageNoAuth

import settings


@pytest.fixture(scope='function')
def driver():
    with webdriver.Chrome(executable_path=settings.DRIVER_PATH) as driver:
        driver.maximize_window()
        yield driver


@pytest.fixture(scope='function')
def base_page_no_auth(driver):
    return BasePageNoAuth(driver=driver)


@pytest.fixture(scope='function')
def main_page_no_auth(driver):
    return MainPageNoAuth(driver=driver)
