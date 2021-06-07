import string
import textwrap
from datetime import datetime

import pytest
from selenium.webdriver.common.keys import Keys

import tests_data
from test_ui.base import BaseUICase
from utils.random_values import random_equal_values as rand_val_eq


class TestLoginPage(BaseUICase):
    authorize = False
    form_errors = tests_data.LoginPage.ErrorMsgs

    # Methods

    def do_incorrect_login(self, username, password):
        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username, password)
            self.login_page.wait_until.is_page_opened()
        assert self.login_page.get_error_text() == self.form_errors.INVALID_DATA

    # Tests

    def test_go_to_register_page(self):
        """
        Тест перехода на страницу регистрации через ссылку внизу формы

        Шаги:
        1. Клик на ссылку

        ОР: Открылась страница регистрации
        """

        self.login_page.click(self.login_page.locators.REGISTER_PAGE_LINK)
        self.register_page.wait_until.is_page_opened()

    def test_login_form__positive(self):
        """
        Позитивный тест авторизации

        Шаги:
        1. Создание пользователя
        2. Отправка формы с корректными именем и паролем

        ОР: Авторизация успешна. Открылась главная страница.
        В БД: поднят флаг активности пользователя; записано время логина
        """

        user = self.users_builder.generate_user()
        login_time = datetime.utcnow()
        self.login_page.login(user.username, user.password)
        self.main_page.wait_until.is_page_opened()
        user = self.myapp_db.get_user(username=user.username, password=user.password, email=user.email)
        assert user.access == 1
        assert user.active == 1
        assert login_time <= user.start_active_time <= datetime.utcnow()

    def test_login_form__blocked_user(self):
        """
        Тест авторизации с данными заблокированного пользователя

        Шаги:
        1. Создание заблокированного пользователя
        2. Отправка формы с корректными именем и паролем

        ОР: Отобразилось сообщение об ошибке:
        """

        user = self.users_builder.generate_user(access=0)
        self.login_page.login(user.username, user.password)
        self.login_page.wait_until.is_page_opened()
        assert self.login_page.get_error_text() == self.form_errors.BLOCKED_USER

    def test_login_form__invalid_data(self):
        """
        Негативный тест авторизации с данными несуществующего пользователя

        Шаги:
        1. Создание пользователя
        2. Отправка формы с данными несуществующего пользователя

        ОР: Отобразилось сообщение об ошибке "Неверное имя пользователя или пароль"
        """

        username = self.fake.get_username()
        password = self.fake.get_password()
        self.do_incorrect_login(username, password)

    def test_login_form__invalid_username(self):
        """
        Негативный тест авторизации с неверным именем пользователя

        Шаги:
        1. Создание пользователя
        2. Отправка формы с неверным именем пользователя

        ОР: Отобразилось сообщение об ошибке "Неверное имя пользователя или пароль"
        """

        username, fake_username = self.fake.get_username(), self.fake.get_username()
        user = self.users_builder.generate_user(username=username)
        self.do_incorrect_login(fake_username, user.password)

    def test_login_form__invalid_password(self):
        """
        Негативный тест авторизации с неверным паролем

        Шаги:
        1. Создание пользователя
        2. Отправка формы с неверным паролем

        ОР: Отобразилось сообщение об ошибке "Неверное имя пользователя или пароль"
        """

        password, fake_password = self.fake.get_password(), self.fake.get_password()
        user = self.users_builder.generate_user(password=password)
        self.do_incorrect_login(user.username, fake_password)

    @pytest.mark.parametrize(
        ('username', 'password'),
        (
                ('', ''),
                ('', rand_val_eq.get_password()),
                (rand_val_eq.get_username(), '')
        )
    )
    def test_login_form__empty_data(self, username, password):
        """
        Негативный тест отправки формы авторизации с незаполненными полями

        Шаги:
        1. Отправка формы с незаполненными полями

        ОР: Страница не перезагрузилась (т.е. POST запрос не был отправлен)
        """

        with self.login_page.is_page_not_reloaded__context_manager():
            self.login_page.login(username, password)
            self.login_page.wait_until.is_page_opened()
        assert self.login_page.check.is_not_visible(self.login_page.locators.ERROR_TEXT, raise_exception=True)

    @pytest.mark.parametrize(
        'username',
        (
                [rand_val_eq.get_random_letters_and_digits(i) for i in [1, 5, 17, 50, 100]]
        )
    )
    def test_login_form__incorrect_username_length(self, username):
        """
        Негативный тест авторизации с именем пользователя некорректной длины

        Шаги:
        1. Отправка формы с именем пользователя некорректной длины

        ОР: Отобразилось сообщение об ошибке "Некорректная длина имени пользователя"
        """

        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username=username, password=self.fake.get_password())
            self.login_page.wait_until.is_page_opened()
        assert self.login_page.get_error_text() == self.form_errors.INCORRECT_USERNAME_LENGTH

    @pytest.mark.parametrize(
        'password',
        (
                [rand_val_eq.get_random_letters_and_digits(i) for i in [1, 5, 17, 50, 100]]
        )
    )
    def test_login_form__password_length(self, password):
        """
        Тест авторизации с паролем различной длины

        Шаги:
        1. Отправка формы с паролем различной длины

        ОР: Страница перезагрузилась. Отобразилось сообщение об ошибке "Неверное имя пользователя или пароль"
        """

        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username=self.fake.get_username(), password=password)
            self.login_page.wait_until.is_page_opened()
        assert self.login_page.get_error_text() == self.form_errors.INVALID_DATA

    def test_login_form__incorrect_empty_username(self):
        """
        Негативный тест авторизации с незаполненным именем

        Шаги:
        1. Отправка формы с незаполненным именем

        ОР: Отобразилось сообщение об ошибке "Имя пользователя не определено"
        """

        username = Keys.SPACE
        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username=username, password=self.fake.get_password())
            self.login_page.wait_until.is_page_opened()
        assert self.login_page.get_error_text() == self.form_errors.USERNAME_NOT_SPECIFIED

    def test_login_form__incorrect_empty_password(self):
        """
        Негативный тест авторизации с незаполненным паролем

        Шаги:
        1. Отправка формы с незаполненным паролем

        ОР: Отобразилось сообщение об ошибке "Пароль не определен"
        """

        password = Keys.SPACE
        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username=self.fake.get_username(), password=password)
            self.login_page.wait_until.is_page_opened()
        assert self.login_page.get_error_text() == self.form_errors.PASSWORD_NOT_SPECIFIED

    @pytest.mark.parametrize(
        'data',
        textwrap.fill(string.punctuation, 16).split('\n')
    )
    def test_login_form__incorrect_symbols(self, data):
        """
        Тест авторизации с данными, содержащими некорректные символы

        Шаги:
        1. Отправка формы с данными, содержащими некорректные символы

        ОР: Отобразилось сообщение об ошибке "Неверное имя пользователя или пароль"
        """

        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username=data, password=data)
            self.login_page.wait_until.is_page_opened()
        assert self.login_page.get_error_text() == self.form_errors.INVALID_DATA

    def test_login_form__sql_injection(self):
        """
        Тест формы авторизации на защиту от SQL-инъекций

        Шаги:
        1. Отправка формы с данными, содержащими SQL-инъекцию

        ОР: Отобразилось сообщение об ошибке "Неверное имя пользователя или пароль". SQL инъекция не сработала
        """

        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username='a OR 1=1', password='a OR 1=1')
            self.login_page.wait_until.is_page_opened()
        assert self.login_page.get_error_text() == self.form_errors.INVALID_DATA

    @pytest.mark.parametrize(
        ('username', 'username_err', 'password', 'password_err'),
        (
                (
                        Keys.SPACE,
                        form_errors.USERNAME_NOT_SPECIFIED,
                        Keys.SPACE,
                        form_errors.PASSWORD_NOT_SPECIFIED
                ),
                (
                        rand_val_eq.get_random_letters_and_digits(5),
                        form_errors.INCORRECT_USERNAME_LENGTH,
                        Keys.SPACE,
                        form_errors.PASSWORD_NOT_SPECIFIED
                )
        )
    )
    def test_login_form__two_errors(self, username, username_err, password, password_err):
        """
        Тест отображения нескольких сообщений об ошибках в форме авторизации

        Шаги:
        1. Отправка формы с неверными данными

        ОР: Сообщения об ошибках отобразились корректно
        """

        with self.login_page.is_page_reloaded__context_manager():
            self.login_page.login(username=username, password=password)
            self.login_page.wait_until.is_page_opened()
        assert self.login_page.get_error_text() == f'{username_err}\n{password_err}'
