import pytest
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, base_page, main_page):
        self.driver = driver
        self.base_page: BasePage = base_page
        self.main_page: MainPage = main_page
