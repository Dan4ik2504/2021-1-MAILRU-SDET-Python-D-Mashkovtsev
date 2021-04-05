import allure
from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page_auth import BasePageAuth
from ui.pages.new_campaign_page import NewCampaignPage
from selenium.common.exceptions import StaleElementReferenceException
from ui.locators import pages_locators
import settings


class DashboardPage(BasePageAuth):
    URL = settings.Url.DASHBOARD
    locators = pages_locators.Dashboard

    def is_loaded(self):
        spinner_locator = self.locators.PAGE_LOADING_SPINNER
        if super().is_loaded():
            if not self.is_element_exists(spinner_locator):
                return True
        raise self.PageIsNotLoadedException(f"Spinner exists: {spinner_locator[1]} (type: {spinner_locator[0]})")

    def go_to_create_campaign_page(self):
        create_campaign_btns = (self.locators.CREATE_CAMPAIGN_BUTTON, self.locators.CREATE_CAMPAIGN_INSTRUCTION_LINK)
        for locator in create_campaign_btns:
            try:
                if self.is_visible(locator):
                    self.click(locator)
                    break
            except self.ElementIsNotVisible:
                continue
        self.wait().until(EC.url_changes(self.URL))
        new_campaign_page = NewCampaignPage(driver=self.driver)
        return new_campaign_page

    def get_all_campaigns(self):
        return [n.text for n in self.driver.find_elements(*self.locators.CAMPAIGN_NAME)]
