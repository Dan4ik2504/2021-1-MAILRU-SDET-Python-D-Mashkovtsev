from itertools import product

import pytest
from selenium.webdriver.common.keys import Keys

from utils.random_values import random_equal_values as rand_val_eq
from test_api.base import BaseAPICase
from tests_data import Api as td_api


class TestMyappApiAuth(BaseAPICase):
    authorize = True
    td_api = td_api


class TestMyappApiAuthWithStatusCodeChecking(TestMyappApiAuth):
    check_status_code = True

    # Methods

    def create_user_data_and_send_post_request(self, send_username=True, send_email=True, send_password=True,
                                               expected_status=None):
        user = self.users_builder.generate_user(save_in_db=False)
        user_data = {}
        if send_username:
            user_data["username"] = user.username
        if send_email:
            user_data["email"] = user.email
        if send_password:
            user_data["password"] = user.password

        return user_data, self.myapp_api.add_user(**user_data, expected_status=expected_status)

    def select_status_code(self, status_code):
        return status_code if self.check_status_code else None

    # Tests

    @pytest.mark.xfail
    def test_api__add_user_positive(self):
        """
        Тест на создание пользователя через API

        Шаги:
        1. Создать случайные данные пользователя
        2. Отправить данные

        ОР: Код ответа: 201. Пользователь создан
        """

        user, response = self.create_user_data_and_send_post_request(
            expected_status=self.select_status_code(201))
        assert self.myapp_db.is_user_exists(**user)
        assert response.text == self.td_api.USER_ADDED

    @pytest.mark.parametrize(
        ("username", "email", "password", "erorr_msg"),
        (
                (rand_val_eq.username, rand_val_eq.email, None, td_api.CANT_ADD_USER__MISSING_PASSWORD),
                (rand_val_eq.username, None, rand_val_eq.password, td_api.CANT_ADD_USER__MISSING_EMAIL),
                (None, rand_val_eq.email, rand_val_eq.password, td_api.CANT_ADD_USER__MISSING_USERNAME),
                (None, None, None, td_api.CANT_ADD_USER__MISSING_USERNAME)
        )
    )
    def test_api__add_user__incorrect_request_json_data(self, username, email, password, erorr_msg):
        """
        Тест на отправку запроса на добавление пользователя с неполными данными

        Шаги:
        1. Отправка неполных данных пользователя

        ОР: Код ответа: 400. Пользователь не создан
        """
        response = self.myapp_api.add_user(username, email, password,
                                           expected_status=self.select_status_code(400))
        assert response.text == erorr_msg
        assert not self.myapp_db.is_user_exists(username=username, email=email, password=password)

    @pytest.mark.parametrize(
        ("username", "email", "password", "erorr_msg"),
        (
                ('', '', '', td_api.CANT_ADD_USER__MISSING_USERNAME),
                (rand_val_eq.username, rand_val_eq.email, ' ', td_api.CANT_ADD_USER__MISSING_PASSWORD),
                (rand_val_eq.username, ' ', rand_val_eq.password, td_api.CANT_ADD_USER__MISSING_EMAIL),
                (' ', rand_val_eq.email, rand_val_eq.password, td_api.CANT_ADD_USER__MISSING_USERNAME)
        )
    )
    @pytest.mark.xfail
    def test_api__add_user__empty_data(self, username, email, password, erorr_msg):
        """
        Тест на отправку запроса на добавление пользователя с неполными данными

        Шаги:
        1. Отправка неполных данных пользователя

        ОР: Код ответа: 400. Пользователь не создан
        """
        response = self.myapp_api.add_user(username, email, password,
                                           expected_status=self.select_status_code(400))
        assert response.text == erorr_msg
        assert not self.myapp_db.is_user_exists(username=username, email=email, password=password)

    def test_api__add_user_request_without_json(self):
        """
        Тест на отправку запроса на добавление пользователя без JSON

        Шаги:
        1. Отправка запроса без JSON

        ОР: Код ответа: 400
        """

        response = self.myapp_api.api.post_request(self.myapp_api.url_add_login, expected_status=400)
        assert response.text.startswith(td_api.CANT_ADD_USER)

    def test_api__add_existing_user(self):
        """
        Негативный тест добавления существующего пользователя

        Шаги:
        1. Создание нового пользователя
        2. Отправка данных этого же пользователя

        ОР: Код ответа: 304
        """

        user = self.users_builder.generate_user()
        username = user.username
        email = user.email
        password = user.password
        response = self.myapp_api.add_user(username, email, password,
                                           expected_status=self.select_status_code(304))
        assert response.text != self.td_api.USER_ADDED

    def test_api__add_existing_username(self):
        """
        Негативный тест добавления пользователя c существующим в БД именем

        Шаги:
        1. Создание нового пользователя
        2. Отправка запроса с именем этого же пользователя

        ОР: Код ответа: 304. Пользователь не создан
        """

        user = self.users_builder.generate_user()
        password = self.fake.password
        email = self.fake.email
        response = self.myapp_api.add_user(user.username, email, password,
                                           expected_status=self.select_status_code(304))
        assert response.text != self.td_api.USER_ADDED
        assert not self.myapp_db.is_user_exists(email=email, password=password)

    @pytest.mark.xfail
    def test_api__add_existing_email(self):
        """
        Негативный тест добавления пользователя c существующим в БД email

        Шаги:
        1. Создание нового пользователя
        2. Отправка запроса с email этого же пользователя

        ОР: Код ответа: 304. Пользователь не создан
        """

        user = self.users_builder.generate_user()
        username = self.fake.username
        password = self.fake.password
        response = self.myapp_api.add_user(username=username, email=user.email, password=password,
                                           expected_status=self.select_status_code(304))
        assert response.text != self.td_api.USER_ADDED
        assert not self.myapp_db.is_user_exists(username=username, password=password)

    @pytest.mark.xfail
    def test_api__add_existing_password(self):
        """
        Тест добавления пользователя c существующим в БД паролем

        Шаги:
        1. Создание нового пользователя
        2. Отправка запроса с паролем этого же пользователя

        ОР: Код ответа: 201. Пользователь создан
        """

        user = self.users_builder.generate_user()
        username = self.fake.username
        email = self.fake.email
        response = self.myapp_api.add_user(username, email, user.password,
                                           expected_status=self.select_status_code(304))
        assert response.text == self.td_api.USER_ADDED
        assert self.myapp_db.is_user_exists(username=username, email=email)

    @pytest.mark.parametrize(
        'email',
        (
            '{}@{}.{}'.format(*i) for i in list(filter(
            lambda l: '' in l and any(l),
            product(
                ('', rand_val_eq.get_random_letters_and_digits(6)),
                ('', rand_val_eq.get_random_letters_and_digits(6)),
                ('', rand_val_eq.get_random_letters_and_digits(6))
            )
        ))
        )
    )
    @pytest.mark.xfail
    def test_api__add_user__incorrect_email(self, email):
        """
        Негативный тест добавления пользователя с некорректным email

        Шаги:
        1. Отправка запроса с некорректным email

        ОР: Код ответа: 400. Пользователь не создан
        """

        username = self.fake.username
        password = self.fake.password

        self.myapp_api.add_user(username, email, password, expected_status=self.select_status_code(400))
        assert not self.myapp_db.is_user_exists(username=username, email=email, password=password)

    @pytest.mark.parametrize(
        'username',
        [rand_val_eq.get_random_letters_and_digits(i) for i in [1, 5, 17, 50, 100]]
    )
    @pytest.mark.xfail
    def test_api__add_user__incorrect_username_length(self, username):
        """
        Негативный тест добавления пользователя с именем пользователя некорректной длины

        Шаги:
        1. Отправка запроса с именем пользователя некорректной длины

        ОР: Код ответа: 400. Пользователь не создан
        """

        email = self.fake.email
        password = self.fake.password
        self.myapp_api.add_user(username, email, password, expected_status=self.select_status_code(400))
        assert not self.myapp_db.is_user_exists(username=username, password=password, email=email)

    @pytest.mark.parametrize(
        'email',
        [rand_val_eq.get_random_letters_and_digits(i) for i in [1, 5]]
    )
    @pytest.mark.xfail
    def test_api__add_user__incorrect_email_length(self, email):
        """
        Негативный тест добавления пользователя с email некорректной длины

        Шаги:
        1. Отправка запроса с email некорректной длины

        ОР: Код ответа: 400. Пользователь не создан
        """

        username = self.fake.username
        password = self.fake.password
        self.myapp_api.add_user(username, email, password, expected_status=self.select_status_code(400))
        assert not self.myapp_db.is_user_exists(username=username, password=password, email=email)

    @pytest.mark.parametrize(
        'password',
        [rand_val_eq.get_random_letters_and_digits(i) for i in [1, 5]]
    )
    @pytest.mark.xfail
    def test_api__add_user__incorrect_password_length(self, password):
        """
        Негативный тест добавления пользователя с коротким паролем (меньше 6 символов)

        Шаги:
        1. Отправка запроса с паролем некорректной длины

        ОР: Код ответа: 400. Пользователь не создан
        """

        username = self.fake.username
        email = self.fake.email
        self.myapp_api.add_user(username, email, password, expected_status=self.select_status_code(400))
        assert not self.myapp_db.is_user_exists(username=username, password=password, email=email)


class TestMyappApiAuthWithoutStatusCodeChecking(TestMyappApiAuthWithStatusCodeChecking):
    check_status_code = False
