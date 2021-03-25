import pytest

from ui.pages.base_page_no_auth import BasePageNoAuth
from ui.pages.main_page_no_auth import MainPageNoAuth
from ui.pages.base_page_auth import BasePageAuth
from ui.pages.profile_page import ProfilePage


class BaseCaseNoAuth:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, base_page_no_auth, main_page_no_auth, base_page_auth, profile_page):
        self.driver = driver
        self.base_page_no_auth: BasePageNoAuth = base_page_no_auth
        self.main_page_no_auth: MainPageNoAuth = main_page_no_auth
        self.base_page_auth: BasePageAuth = base_page_auth
        self.profile_page: ProfilePage = profile_page


class BaseCaseAuth(BaseCaseNoAuth):
    @pytest.fixture(scope='function', autouse=True)
    def login(self, setup):
        self.main_page_no_auth.login()
