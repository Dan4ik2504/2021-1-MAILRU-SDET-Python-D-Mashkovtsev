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

    def is_opened(self):
        spinner_locator = self.locators.PAGE_LOADING_SPINNER
        if not self.check.is_exists(spinner_locator, raise_exception=False):
            return True
        raise self.check.PageNotOpenedException(f"Spinner exists: {spinner_locator[1]} (type: {spinner_locator[0]})")

    def go_to_create_campaign_page(self):
        create_campaign_btns = (self.locators.CREATE_CAMPAIGN_BUTTON, self.locators.CREATE_CAMPAIGN_INSTRUCTION_LINK)
        for locator in create_campaign_btns:
            if self.check.is_visible(locator, raise_exception=False):
                self.click(locator)
                break
        new_campaign_page = NewCampaignPage(self, driver=self.driver)
        new_campaign_page.custom_wait(new_campaign_page.check.is_page_opened)
        return new_campaign_page

    def get_all_campaigns(self):
        return [n.text for n in self.driver.find_elements(*self.locators.CAMPAIGN_NAME)]
