import allure

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page_no_auth import BasePageNoAuth
from ui.pages.dashboard_page import DashboardPage
from ui.pages.login_page import LoginPage
from ui.locators import pages_locators

import settings


class MainPageNoAuth(BasePageNoAuth):
    """The object of the page displayed before authorization"""
    URL = settings.Url.BASE
    locators = pages_locators.MainPageNoAuth

    class LoginError(Exception):
        pass

    @allure.step('Login "{login}"')
    def login(self, login=settings.User.LOGIN, password=settings.User.PASSWORD, checking=True,
              raise_error_if_login_failed=True):
        """Authorization"""
        self.logger.info(f'Login "{login}"')
        if self.driver.current_url != settings.Url.BASE:
            self.open_page()

        log_msg = 'Filling out the login form'
        self.logger.info('Filling out the login form')
        with allure.step(log_msg):
            self.click(self.locators.LOGIN_BUTTON)
            self.wait().until(EC.visibility_of_element_located(self.locators.AUTH_FORM))
            self.fill_field(self.locators.EMAIL_FIELD, login)
            self.fill_field(self.locators.PASSWORD_FIELD, password)

        log_msg = 'Login confirmation'
        self.logger.info(log_msg)
        with allure.step(log_msg):
            self.click(self.locators.LOGIN_CONFIRM_BUTTON)

        if checking:
            log_msg = f'Login validation'
            self.logger.info(log_msg)
            with allure.step(log_msg):
                if settings.Url.DASHBOARD in self.driver.current_url:
                    log_msg = 'Redirection to dashboard page'
                    with allure.step(log_msg):
                        self.logger.info(log_msg)
                        dashboard_page = DashboardPage(driver=self.driver)
                        dashboard_page.custom_wait(dashboard_page.check.is_page_opened)
                        return dashboard_page
                else:
                    if raise_error_if_login_failed:
                        raise self.LoginError("Login failed")
                    else:
                        log_msg = 'Login failed'
                        self.logger.info(log_msg)
                        if settings.Url.BASE == self.driver.current_url:
                            self.logger.info("Login form validation failed")
                            return self
                        elif settings.Url.LOGIN in self.driver.current_url:
                            self.logger.info("Login data validation failed. Redirect to login page")
                            return LoginPage(driver=self.driver)
                        else:
                            raise self.LoginError(f"Login failed. \
                            Current url does not matches login page: {self.driver.current_url} != {settings.Url.LOGIN}")
