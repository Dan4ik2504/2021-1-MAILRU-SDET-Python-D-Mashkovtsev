import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.main_page_no_auth import MainPageNoAuth

class BaseCaseNoAuth:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        self.driver = driver
        self.main_page_no_auth: MainPageNoAuth = request.getfixturevalue("main_page_no_auth")