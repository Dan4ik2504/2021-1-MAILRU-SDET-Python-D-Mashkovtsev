import allure

import exceptions
from ui.pages.base_page import BasePage
from ui.locators import login_page_locators
import settings


class LoginPage(BasePage):
    URL = settings.APP_SETTINGS.URLS.LOGIN
    locators = login_page_locators

    @allure.step("Login. Username: {username}. Password: {password}")
    def login(self, username, password):
        self.logger.info(f"Login. Username: {username}. Password: {password}")
        self.fill_field(self.locators.USERNAME_FIELD, username)
        self.fill_field(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.CONFIRM_BUTTON)

    @allure.step("Getting form error text")
    def get_error_text(self):
        self.logger.info("Getting form error text")
        self.wait_until.is_visible(self.locators.ERROR_TEXT)
        try:
            text = self.get_elem_text(self.locators.ERROR_TEXT)
        except exceptions.FindingException:
            return None
        self.logger.info(f"Form error text: {text}")
        return text
