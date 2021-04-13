from ui.pages.base_page_no_auth import BasePageNoAuth
from ui.locators import pages_locators

import settings


class LoginPage(BasePageNoAuth):
    URL = settings.Url.LOGIN
    locators = pages_locators.LoginPage
