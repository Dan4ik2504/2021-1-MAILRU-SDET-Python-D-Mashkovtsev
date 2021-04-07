import datetime
import os
import random
from time import sleep
import allure

import pytest

from selenium.webdriver.support import expected_conditions as EC

from base_tests.base import BaseCase
from ui.locators import pages_locators
from ui.pages.login_page import LoginPage
from ui.pages.main_page_no_auth import MainPageNoAuth
from ui.pages.new_campaign_page import NewCampaignPage
from ui.pages.segments_page import SegmentsPage

from utils import random_values
import settings


class TestLogin(BaseCase):
    authorize = False

    @pytest.mark.UI
    @allure.title("Positive login test")
    def test_login_positive(self):
        self.main_page.login()
        assert self.driver.current_url == settings.Url.DASHBOARD

    @pytest.mark.parametrize(
        ("login", "password"),
        (
                (pytest.lazy_fixture("random_email"), pytest.lazy_fixture("random_password")),
                (pytest.lazy_fixture("random_phone_number"), pytest.lazy_fixture("random_password")),
                (pytest.lazy_fixture("random_email"), settings.User.PASSWORD),
                (settings.User.LOGIN, pytest.lazy_fixture("random_password")),
        )
    )
    @pytest.mark.UI
    @allure.title('Negative login test with wrong login or password. Login: "{login}". Password: "{password}"')
    def test_login_negative__wrong_login_or_password(self, login, password):
        with allure.step('Login with wrong data'):
            login_page = self.main_page.login(login=login, password=password, checking=True,
                                              raise_error_if_login_failed=False)
            assert isinstance(login_page, LoginPage)

        with allure.step('Searching for a login form error message about invalid data'):
            assert settings.Url.LOGIN in self.driver.current_url
            assert login_page.find(login_page.locators.LOGIN_MSG_TITLE).text in ("Error", "Ошибка")
            assert login_page.find(login_page.locators.LOGIN_MSG_TEXT).text in ("Invalid login or password",
                                                                                "Неверный логин или пароль")

    @pytest.mark.parametrize(
        "login",
        (
                pytest.lazy_fixture("random_incorrect_login"),
                "mail@mail",
                "mail@.ru",
                "@mail.ru",
                "@mail",
                "@.ru",
                "mail.ru",
        )
    )
    @pytest.mark.UI
    @allure.title('Negative login test with incorrect login and random password. Login: "{login}"')
    def test_login_form_negative__incorrect_login(self, login):
        with allure.step('Login with incorrect data'):
            main_page = self.main_page.login(login=login, password=random_values.get_random_letters(),
                                             checking=True, raise_error_if_login_failed=False)
            assert isinstance(main_page, MainPageNoAuth)

        with allure.step('Searching for a login form error message about invalid data'):
            elem = main_page.find(main_page.locators.FORM_ERROR)
            main_page.custom_wait(main_page.check.is_element_text_not_equal, elem, '')
            assert elem.text in ("Введите email или телефон", "Please input email or mobile phone number")


class TestCampaigns(BaseCase):
    @allure.step("Opening new campaign page")
    def open_new_campaign_page(self):
        new_campaign_page: NewCampaignPage = self.dashboard_page.go_to_create_campaign_page()
        new_campaign_page.custom_wait(new_campaign_page.check.is_page_opened)
        assert self.driver.current_url == new_campaign_page.URL
        return new_campaign_page

    @allure.step("Creating campaign")
    def create_campaign(self, new_campaign_page, repo_root):
        with allure.step("Filling out the form on the campaign creation page"):
            new_campaign_page.select_goal('traffic')
            new_campaign_page.change_url(random_values.get_random_letters() + ".ru")
            campaign_name = random_values.get_random_letters()
            new_campaign_page.change_campaign_name(campaign_name)
            new_campaign_page.select_sex(male=True, female=False)

            date_from = datetime.datetime.now()
            date_to = date_from + datetime.timedelta(days=30)
            new_campaign_page.select_date(fr=date_from, to=date_to)

            budget_per_day = str(random.randint(50, 1000) * 100)
            budget_total = str(random.randint(1000, 100000) * 100)
            new_campaign_page.select_budget(per_day=budget_per_day, total=budget_total)

            with allure.step('Creating campaign banner'):
                new_campaign_page.select_banner_format("multiformat")
                new_campaign_page.load_image(repo_root=repo_root, img_name='Image1.jpg', small_img_name='Image2.jpg',
                                             icon_name='Image3.jpg')

                new_campaign_page.set_banner_title(random_values.get_random_letters())
                new_campaign_page.set_banner_text(random_values.get_random_letters(80))
                new_campaign_page.set_banner_about_company(random_values.get_random_letters(100))
                new_campaign_page.set_banner_name(random_values.get_random_letters())

                new_campaign_page.save_banner()

        with allure.step('Submitting campaign creation'):
            new_campaign_page.save_campaign()
            self.dashboard_page.custom_wait(self.dashboard_page.check.is_page_opened)

        return campaign_name

    @allure.step('Verifying that the campaign "{campaign_name}" has been created')
    def verify_campaign_creation(self, new_campaign_page, campaign_name):
        campaigns = self.dashboard_page.get_all_campaigns()
        assert campaign_name in campaigns
        return campaigns

    @pytest.mark.UI
    @allure.title("Campaign creation test")
    def test_creating_campaign(self, repo_root):
        new_campaign_page = self.open_new_campaign_page()
        campaign_name = self.create_campaign(new_campaign_page, repo_root)
        self.verify_campaign_creation(new_campaign_page, campaign_name)


class TestSegments(BaseCase):
    @allure.step("Opening segments page")
    def open_segments_page(self):
        segments_page: SegmentsPage = self.nav_panel.go_to_segments()
        assert segments_page.check.is_page_url_match_driver_url()
        return segments_page

    @allure.step('Creating a segment')
    def create_segment(self, segments_page):
        segment_name = random_values.get_random_letters()
        with segments_page.new_segment as segment:
            assert segments_page.new_segment.URL == segments_page.driver.current_url.rstrip('/')
            segment.select_segment_type(segment.TYPES.APPS)
            segment.name = segment_name
        assert segments_page.check.is_page_url_match_driver_url()

        return segment_name

    @allure.step('Verifying that the segment "{segment_name}" has been created')
    def verify_segment_creation(self, segments_page, segment_name):
        all_segments = segments_page.segments_table.get_segments()
        assert segment_name in all_segments
        return all_segments

    @pytest.mark.UI
    @allure.title("Segment creation test")
    def test_create_segment(self):
        segments_page = self.open_segments_page()
        segment_name = self.create_segment(segments_page)
        self.verify_segment_creation(segments_page, segment_name)

    @pytest.mark.UI
    @allure.title("Segment deletion test")
    def test_delete_segment(self):
        segments_page = self.open_segments_page()
        segment_name = self.create_segment(segments_page)
        all_segments = self.verify_segment_creation(segments_page, segment_name)

        with allure.step(f'Removing segment "{segment_name}"'):
            with allure.step(f'Segment search'):
                segment_object = None
                for sgm in all_segments:
                    if sgm.name == segment_name:
                        segment_object = sgm
                        break

                assert segment_object

            segment_object.remove()

        with allure.step(f'Verifying that the segment "{segment_name}" has been deleted'):
            all_segments = segments_page.segments_table.get_segments()
            assert segment_name not in all_segments
