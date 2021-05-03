from app.locators.base_page import BasePageLocators
from appium.webdriver.common.mobileby import MobileBy as By


class NewsSourcesSetupPageLocators(BasePageLocators):
    TOOLBAR = (By.ID, "ru.mail.search.electroscope:id/news_sources_toolbar")
    CHECKED_SOURCE_NAME = \
        (By.XPATH, "//android.widget.FrameLayout["
                   "*[@resource-id='ru.mail.search.electroscope:id/news_sources_item_selected']]/"
                   "*[@resource-id='ru.mail.search.electroscope:id/news_sources_item_title']")
    SOURCE_BY_NAME__BASE = (By.XPATH, "//*[*[@text='{}']]")
    CHECKED_SOURCE_BY_NAME__BASE = \
        (By.XPATH, "//android.widget.FrameLayout[*[@text='{}'] and "
                   "*[@resource-id='ru.mail.search.electroscope:id/news_sources_item_title']]")
