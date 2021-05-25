import settings
from ui.pages.base_page import BasePage
from ui.locators import main_page_locators


class MainPage(BasePage):
    URL = settings.APP_SETTINGS.URLS.MAIN
    locators = main_page_locators
