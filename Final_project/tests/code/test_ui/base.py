import pytest
from _pytest.fixtures import FixtureRequest

from db.vk_api_client import VkApiDBClient
from db.myapp_client import MyappDBClient
from db.builder import VkApiBuilder, UserBuilder
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from utils.random_values import random_different_values


class BaseUICase:
    authorize = True
    auto_open_page = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, ui_report):
        self.fake = random_different_values
        self.driver = driver
        self.config = config
        self.logger = logger
        self.vkapi_db = VkApiDBClient()
        self.myapp_db = MyappDBClient()
        self.vkapi_builder = VkApiBuilder(self.vkapi_db)
        self.users_builder = UserBuilder(self.myapp_db)

        self.login_page: LoginPage = request.getfixturevalue("login_page")
        self.main_page: MainPage = request.getfixturevalue("main_page")

        if self.auto_open_page:
            self.login_page.open_page()

        self.logger.debug('Initial setup done!')
