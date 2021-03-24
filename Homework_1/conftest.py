import pytest
from selenium import webdriver

import settings


@pytest.fixture(scope='function')
def driver():
    with webdriver.Chrome(executable_path=settings.DRIVER_PATH) as driver:
        driver.maximize_window()
        yield driver
