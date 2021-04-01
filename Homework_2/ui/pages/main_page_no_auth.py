import allure

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page_no_auth import BasePageNoAuth
from ui.pages.login_page import LoginPage
from ui.locators import pages_locators

import settings


class MainPageNoAuth(BasePageNoAuth):
    """Объект страницы, отображающейся до авторизации"""
    URL = settings.Url.BASE
    locators = pages_locators.MainPageNoAuth

    class LoginError(Exception):
        pass

    def login(self, login=settings.User.LOGIN, password=settings.User.PASSWORD, checking=True,
              raise_error_if_login_failed=True):
        """Авторизация"""
        allure.step(f"Login ({login})")
        if self.driver.current_url != settings.Url.BASE:
            self.open_page()

        self.click(self.locators.LOGIN_BUTTON)
        self.wait().until(EC.visibility_of_element_located(self.locators.AUTH_FORM))
        self.fill_field(self.locators.EMAIL_FIELD, login)
        self.fill_field(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.LOGIN_CONFIRM_BUTTON)

        if checking:
            if settings.Url.DASHBOARD in self.driver.current_url:
                allure.step(f"Page opened: {self.driver.current_url}")
                return
            else:
                if raise_error_if_login_failed:
                    raise self.LoginError("Login failed")
                else:
                    if settings.Url.BASE == self.driver.current_url:
                        return self
                    elif settings.Url.LOGIN in self.driver.current_url:
                        allure.step(f"Page opened: {self.driver.current_url}")
                        return LoginPage(self.driver)
                    else:
                        raise self.LoginError(f"Login failed. \
                        Current url does not matches login page: {self.driver.current_url} != {settings.Url.LOGIN}")
