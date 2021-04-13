import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.main_page_no_auth import MainPageNoAuth
from ui.pages.dashboard_page import DashboardPage
from ui.pages.nav_panel import NavPanel


class BaseCase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, ui_report):
        self.driver = driver
        self.config = config
        self.logger = logger

        if self.authorize:
            self.dashboard_page: DashboardPage = request.getfixturevalue("login")
            self.nav_panel: NavPanel = request.getfixturevalue("nav_panel")
        else:
            self.main_page: MainPageNoAuth = request.getfixturevalue("main_page_no_auth")
            self.main_page.open_page()

        self.logger.debug('Initial setup done!')
