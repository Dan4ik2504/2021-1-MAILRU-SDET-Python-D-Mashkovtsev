import datetime
import os
import random
from time import sleep

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
    def test_login_negative__wrong_login_or_password(self, login, password):
        login_page = self.main_page.login(login=login, password=password, checking=True,
                                          raise_error_if_login_failed=False)
        assert isinstance(login_page, LoginPage)
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
    def test_login_form_negative__incorrect_login(self, login):
        main_page = self.main_page.login(login=login, password=random_values.get_random_letters(),
                                         checking=True, raise_error_if_login_failed=False)
        assert isinstance(main_page, MainPageNoAuth)
        elem = main_page.find(main_page.locators.FORM_ERROR)
        main_page.wait_until_elem_text_changes(elem, '')
        assert elem.text in ("Введите email или телефон", "Please input email or mobile phone number")


class TestCampaigns(BaseCase):
    @pytest.mark.UI
    def test_creating_campaign(self, repo_root):
        self.new_campaign_page: NewCampaignPage = self.dashboard_page.go_to_create_campaign_page()
        self.new_campaign_page.wait_until_load()
        assert self.driver.current_url == self.new_campaign_page.URL
        self.new_campaign_page.select_goal('traffic')
        self.new_campaign_page.change_url(random_values.get_random_letters() + ".ru")
        campaign_name = random_values.get_random_letters()
        self.new_campaign_page.change_campaign_name(campaign_name)
        self.new_campaign_page.select_sex(male=True, female=False)

        date_from = datetime.datetime.now()
        date_to = date_from + datetime.timedelta(days=30)
        self.new_campaign_page.select_date(fr=date_from, to=date_to)

        budget_per_day = str(random.randint(50, 1000) * 100)
        budget_total = str(random.randint(1000, 100000) * 100)
        self.new_campaign_page.select_budget(per_day=budget_per_day, total=budget_total)

        self.new_campaign_page.select_banner_format("multiformat")
        self.new_campaign_page.load_image(repo_root=repo_root, img_name='Image1.jpg', small_img_name='Image2.jpg',
                                          icon_name='Image3.jpg')

        self.new_campaign_page.set_banner_title(random_values.get_random_letters())
        self.new_campaign_page.set_banner_text(random_values.get_random_letters(80))
        self.new_campaign_page.set_banner_about_company(random_values.get_random_letters(100))
        self.new_campaign_page.set_banner_name(random_values.get_random_letters())
        self.new_campaign_page.save_banner()

        self.new_campaign_page.save_campaign()
        assert self.dashboard_page.is_opened()
        campaigns = self.dashboard_page.get_all_campaigns()

        assert campaign_name in campaigns


class TestSegments(BaseCase):
    @pytest.mark.UI
    def test_create_segment(self):
        self.segments_page: SegmentsPage = self.nav_panel.go_to_segments()
        self.segments_page.wait_until_load()
        assert self.segments_page.URL == self.segments_page.driver.current_url.rstrip('/')

        segment_name = random_values.get_random_letters()
        with self.segments_page.new_segment as segment:
            assert self.segments_page.new_segment.URL == self.segments_page.driver.current_url.rstrip('/')
            segment.select_segment_type(segment.TYPES.APPS)
            segment.name = segment_name
        assert self.segments_page.URL == self.segments_page.driver.current_url.rstrip('/')

        all_segments = self.segments_page.segments_table.get_segments()
        assert segment_name in all_segments

    @pytest.mark.UI
    def test_delete_segment(self):
        self.segments_page: SegmentsPage = self.nav_panel.go_to_segments()
        self.segments_page.wait_until_load()
        assert self.segments_page.URL == self.segments_page.driver.current_url.rstrip('/')

        segment_name = random_values.get_random_letters()
        with self.segments_page.new_segment as segment:
            assert self.segments_page.new_segment.URL == self.segments_page.driver.current_url.rstrip('/')
            segment.select_segment_type(segment.TYPES.APPS)
            segment.name = segment_name
        assert self.segments_page.URL == self.segments_page.driver.current_url.rstrip('/')

        all_segments = self.segments_page.segments_table.get_segments()
        assert segment_name in all_segments

        segment_object = None
        for sgm in all_segments:
            if sgm.name == segment_name:
                segment_object = sgm
                break

        segment_object.remove()

        all_segments = self.segments_page.segments_table.get_segments()
        assert segment_name not in all_segments
