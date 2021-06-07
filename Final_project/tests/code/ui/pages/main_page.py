import allure

import exceptions
import settings
from ui.locators import main_page_locators
from ui.pages.base_page import BasePage


class MainPage(BasePage):
    URL = settings.APP_SETTINGS.URLS.MAIN
    locators = main_page_locators

    @allure.step("Searching for VK ID in header")
    def get_vk_id(self):
        try:
            vk_id = self.get_elem_text(self.locators.VK_ID_TEXT)
        except exceptions.FindingException:
            vk_id = ''
        self.logger.info(f"VK ID in header: {vk_id}")
        return vk_id

    @allure.step("Searching for username in header")
    def get_username(self):
        try:
            username = self.get_elem_text(self.locators.USERNAME_TEXT)
        except exceptions.FindingException:
            username = ''
        self.logger.info(f"Username in header: {username}")
        return username

    def open_navbar_dropdown(self, target_locator):
        if target_locator in self.locators.HEADER_NAVBAR_DEPENDENCIES:
            btn_locator = self.locators.HEADER_NAVBAR_DEPENDENCIES[target_locator]
            self.hover_over_element(btn_locator)
            self.wait_until.is_visible(target_locator)

    def click_on_navbar_dropdown_item(self, locator):
        if not self.check.is_visible(locator):
            self.open_navbar_dropdown(locator)
        self.click(locator)
