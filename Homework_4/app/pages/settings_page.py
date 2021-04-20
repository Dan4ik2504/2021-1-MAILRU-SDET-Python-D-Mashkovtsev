import allure

from app.pages.base_page import BasePage
from app.locators.settings_page import SettingsPageLocators
from app.pages.news_sources_setup_page import NewsSourcesSetupPage


class SettingsPage(BasePage):
    locators = SettingsPageLocators

    def is_opened(self):
        return self.check.is_visible(self.locators.TOOLBAR, raise_exception=False)

    @allure.step("Opening the news sources setup page")
    def go_to_news_sources_setup_page(self):
        news_sources_btn = self.swipe_to_element(locator=self.locators.SETTING_NEWS_SOURCES)
        news_sources_btn.click()
        news_sources_setup_page = NewsSourcesSetupPage(self.driver)
        news_sources_setup_page.custom_wait(news_sources_setup_page.is_opened)
        self.logger.info("News sources setup page is open")
        return news_sources_setup_page
