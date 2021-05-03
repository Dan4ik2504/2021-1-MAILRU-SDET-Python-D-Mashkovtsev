from app.locators.base_page import BasePageLocators
from appium.webdriver.common.mobileby import MobileBy as By


class AboutAppPageLocators(BasePageLocators):
    TOOLBAR = (By.ID, "ru.mail.search.electroscope:id/about_toolbar")
    APP_VERSION = (By.ID, "ru.mail.search.electroscope:id/about_version")
    ABOUT_COPYRIGHT = (By.ID, "ru.mail.search.electroscope:id/about_copyright")
