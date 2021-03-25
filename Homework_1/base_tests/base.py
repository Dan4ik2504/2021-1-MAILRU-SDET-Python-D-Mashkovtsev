import pytest
from ui.pages.base_page_no_auth import BasePageNoAuth
from ui.pages.main_page_no_auth import MainPageNoAuth


class BaseCaseNoAuth:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, base_page_no_auth, main_page_no_auth):
        self.driver = driver
        self.base_page_no_auth: BasePageNoAuth = base_page_no_auth
        self.main_page_no_auth: MainPageNoAuth = main_page_no_auth
