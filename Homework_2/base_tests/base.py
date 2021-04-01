import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.main_page_no_auth import MainPageNoAuth
from ui.pages.dashboard_page import DashboardPage


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.logger.debug('Initial setup done!')


class BaseCaseNoAuth(BaseCase):
    @pytest.fixture(scope='function', autouse=True)
    def setup_main_page(self, request: FixtureRequest):
        self.page: MainPageNoAuth = request.getfixturevalue("main_page_no_auth")


class BaseCaseAuth(BaseCase):
    @pytest.fixture(scope='function', autouse=True)
    def setup_login(self, request: FixtureRequest):
        self.page: DashboardPage = request.getfixturevalue("main_page_no_auth").login()
