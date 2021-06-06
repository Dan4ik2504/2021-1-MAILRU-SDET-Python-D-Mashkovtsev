import pytest
from _pytest.fixtures import FixtureRequest

import settings
from api.myapp_api import MyappApi
from db.vk_api_client import VkApiDBClient
from db.myapp_client import MyappDBClient
from db.builder import VkApiBuilder, UserBuilder
from ui.pages.base_page import BasePage
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.register_page import RegisterPage
from utils.random_values import random_different_values


class BaseUICase:
    authorize = True
    auto_open_page = True
    current_user = None
    seleniumwire_pages = False

    def do_login(self):
        self.myapp_api.api.headers['User-Agent'] = self.login_page.user_agent

        user = self.users_builder.generate_user()
        self.current_user = user
        self.myapp_api.login(user.username, user.password)

        cookies = self.myapp_api.api.cookies_list
        self.login_page.open_page()
        for cookie in cookies:
            self.login_page.driver.add_cookie(cookie)
        self.main_page.open_page()

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config, request: FixtureRequest, logger):
        self.fake = random_different_values
        self.config = config
        self.logger = logger
        self.vkapi_db: VkApiDBClient = request.getfixturevalue("vk_api_client")
        self.myapp_db: MyappDBClient = request.getfixturevalue("myapp_client")
        self.vkapi_builder = VkApiBuilder(self.vkapi_db)
        self.users_builder = UserBuilder(self.myapp_db)

        if self.seleniumwire_pages:
            driver = request.getfixturevalue("seleniumwire_driver")
            request.getfixturevalue("ui_seleniumwire_report")
        else:
            driver = request.getfixturevalue("driver")
            request.getfixturevalue('ui_report')

        self.base_page = BasePage(driver)
        self.login_page = LoginPage(driver)
        self.main_page = MainPage(driver)
        self.register_page = RegisterPage(driver)

        self.myapp_api: MyappApi = request.getfixturevalue('myapp_api')

        if self.authorize:
            self.do_login()

        else:
            if self.auto_open_page:
                self.login_page.open_page()

        self.logger.debug('Initial setup done!')
