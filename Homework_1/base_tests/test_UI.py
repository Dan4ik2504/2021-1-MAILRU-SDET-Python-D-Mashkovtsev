import pytest
import settings
from base_tests.base import BaseCase
from ui.locators import pages_locators
from selenium.webdriver.common.by import By


class TestLoginLogout(BaseCase):
    @pytest.mark.ui
    def test_login(self):
        self.main_page.login(checking=False)
        assert self.driver.current_url == settings.DASHBOARD_URL

    @pytest.mark.ui
    def test_logout(self):
        self.main_page.login()
        self.main_page.logout(checking=False)
        assert self.driver.current_url == settings.BASE_URL
