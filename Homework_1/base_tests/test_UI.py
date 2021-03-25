import pytest
import settings
from base_tests.base import BaseCase
from ui.locators import pages_locators
from selenium.webdriver.common.by import By


class TestUI(BaseCase):
    @pytest.mark.ui
    def test_login(self):
        self.main_page.login()
