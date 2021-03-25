import pytest
import settings
from base_tests.base import BaseCaseNoAuth, BaseCaseAuth
from ui.locators import pages_locators
from selenium.webdriver.common.by import By


class TestLoginLogout(BaseCaseNoAuth):
    @pytest.mark.ui
    def test_login(self):
        self.main_page_no_auth.login(checking=False)
        assert self.driver.current_url == settings.DASHBOARD_URL

    @pytest.mark.ui
    def test_logout(self):
        self.main_page_no_auth.login()
        self.main_page_no_auth.logout(checking=False)
        assert self.driver.current_url == settings.BASE_URL
