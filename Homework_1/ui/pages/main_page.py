from selenium.webdriver.support import expected_conditions as EC

import settings
from ui.pages.base_page import BasePage
from ui.locators import pages_locators

from time import sleep


class MainPage(BasePage):
    def login(self, login=settings.LOGIN, password=settings.PASSWORD):
        """Авторизация"""
        self.open_page()
        self.click(pages_locators.MainPage.LOGIN_BUTTON)
        self.wait().until(EC.visibility_of_element_located(pages_locators.MainPage.AUTH_FORM))
        self.fill_field(pages_locators.MainPage.EMAIL_FIELD, login)
        self.fill_field(pages_locators.MainPage.PASSWORD_FIELD, password)
        self.click(pages_locators.MainPage.LOGIN_CONFIRM_BUTTON)
        self.driver.execute_script("window.open('');")
        self.driver.execute_script("window.open('');")
        self.is_authorised()

    def is_authorised(self):
        """Проверка того, что пользователь авторизован"""
        original_tab = self.driver.current_window_handle
        self.driver.execute_script("window.open('');")
        new_tab = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_tab)
        self.open_page()
        self.wait().until(EC.url_changes(settings.BASE_URL))
        assert self.driver.current_url == settings.DASHBOARD_URL
        assert self.find(pages_locators.Dashboard.HEADER_USERNAME).text == settings.USERNAME.upper()
        self.driver.close()
        self.driver.switch_to.window(original_tab)
