import pytest
from _pytest.fixtures import FixtureRequest

import settings
from api.myapp_api import MyappApi
from db.vk_api_client import VkApiDBClient
from db.myapp_client import MyappDBClient
from db.builder import VkApiBuilder, UserBuilder
from utils.random_values import random_different_values


class BaseAPICase:
    authorize = True
    current_user = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, config, request: FixtureRequest, logger):
        self.fake = random_different_values
        self.config = config
        self.logger = logger
        self.myapp_db: MyappDBClient = request.getfixturevalue("myapp_client")
        self.users_builder = UserBuilder(self.myapp_db)

        self.myapp_api: MyappApi = request.getfixturevalue('myapp_api')

        if self.authorize:
            user = self.users_builder.generate_user()
            self.current_user = user
            self.myapp_api.login(user.username, user.password)

        self.logger.debug('Initial setup done!')
