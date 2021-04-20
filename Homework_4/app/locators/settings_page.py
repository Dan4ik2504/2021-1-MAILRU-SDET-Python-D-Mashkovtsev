from app.locators.base_page import BasePageLocators
from appium.webdriver.common.mobileby import MobileBy as By


class SettingsPageLocators(BasePageLocators):
    TOOLBAR = (By.ID, "ru.mail.search.electroscope:id/user_settings_toolbar")
    SETTING_NEWS_SOURCES = (By.ID, "ru.mail.search.electroscope:id/user_settings_field_news_sources")
