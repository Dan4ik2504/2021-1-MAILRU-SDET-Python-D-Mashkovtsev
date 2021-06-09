import allure

import exceptions
import settings
from ui.locators import register_page_locators
from ui.pages.base_page import BasePage


class RegisterPage(BasePage):
    URL = settings.APP_SETTINGS.URLS.REGISTRATION
    locators = register_page_locators

    @allure.step("Register. Username: {username}. Email: {email}. Password: {password}")
    def register(self, username, email, password, repeat_password=None, sdet=True):
        self.logger.info(
            f"Register. Username: {username}. Email: {email}. Password: {password}. "
            f"Repeat password: {repeat_password}. SDET: {sdet}")
        self.fill_field(self.locators.USERNAME_FIELD, username)
        self.fill_field(self.locators.EMAIL_FIELD, email)
        self.fill_field(self.locators.PASSWORD_FIELD, password)

        if repeat_password is None:
            repeat_password = password
        self.fill_field(self.locators.REPEAT_PASSWORD_FIELD, repeat_password)

        if sdet:
            self.click(self.locators.SDET_CHECKBOX)

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
