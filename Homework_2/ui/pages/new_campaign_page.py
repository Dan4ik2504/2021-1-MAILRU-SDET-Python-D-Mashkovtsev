import os

import allure
import datetime

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from ui.pages.base_page_auth import BasePageAuth
from ui.locators import pages_locators
import settings

from time import sleep


class NewCampaignPage(BasePageAuth):
    URL = settings.Url.NEW_CAMPAIGN
    locators = pages_locators.NewCampaign
    GOALS = {
        "traffic": locators.BUTTON_GOAL_TRAFFIC,
    }
    BANNERS = {
        "multiformat": locators.MULTIFORMAT_BANNER_FORMAT_ITEM_BUTTON,
    }

    def __init__(self, driver, DashboardClass):
        super().__init__(driver)
        self.DashboardClass = DashboardClass

    def is_loaded(self):
        if super(NewCampaignPage, self).is_loaded():
            elems = self.driver.find_elements(*self.locators.PAGE_LOADING_SPINNER)
            try:
                result = [self.elem_is_visible(r) for r in elems]
            except StaleElementReferenceException:
                return False
            if len(result) > 1 and not any(result):
                return True
        return False

    def select_goal(self, goal):
        self.click(self.GOALS[goal])

    def open_setting(self, setting_locator, setting_wrapper_locator):
        if self.is_not_visible(setting_locator):
            self.click(setting_wrapper_locator)

    def select_sex(self, female=True, male=True):
        self.open_setting(self.locators.SEX_CHECKBOX_MALE, self.locators.SEX_WRAPPER_BUTTON)
        if not female:
            self.click(self.locators.SEX_CHECKBOX_FEMALE)
        if not male:
            self.click(self.locators.SEX_CHECKBOX_MALE)

    def change_url(self, url):
        self.fill_field(self.locators.INPUT_URL, url)

    def change_campaign_name(self, name):
        self.fill_field(self.locators.INPUT_CAMPAIGN_NAME, name)

    def select_date(self, fr: datetime.datetime, to: datetime.datetime):
        self.open_setting(self.locators.DATE_FROM_INPUT, self.locators.DATE_WRAPPER_BUTTON)
        self.fill_field(self.locators.DATE_FROM_INPUT, fr.strftime('%d.%m.%Y'))
        self.fill_field(self.locators.DATE_TO_INPUT, to.strftime('%d.%m.%Y'))

    def select_budget(self, per_day, total):
        self.open_setting(self.locators.BUDGET_PER_DAY_INPUT, self.locators.BUDGET_WRAPPER_BUTTON)
        self.fill_field(self.locators.BUDGET_PER_DAY_INPUT, per_day)
        self.fill_field(self.locators.BUDGET_TOTAL_INPUT, total)

    def select_banner_format(self, format):
        self.click(self.BANNERS[format])

    def load_image(self, repo_root, img_name=None, small_img_name=None, icon_name=None,
                   test_files_dir=settings.Basic.TEST_FILES_DIR):
        for img, locator in zip((img_name, small_img_name, icon_name),
                                (self.locators.BANNER_IMAGE_INPUT, self.locators.BANNER_SMALL_IMAGE_INPUT,
                                 self.locators.BANNER_ICON_INPUT)):
            if img:
                image_input = self.find(locator)
                image_input.send_keys(os.path.join(repo_root, test_files_dir, img))
                self.click(self.locators.BANNER_IMAGE_SAVING_SUBMIT_BUTTON)

    def set_banner_title(self, text):
        self.fill_field(self.locators.BANNER_TITLE_INPUT, text)

    def set_banner_text(self, text):
        self.fill_field(self.locators.BANNER_TEXT_INPUT, text)

    def set_banner_about_company(self, text):
        self.fill_field(self.locators.BANNER_ABOUT_COMPANY_INPUT, text)

    def set_banner_name(self, text):
        self.fill_field(self.locators.BANNER_NAME_INPUT, text)

    def save_banner(self):
        self.click(self.locators.BANNER_SAVE_INPUT)

    def save_campaign(self):
        self.click(self.locators.SUBMIT_BUTTON)
        self.wait().until(EC.url_changes(self.URL))
        return self.DashboardClass(driver=self.driver)