import allure
from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page_auth import BasePageAuth
from ui.locators import pages_locators
import settings


class DashboardPage(BasePageAuth):
    URL = settings.Url.DASHBOARD
    locators = pages_locators.Dashboard

    def is_loaded(self):
        if super(DashboardPage, self).is_loaded() and \
                EC.invisibility_of_element_located(self.locators.PAGE_LOADING_SPINNER):
            return True
        return False

