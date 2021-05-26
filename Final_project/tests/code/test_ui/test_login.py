import time
import pytest
from selenium.webdriver.common.keys import Keys
import string
import textwrap

import settings
from test_ui.base import BaseUICase
import tests_data
from utils.random_values import random_equal_values as rand_val_eq


class TestLoginPage(BaseUICase):
    authorize = False

    def test_go_to_register_page(self):
        self.login_page.click(self.login_page.locators.REGISTER_PAGE_LINK)
        self.register_page.wait_until.is_page_opened()
        assert self.register_page.check.is_page_url_match_driver_url()

    def do_incorrect_login(self, username, password):
        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username, password)
            self.login_page.wait_until.is_page_url_match_driver_url()
            assert self.login_page.get_error_text() == tests_data.LoginPage.ErrorMsgs.INVALID_DATA

    def test_login_form__positive(self):
        user = self.users_builder.generate_user()
        self.login_page.login(user.username, user.password)
        self.main_page.wait_until.is_page_opened()

    def test_login_form__invalid_data(self):
        username = self.fake.username
        password = self.fake.password
        self.do_incorrect_login(username, password)

    def test_login_form__invalid_username(self):
        username, fake_username = self.fake.username, self.fake.username
        user = self.users_builder.generate_user(username=username)
        self.do_incorrect_login(fake_username, user.password)

    def test_login_form__invalid_password(self):
        password, fake_password = self.fake.password, self.fake.password
        user = self.users_builder.generate_user(password=password)
        self.do_incorrect_login(user.username, fake_password)

    @pytest.mark.parametrize(
        ('username', 'password'),
        (
                ('', ''),
                ('', rand_val_eq.password),
                (rand_val_eq.username, '')
        )
    )
    def test_login_form__empty_data(self, username, password):
        with self.login_page.is_page_not_reloaded__context_manager():
            self.login_page.login(username, password)
            self.login_page.wait_until.is_page_url_match_driver_url()
            assert self.login_page.check.is_not_visible(self.login_page.locators.ERROR_TEXT)

    @pytest.mark.parametrize(
        'username',
        (
                [rand_val_eq.get_random_letters_and_digits(i) for i in [1, 5, 17, 50, 100]]
         )
    )
    def test_login_form__incorrect_username_length(self, username):
        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username=username, password=self.fake.password)
            assert self.login_page.get_error_text() == tests_data.LoginPage.ErrorMsgs.INCORRECT_USERNAME_LENGTH

    @pytest.mark.parametrize(
        'password',
        (
                [rand_val_eq.get_random_letters_and_digits(i) for i in [1, 5, 17, 50, 100]]
         )
    )
    def test_login_form__password_length(self, password):
        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username=self.fake.username, password=password)
            assert self.login_page.get_error_text() == tests_data.LoginPage.ErrorMsgs.INVALID_DATA

    def test_login_form__incorrect_empty_username(self):
        username = Keys.SPACE
        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username=username, password=self.fake.password)
            assert self.login_page.get_error_text() == tests_data.LoginPage.ErrorMsgs.USERNAME_NOT_SPECIFIED

    def test_login_form__incorrect_empty_password(self):
        password = Keys.SPACE
        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username=self.fake.username, password=password)
            assert self.login_page.get_error_text() == tests_data.LoginPage.ErrorMsgs.PASSWORD_NOT_SPECIFIED

    @pytest.mark.parametrize(
        'data',
        textwrap.fill(string.punctuation, 16).split('\n')
    )
    def test_login_form__incorrect_symbols(self, data):
        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username=data, password=data)
            assert self.login_page.get_error_text() == tests_data.LoginPage.ErrorMsgs.INVALID_DATA

    def test_login_form__sql_injection(self):
        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username='a OR 1=1', password='a OR 1=1')
            assert self.login_page.check.is_page_opened()
            assert self.login_page.get_error_text() == tests_data.LoginPage.ErrorMsgs.INVALID_DATA

    @pytest.mark.parametrize(
        ('username', 'username_err', 'password', 'password_err'),
        (
                (
                        Keys.SPACE,
                        tests_data.LoginPage.ErrorMsgs.USERNAME_NOT_SPECIFIED,
                        Keys.SPACE,
                        tests_data.LoginPage.ErrorMsgs.PASSWORD_NOT_SPECIFIED
                ),
                (
                        rand_val_eq.get_random_letters_and_digits(5),
                        tests_data.LoginPage.ErrorMsgs.INCORRECT_USERNAME_LENGTH,
                        Keys.SPACE,
                        tests_data.LoginPage.ErrorMsgs.PASSWORD_NOT_SPECIFIED
                )
        )
    )
    def test_login_form__two_errors(self, username, username_err, password, password_err):
        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username=username, password=password)
            self.login_page.wait_until.is_page_url_match_driver_url()
            assert self.login_page.get_error_text() == f'{username_err}\n{password_err}'


class TestAccessToPagesWithoutLogin(BaseUICase):
    authorize = False
    auto_open_page = False

    def test_no_login__access_login_page(self):
        self.login_page.open_page()
        assert self.login_page.check.is_page_url_match_driver_url()

    def test_no_login__access_login_page_2(self):
        self.login_page.open_page(url=settings.APP_SETTINGS.URL)
        assert self.login_page.current_url.path == '/'

    def test_no_login__access_register_page(self):
        self.register_page.open_page()
        assert self.register_page.check.is_page_url_match_driver_url()

    def test_no_login__access_main_page(self):
        self.main_page.open_page(check_page_is_open=False)
        self.login_page.wait_until.is_page_opened()
        assert self.login_page.current_url.args['next'] == settings.APP_SETTINGS.URLS.MAIN
        assert self.login_page.get_error_text() == tests_data.LoginPage.ErrorMsgs.NOT_AUTHORIZED


class TestAccessToPageWithLogin(BaseUICase):
    authorize = True
    auto_open_page = False

    def test_login__access_login_page(self):
        self.login_page.open_page()
        self.main_page.wait_until.is_page_opened()
        assert self.main_page.check.is_page_url_match_driver_url()

    def test_login__access_login_page_2(self):
        self.login_page.open_page(url=settings.APP_SETTINGS.URL)
        self.main_page.wait_until.is_page_opened()
        assert self.main_page.check.is_page_url_match_driver_url()

    def test_login__access_register_page(self):
        self.register_page.open_page()
        self.main_page.wait_until.is_page_opened()
        assert self.main_page.check.is_page_url_match_driver_url()

    def test_login__access_main_page(self):
        self.main_page.open_page()
        assert self.main_page.check.is_page_url_match_driver_url()
