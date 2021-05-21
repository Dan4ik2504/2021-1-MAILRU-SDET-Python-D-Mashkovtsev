from base import BaseCase
import time


class TestLoginPage(BaseCase):
    def test_test(self):
        self.login_page.open_page()
        time.sleep(10)
