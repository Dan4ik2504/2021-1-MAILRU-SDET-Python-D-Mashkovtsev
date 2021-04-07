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
    """Object of the page with the form for creating a new campaign"""
    URL = settings.Url.NEW_CAMPAIGN
    locators = pages_locators.NewCampaign
    GOALS = {
        "traffic": locators.BUTTON_GOAL_TRAFFIC,
    }
    BANNERS = {
        "multiformat": locators.MULTIFORMAT_BANNER_FORMAT_ITEM_BUTTON,
    }

    def __init__(self, dashboard_page, driver):
        super().__init__(driver)
        self.dashboard_page = dashboard_page

    def is_opened(self):
        elems = self.find_elements(self.locators.PAGE_LOADING_SPINNER)
        try:
            result = [self.check.is_element_visible(elem, raise_exception=False) for elem in elems]
        except StaleElementReferenceException:
            return False
        if len(result) > 1 and not any(result):
            self.logger.info("New campaign page opened")
            return True

    @allure.step('Selecting campaign goal: "{goal}"')
    def select_goal(self, goal):
        self.click(self.GOALS[goal])
        self.logger.info(f'Goal selected: {goal}')

    def open_setting(self, setting_locator, setting_wrapper_locator):
        if self.check.is_not_visible(setting_locator, raise_exception=False):
            self.click(setting_wrapper_locator)
            self.logger.info(f'Setting "{setting_locator[1]}" (type: {setting_locator[0]}) wrapper is opened')

    @allure.step('Changing campaign URL: "{url}"')
    def change_url(self, url):
        self.fill_field(self.locators.INPUT_URL, url)
        self.logger.info(f'Url rewrited in field: "{url}"')

    @allure.step('Setting up targeting - sex. Female: "{female}". Male: "{male}"')
    def select_sex(self, female=True, male=True):
        self.open_setting(self.locators.SEX_CHECKBOX_MALE, self.locators.SEX_WRAPPER_BUTTON)
        if not female:
            self.click(self.locators.SEX_CHECKBOX_FEMALE)
            self.logger.info(f'Selected female sex')
        if not male:
            self.click(self.locators.SEX_CHECKBOX_MALE)
            self.logger.info(f'Selected male sex')

    @allure.step('Changing campaign name: "{name}"')
    def change_campaign_name(self, name):
        self.fill_field(self.locators.INPUT_CAMPAIGN_NAME, name)
        self.logger.info(f'Campaign name changed: "{name}"')

    def select_date(self, fr: datetime.datetime, to: datetime.datetime):
        fr_formatted = fr.strftime('%d.%m.%Y')
        to_formatted = to.strftime('%d.%m.%Y')
        with allure.step(f'Setting up targeting - campaign date. From: "{fr_formatted}". To: "{to_formatted}"'):
            self.open_setting(self.locators.DATE_FROM_INPUT, self.locators.DATE_WRAPPER_BUTTON)
            self.fill_field(self.locators.DATE_FROM_INPUT, fr_formatted)
            self.fill_field(self.locators.DATE_TO_INPUT, to_formatted)
            self.logger.info(f'Date selected. From: "{fr_formatted}". To: "{to_formatted}"')

    @allure.step('Changing campaign budget. Per day: "{per_day}". Total: "{total}"')
    def select_budget(self, per_day, total):
        self.open_setting(self.locators.BUDGET_PER_DAY_INPUT, self.locators.BUDGET_WRAPPER_BUTTON)
        self.fill_field(self.locators.BUDGET_PER_DAY_INPUT, per_day)
        self.fill_field(self.locators.BUDGET_TOTAL_INPUT, total)
        self.logger.info(f'Budget selected. Per day: "{per_day}". Total: "{total}"')

    @allure.step('Changing advertisement format: {banner_format}')
    def select_banner_format(self, banner_format):
        self.click(self.BANNERS[banner_format])
        self.logger.info(f'Banner format selected: "{banner_format}"')

    @allure.step('Creating campaign banner - images loading. Main image name: "{img_name}". '
                 'Small image name: "{small_img_name}". Icon name: "{icon_name}"')
    def load_image(self, repo_root, img_name=None, small_img_name=None, icon_name=None,
                   test_files_dir=settings.Basic.TEST_FILES_DIR):
        for img, locator in zip((img_name, small_img_name, icon_name),
                                (self.locators.BANNER_IMAGE_INPUT, self.locators.BANNER_SMALL_IMAGE_INPUT,
                                 self.locators.BANNER_ICON_INPUT)):
            image_input = self.find(locator)
            log_msg = f'Uploading image "{img}" into "{locator[1]}" (type: {locator[0]})'
            with allure.step(log_msg):
                self.dashboard_page.logger.info(log_msg)
                image_input.send_keys(os.path.join(repo_root, test_files_dir, img))
                self.click(self.locators.BANNER_IMAGE_SAVING_SUBMIT_BUTTON)
                self.logger.info(f'Image "{img_name}" uploaded into "{locator[1]}" (type: {locator[0]})')

    @allure.step('Creating campaign banner - changing banner title: "{text}"')
    def set_banner_title(self, text):
        self.fill_field(self.locators.BANNER_TITLE_INPUT, text)
        self.logger.info(f'Banner title written: "{text}"')

    @allure.step('Creating campaign banner - changing banner text: "{text}"')
    def set_banner_text(self, text):
        self.fill_field(self.locators.BANNER_TEXT_INPUT, text)
        self.logger.info(f'Banner title written: "{text}"')

    @allure.step('Creating campaign banner - changing banner info about company: "{text}"')
    def set_banner_about_company(self, text):
        self.fill_field(self.locators.BANNER_ABOUT_COMPANY_INPUT, text)
        self.logger.info(f'Banner about company field written: "{text}"')

    @allure.step('Creating campaign banner - changing banner name: "{text}"')
    def set_banner_name(self, text):
        self.fill_field(self.locators.BANNER_NAME_INPUT, text)
        self.logger.info(f'Banner name written: "{text}"')

    @allure.step('Creating campaign banner - saving banner')
    def save_banner(self):
        self.click(self.locators.BANNER_SAVE_INPUT)
        self.logger.info('Banner saved')

    @allure.step('Campaign saving')
    def save_campaign(self):
        self.click(self.locators.SUBMIT_BUTTON)
        self.dashboard_page.custom_wait(self.dashboard_page.check.is_page_opened)
        self.logger.info('Campaign saved')
