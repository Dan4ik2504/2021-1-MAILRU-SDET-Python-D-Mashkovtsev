from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page import BasePage
from ui.pages.nav_panel import NavPanel
from ui.locators import pages_locators

import settings


class BasePageAuth(BasePage):
    locators = pages_locators.BasePageAuth

    def __init__(self, driver):
        super().__init__(driver)
        self.nav_panel = NavPanel(self)


