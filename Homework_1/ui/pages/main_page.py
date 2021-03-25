from selenium.webdriver.support import expected_conditions as EC

import settings
from ui.pages.base_page import BasePage
from ui.locators import pages_locators


class MainPage(BasePage):
    def login(self, login=settings.LOGIN, password=settings.PASSWORD):
        """Авторизация"""
        self.open_page()
        self.click(pages_locators.MainPage.LOGIN_BUTTON)
        self.wait().until(EC.visibility_of_element_located(pages_locators.MainPage.AUTH_FORM))
        self.fill_field(pages_locators.MainPage.EMAIL_FIELD, login)
        self.fill_field(pages_locators.MainPage.PASSWORD_FIELD, password)
        self.click(pages_locators.MainPage.LOGIN_CONFIRM_BUTTON)
        self.wait().until(EC.url_changes(settings.BASE_URL))
        assert self.driver.current_url == settings.DASHBOARD_URL
