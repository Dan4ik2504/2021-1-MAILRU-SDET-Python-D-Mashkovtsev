import pytest
from selenium import webdriver
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage

import settings


@pytest.fixture(scope='function')
def driver():
    with webdriver.Chrome(executable_path=settings.DRIVER_PATH) as driver:
        driver.maximize_window()
        yield driver


@pytest.fixture(scope='function')
def base_page(driver):
    return BasePage(driver=driver)
