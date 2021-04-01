import allure

from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page_no_auth import BasePageNoAuth
from ui.locators import pages_locators

import settings


class MainPageNoAuth(BasePageNoAuth):
    """Объект страницы, отображающейся до авторизации"""
    URL = settings.Url.BASE
    locators = pages_locators.MainPageNoAuth

    @allure.step("Login: {login}")
    def login(self, login=settings.User.LOGIN, password=settings.User.PASSWORD):
        """Авторизация"""
        if self.driver.current_url != settings.Url.BASE:
            self.open_page()
        self.click(self.locators.LOGIN_BUTTON)
        self.wait().until(EC.visibility_of_element_located(self.locators.AUTH_FORM))
        self.fill_field(self.locators.EMAIL_FIELD, login)
        self.fill_field(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.LOGIN_CONFIRM_BUTTON)
        self.wait().until(EC.url_changes(settings.Url.BASE))
