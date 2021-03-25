from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import settings
from ui.pages.base_page_no_auth import BasePageNoAuth
from ui.locators import pages_locators

from time import sleep


class MainPageNoAuth(BasePageNoAuth):
    """Объект страницы, отображающейся до авторизации"""
    
    locators = pages_locators.MainPageNoAuth

    class LoginException(Exception):
        """Пользователь не авторизован"""

    class LogoutException(Exception):
        """Пользователь авторизован"""

    def login(self, login=settings.LOGIN, password=settings.PASSWORD, checking=True):
        """Авторизация"""
        self.open_page()
        self.click(self.locators.LOGIN_BUTTON)
        self.wait().until(EC.visibility_of_element_located(self.locators.AUTH_FORM))
        self.fill_field(self.locators.EMAIL_FIELD, login)
        self.fill_field(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.LOGIN_CONFIRM_BUTTON)
        if checking:
            self.is_authorized(open_new_tab=False)

    def logout(self, checking=True):
        """Выход из аккаунта"""
        self.open_page(settings.DASHBOARD_URL)
        self.click(pages_locators.BasePageAuth.HEADER_USER_MENU_BUTTON)
        self.click(pages_locators.BasePageAuth.HEADER_USER_MENU_LOGOUT_BUTTON)
        if checking:
            self.is_not_authorized(open_new_tab=False)

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
