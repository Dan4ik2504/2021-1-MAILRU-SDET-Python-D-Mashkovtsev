import allure

from app.pages.base_page import BasePage
from app.locators.news_sources_setup_page import NewsSourcesSetupPageLocators


class NewsSourcesSetupPage(BasePage):
    locators = NewsSourcesSetupPageLocators

    class SOURCES:
        NEWS_MAILRU = "Новости Mail.ru"
        VESTI_FM = "Вести FM"
        KOMMERSANT_FM = "Коммерсант FM"

    def is_opened(self):
        return self.check.is_visible(self.locators.TOOLBAR, raise_exception=False)

    @allure.step('Selecting source: "{source_name}"')
    def select_source(self, source_name: str):
        self.logger.info(f'Selecting source: "{source_name}"')
        source_btn_locator = (self.locators.SOURCE_BY_NAME__BASE[0], 
                              self.locators.SOURCE_BY_NAME__BASE[1].format(source_name))
        self.click(source_btn_locator)

        checked_source_locator = (self.locators.CHECKED_SOURCE_BY_NAME__BASE[0],
                                  self.locators.CHECKED_SOURCE_BY_NAME__BASE[1].format(source_name))
        self.custom_wait(self.check.is_visible, locator=checked_source_locator)
        self.logger.info('Source selected')


