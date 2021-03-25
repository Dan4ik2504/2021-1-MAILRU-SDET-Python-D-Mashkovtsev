from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import settings
from ui.pages.base_page_no_auth import BasePageNoAuth
from ui.locators import pages_locators


class BasePageAuth(BasePageNoAuth):
    """Базовый объект страниц, отображающихся после авторизации"""

    locators = pages_locators.BasePageAuth

    class LogoutException(Exception):
        """Пользователь авторизован"""

    def __init__(self, driver):
        super().__init__(driver)
        header = self.NavPanel(self)

    class NavPanel:
        def __init__(self, page):
            self.page = page

    def logout(self):
        """Выход из аккаунта"""
        self.open_page(settings.DASHBOARD_URL)
        self.click(self.locators.HEADER_USER_MENU_BUTTON)
        self.click(self.locators.HEADER_USER_MENU_LOGOUT_BUTTON)

    def is_authorized(self, open_new_tab=True):
        """Проверка того, что пользователь авторизован"""

        def check_func(self, open_new_tab=True, *args, **kwargs):
            if open_new_tab:
                self.open_page()
                self.wait().until(EC.url_changes(settings.BASE_URL))
            if self.driver.current_url != settings.DASHBOARD_URL:
                raise self.LoginException("{} != {}", self.driver.current_url, settings.DASHBOARD_URL)
            return True

        return self.checking_in_new_tab_wrapper(check_func, open_new_tab=open_new_tab)