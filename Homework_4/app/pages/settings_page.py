import allure

from app.pages.base_page import BasePage
from app.locators.settings_page import SettingsPageLocators
from app.pages.news_sources_setup_page import NewsSourcesSetupPage
from app.pages.about_app import AboutAppPage


class SettingsPage(BasePage):
    locators = SettingsPageLocators

    def is_opened(self):
        return self.check.is_visible(self.locators.TOOLBAR, raise_exception=False)

    @allure.step("Opening the news sources setup page")
    def go_to_news_sources_setup_page(self):
        self.swipe_to_element(locator=self.locators.SETTING_NEWS_SOURCES).click()
        news_sources_setup_page = NewsSourcesSetupPage(self.driver)
        news_sources_setup_page.custom_wait(news_sources_setup_page.is_opened)
        self.logger.info("News sources setup page is open")
        return news_sources_setup_page

    @allure.step("Opening the about app page")
    def go_to_about_app_page(self):
        self.swipe_to_element(locator=self.locators.SETTING_ABOUT_APP).click()
        about_app_page = AboutAppPage(self.driver)
        about_app_page.custom_wait(about_app_page.is_opened)
        self.logger.info("About app page is open")
        return about_app_page
