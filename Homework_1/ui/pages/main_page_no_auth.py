from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page import BasePage
from ui.locators import pages_locators

import settings


class MainPageNoAuth(BasePage):
    """Объект страницы, отображающейся до авторизации"""
    
    locators = pages_locators.MainPageNoAuth

    class LoginException(Exception):
        """Пользователь не авторизован"""

    def login(self, login=settings.LOGIN, password=settings.PASSWORD):
        """Авторизация"""
        self.open_page()
        self.click(self.locators.LOGIN_BUTTON)
        self.wait().until(EC.visibility_of_element_located(self.locators.AUTH_FORM))
        self.fill_field(self.locators.EMAIL_FIELD, login)
        self.fill_field(self.locators.PASSWORD_FIELD, password)
        self.click(self.locators.LOGIN_CONFIRM_BUTTON)
        self.wait().until(EC.url_changes(settings.BASE_URL))

    def is_not_authorized(self, open_new_tab=True):
        """Проверка того, что пользователь не авторизован"""

        def check_func(self, open_new_tab=True, *args, **kwargs):
            if open_new_tab:
                self.open_page()
                self.wait().until(EC.visibility_of_element_located(self.locators.LOGIN_BUTTON))
            if self.driver.current_url != settings.BASE_URL:
                raise self.LogoutException("{} != {}", self.driver.current_url, settings.BASE_URL)
            return True

        return self.checking_in_new_tab_wrapper(check_func, open_new_tab=open_new_tab)
