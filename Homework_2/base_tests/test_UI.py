import pytest

from selenium.webdriver.support import expected_conditions as EC

from base_tests.base import BaseCaseNoAuth
from ui.locators import pages_locators
from ui.pages.login_page import LoginPage
from ui.pages.main_page_no_auth import MainPageNoAuth

from utils import random_string
import settings


class TestLogin(BaseCaseNoAuth):
    @pytest.mark.UI
    def test_login_positive(self):
        self.main_page_no_auth.login()
        assert self.driver.current_url == settings.Url.DASHBOARD

    @pytest.mark.parametrize(
        ("login", "password"),
        (
                (random_string.get_random_email(), random_string.get_random_letters_and_digits()),
                (random_string.get_random_phone_number(), random_string.get_random_letters_and_digits()),
                (random_string.get_random_email(), settings.User.PASSWORD),
                (settings.User.LOGIN, random_string.get_random_letters_and_digits()),
        )
    )
    @pytest.mark.UI
    def test_login_negative__wrong_login_or_password(self, login, password):
        login_page = self.main_page_no_auth.login(login=login, password=password, checking=True,
                                                  raise_error_if_login_failed=False)
        assert isinstance(login_page, LoginPage)
        assert settings.Url.LOGIN in self.driver.current_url
        assert login_page.find(login_page.locators.LOGIN_MSG_TITLE).text in ("Error", "Ошибка")
        assert login_page.find(login_page.locators.LOGIN_MSG_TEXT).text in ("Invalid login or password",
                                                                            "Неверный логин или пароль")

    @pytest.mark.parametrize(
        "login",
        (
                random_string.get_random_letters(),
                random_string.get_random_phone_number() + random_string.get_random_letters(1),
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
        main_page = self.main_page_no_auth.login(login=login, password=random_string.get_random_letters(),
                                                 checking=True, raise_error_if_login_failed=False)
        assert isinstance(main_page, MainPageNoAuth)
        elem = main_page.find(main_page.locators.FORM_ERROR)
        main_page.wait_until_elem_text_changes(elem, '')
        assert elem.text in ("Введите email или телефон", "Please input email or mobile phone number")
