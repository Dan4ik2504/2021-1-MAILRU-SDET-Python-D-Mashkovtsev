from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page import BasePage
from ui.locators import pages_locators

import settings


class BasePageAuth(BasePage):
    locators = pages_locators.BasePageAuth
