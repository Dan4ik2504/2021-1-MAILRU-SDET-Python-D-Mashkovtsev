import allure
from selenium.webdriver.support import expected_conditions as EC

from ui.pages.base_page_auth import BasePageAuth
from ui.pages.new_campaign_page import NewCampaignPage
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from ui.locators import pages_locators
import settings


class DashboardPage(BasePageAuth):
    URL = settings.Url.DASHBOARD
    locators = pages_locators.Dashboard

    class NewCampaignPageOpenException(Exception):
        pass

    def is_opened(self):
        spinner_locator = self.locators.PAGE_LOADING_SPINNER
        if not self.check.is_exists(spinner_locator, raise_exception=False):
            self.logger.info(f'Dashboard page loaded')
            return True
        raise self.check.PageNotOpenedException(f"Spinner exists: {spinner_locator[1]} (type: {spinner_locator[0]})")

    @allure.step("Going to create campaign page")
    def go_to_create_campaign_page(self):
        """Opens a campaign page and returns an object of that page"""
        self.logger.info('Clicking on create campaign button')

        create_campaign_btns = (self.locators.CREATE_CAMPAIGN_BUTTON,
                                self.locators.CREATE_CAMPAIGN_INSTRUCTION_LINK)
        elem = None
        for locator in create_campaign_btns:
            elem = self.fast_find(locator)
            if elem and self.check.is_element_visible(elem, raise_exception=False):
                self.click(locator)
                break

        if not elem:
            self.NewCampaignPageOpenException(
                f'Unable to navigate to the page for creating a new campaign '
                f'because there is no button or link linking to it. '
                f'Checked button "{create_campaign_btns[0][1]}" (type: {create_campaign_btns[0][0]}) '
                f'and link "{create_campaign_btns[1][1]}" (type: {create_campaign_btns[1][0]})')

        self.logger.info('Opening the campaign creation page')
        new_campaign_page = NewCampaignPage(self, driver=self.driver)
        new_campaign_page.custom_wait(new_campaign_page.check.is_page_opened)
        self.logger.info(f'The campaign creation page is open')
        return new_campaign_page

    @allure.step("Search for campaigns in the table")
    def get_all_campaigns(self):
        """Returns all campaigns found in the table"""
        self.logger.info("Searching for campaigns")
        campaigns = [n.text for n in self.driver.find_elements(*self.locators.CAMPAIGN_NAME)]
        self.logger.info(f'Found {len(campaigns)} campaigns')
        self.logger.debug(f'Found {len(campaigns)} campaigns: {"; ".join(campaigns)}')
        return campaigns
