import allure
import re

from app.pages.base_page import BasePage
from app.locators.about_app import AboutAppPageLocators


class AboutAppPage(BasePage):
    locators = AboutAppPageLocators

    def is_opened(self):
        return self.check.is_visible(self.locators.TOOLBAR, raise_exception=False)

    @allure.step("Searching app version")
    def get_app_version(self):
        app_version_raw = self.find(self.locators.APP_VERSION).text
        app_version = re.findall(r"^.+? (?P<version>[\d\.]+?)$", app_version_raw)[0]
        self.logger.debug(f'App version: {app_version}')
        return app_version

    @allure.step("Searching copyright text")
    def get_about_copyright_text(self):
        copyright_text = self.find(self.locators.ABOUT_COPYRIGHT).text
        self.logger.debug(f"Copyright text: {copyright_text}")
        return copyright_text
