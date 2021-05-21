import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.login_page import LoginPage


class BaseCase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, ui_report):
        self.driver = driver
        self.config = config
        self.logger = logger

        self.login_page: LoginPage = request.getfixturevalue("login_page")

        self.logger.debug('Initial setup done!')
