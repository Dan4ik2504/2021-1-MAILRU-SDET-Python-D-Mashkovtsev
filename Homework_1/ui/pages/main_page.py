from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import settings
from ui.pages.base_page import BasePage
from ui.locators import pages_locators

from time import sleep


class MainPage(BasePage):
    
    locators = pages_locators.MainPage

    class LoginException(Exception):
        """Пользователь не авторизован"""

    class LogoutException(Exception):
        """Пользователь авторизован"""

    def login(self, login=settings.LOGIN, password=settings.PASSWORD):
        """Авторизация"""
        self.open_page()
        self.click(self.locators.LOGIN_BUTTON)
        self.wait().until(EC.visibility_of_element_located(self.locators.AUTH_FORM))
        self.fill_field(self.locators.EMAIL_FIELD, login)
        self.fill_field(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.LOGIN_CONFIRM_BUTTON)
        self.is_authorized(open_new_tab=False)

    def is_authorized(self, open_new_tab=True):
        """Проверка того, что пользователь авторизован"""

        def check_func(self, open_new_tab=True, *args, **kwargs):
            if open_new_tab:
                self.open_page()
                self.wait().until(EC.url_changes(settings.BASE_URL))
            if self.driver.current_url != settings.DASHBOARD_URL:
                raise self.LoginException("{} != {}", self.driver.current_url, settings.DASHBOARD_URL)
            return True

        self.checking_in_new_tab_wrapper(check_func, open_new_tab=open_new_tab)

    def is_not_authorized(self, open_new_tab=True):
        """Проверка того, что пользователь не авторизован"""

        def check_func(self, open_new_tab=True, *args, **kwargs):
            if open_new_tab:
                self.open_page()
                self.wait().until(EC.visibility_of_element_located(self.locators.LOGIN_BUTTON))
            if self.driver.current_url != settings.BASE_URL:
                raise self.LogoutException("{} != {}", self.driver.current_url, settings.BASE_URL)
            return True

        self.checking_in_new_tab_wrapper(check_func, open_new_tab=open_new_tab)
