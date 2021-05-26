import settings
from ui.pages.base_page import BasePage
from ui.locators import register_page_locators


class RegisterPage(BasePage):
    URL = settings.APP_SETTINGS.URLS.REGISTRATION
    locators = register_page_locators