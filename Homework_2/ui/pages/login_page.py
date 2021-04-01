import allure

from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page_no_auth import BasePageNoAuth
from ui.locators import pages_locators

import settings


class LoginPage(BasePageNoAuth):
    locators = pages_locators.LoginPage
