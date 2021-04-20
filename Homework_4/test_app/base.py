import pytest
from _pytest.fixtures import FixtureRequest
from app.pages.base_page import BasePage
from appium.webdriver.webdriver import WebDriver

class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest, logger, ui_report):
        self.driver: WebDriver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePage = request.getfixturevalue("base_page")

        self.logger.debug('Initial setup done!')