from selenium.webdriver.support import expected_conditions as EC

import settings
from ui.pages.base_page_auth import BasePageAuth
from ui.locators import pages_locators


class ProfilePage(BasePageAuth):
    locators = pages_locators.ProfilePage

    def change_contacts_info_data(self, locator, text):
        """Заполняет поле формы для редактирования контактной информации и подтверждает изменения"""
        element = self.fill_field(locator, text)
        self.click(self.locators.CONFIRM_CHANGES_BUTTON)
        self.wait().until(EC.visibility_of_element_located(self.locators.SUCCESS_VIEW))
        return element
