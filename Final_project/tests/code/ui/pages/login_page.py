import exceptions
from ui.pages.base_page import BasePage
from ui.locators import login_page_locators
import settings


class LoginPage(BasePage):
    URL = settings.APP_SETTINGS.URLS.LOGIN
    locators = login_page_locators

    def login(self, username, password):
        self.fill_field(self.locators.USERNAME_FIELD, username)
        self.fill_field(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.CONFIRM_BUTTON)

    def get_error_text(self):
        self.wait_until.is_visible(self.locators.ERROR_TEXT)
        try:
            elem = self.fast_find(self.locators.ERROR_TEXT)
        except exceptions.FindingException:
            return None
        return elem.text
