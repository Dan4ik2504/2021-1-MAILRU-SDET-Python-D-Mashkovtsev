import datetime

import pytest
import requests
from furl import furl

from api.client import ApiClient
from api.myapp_api import MyappApi
from test_api.base import BaseAPICase
from tests_data import Api as td_api


class BaseAPITestCase(BaseAPICase):
    td_api = td_api

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

    @staticmethod
    def create_new_myapp_api_client():
        return MyappApi(ApiClient(requests.Session()))


class BaseAPIAuthTestCase(BaseAPITestCase):
    authorize = True


class BaseAPINoAuthTestCase(BaseAPITestCase):
    authorize = False


class TestMyappApiAuth(BaseAPIAuthTestCase):

    def test_api__start_active_time_change(self):
        """
        Тест на изменение времени логина при повторном логине

        Шаги:
        1. Создание пользователя с временем последнего логина, которое меньше, чем текущее время
        2. Осуществить успешный логин

        ОР: Время последнего логина изменилось
        """
        user = self.users_builder.generate_user(start_active_time=datetime.datetime.now() - datetime.timedelta(days=1))
        first_login_time = user.start_active_time
        self.myapp_api.logout()
        self.myapp_api.login(user.username, user.password)
        user = self.myapp_db.get_user(username=user.username)
        second_login_time = user.start_active_time
        assert first_login_time < second_login_time


class TestMyappApiAuthWithStatusCodeChecking(BaseAPIAuthTestCase):
    check_response_status = True

    def select_status_code(self, status_code):
        return status_code if self.check_response_status else None

    # Tests

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
        if self.check_response_status:
            assert response.text == self.td_api.USER_ADDED
        assert self.myapp_db.check.is_user_exists(**user)

    @pytest.mark.parametrize(
        ("username", "email", "password", "error_msg"),
        (
                (True, True, None, td_api.CANT_ADD_USER__MISSING_PASSWORD),
                (True, None, True, td_api.CANT_ADD_USER__MISSING_EMAIL),
                (None, True, True, td_api.CANT_ADD_USER__MISSING_USERNAME),
                (None, None, None, td_api.CANT_ADD_USER__MISSING_USERNAME)
        )
    )
    def test_api__add_user__incorrect_request_json_data(self, username, email, password, error_msg):
        """
        Тест на отправку запроса на добавление пользователя с неполными данными

        Шаги:
        1. Отправка неполных данных пользователя

        ОР: Код ответа: 400. Пользователь не создан
        """

        username = username if username is None else self.fake.get_username()
        email = email if email is None else self.fake.get_email()
        password = password if password is None else self.fake.get_password()
        response = self.myapp_api.add_user(username, email, password,
                                           expected_status=self.select_status_code(400))
        if self.check_response_status:
            assert response.text == error_msg
        assert self.myapp_db.check.is_not_user_exists(username=username, email=email, password=password)

    @pytest.mark.parametrize(
        ("username", "email", "password", "erorr_msg"),
        (
                (False, False, False, td_api.CANT_ADD_USER__MISSING_USERNAME),
                (True, True, False, td_api.CANT_ADD_USER__MISSING_PASSWORD),
                (True, False, True, td_api.CANT_ADD_USER__MISSING_EMAIL),
                (False, True, True, td_api.CANT_ADD_USER__MISSING_USERNAME)
        )
    )
    def test_api__add_user__empty_data(self, username, email, password, erorr_msg):
        """
        Тест на отправку запроса на добавление пользователя с неполными данными

        Шаги:
        1. Отправка неполных данных пользователя

        ОР: Код ответа: 304. Пользователь не создан
        """

        username = self.fake.get_empty_value() if username is False else self.fake.get_username()
        email = self.fake.get_empty_value() if email is False else self.fake.get_email()
        password = self.fake.get_empty_value() if password is False else self.fake.get_password()
        self.myapp_api.add_user(username, email, password, expected_status=self.select_status_code(304))
        assert self.myapp_db.check.is_not_user_exists(username=username, email=email, password=password)

    def test_api__add_user_request_without_json(self):
        """
        Тест на отправку запроса на добавление пользователя без JSON

        Шаги:
        1. Отправка запроса без JSON

        ОР: Код ответа: 400
        """

        response = self.myapp_api.api.post_request(self.myapp_api.url_add_user,
                                                   expected_status=self.select_status_code(400))
        if self.check_response_status:
            assert response.text.startswith(td_api.CANT_ADD_USER)

    def test_api__add_existing_user(self):
        """
        Негативный тест добавления существующего пользователя

        Шаги:
        1. Создание нового пользователя
        2. Отправка данных этого же пользователя

        ОР: Код ответа: 304. Пользователь не создан
        """

        user = self.users_builder.generate_user()
        username = user.username
        email = user.email
        password = user.password
        response = self.myapp_api.add_user(username, email, password,
                                           expected_status=self.select_status_code(304))
        if self.check_response_status:
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
        password = self.fake.get_password()
        email = self.fake.get_email()
        response = self.myapp_api.add_user(user.username, email, password,
                                           expected_status=self.select_status_code(304))
        if self.check_response_status:
            assert response.text != self.td_api.USER_ADDED
        assert self.myapp_db.check.is_not_user_exists(email=email, password=password)

    def test_api__add_existing_email(self):
        """
        Негативный тест добавления пользователя c существующим в БД email

        Шаги:
        1. Создание нового пользователя
        2. Отправка запроса с email этого же пользователя

        ОР: Код ответа: 304. Пользователь не создан
        """

        user = self.users_builder.generate_user()
        username = self.fake.get_username()
        password = self.fake.get_password()
        response = self.myapp_api.add_user(username=username, email=user.email, password=password,
                                           expected_status=self.select_status_code(304))
        if self.check_response_status:
            assert response.text != self.td_api.USER_ADDED
        assert self.myapp_db.check.is_not_user_exists(username=username, password=password)

    def test_api__add_existing_password(self):
        """
        Тест добавления пользователя c существующим в БД паролем

        Шаги:
        1. Создание нового пользователя
        2. Отправка запроса с паролем этого же пользователя

        ОР: Код ответа: 201. Пользователь создан
        """

        user = self.users_builder.generate_user()
        username = self.fake.get_username()
        email = self.fake.get_email()
        response = self.myapp_api.add_user(username, email, user.password,
                                           expected_status=self.select_status_code(201))
        if self.check_response_status:
            assert response.text == self.td_api.USER_ADDED
        assert self.myapp_db.check.is_user_exists(username=username, email=email)

    def test_api__add_user__incorrect_email(self):
        """
        Негативный тест добавления пользователя с некорректным email

        Шаги:
        1. Отправка запроса с некорректным email

        ОР: Код ответа: 304. Пользователь не создан
        """

        email = self.fake.get_password().replace("@", "")
        username = self.fake.get_username()
        password = self.fake.get_password()

        self.myapp_api.add_user(username, email, password, expected_status=self.select_status_code(304))
        assert self.myapp_db.check.is_not_user_exists(username=username, email=email, password=password)

    @pytest.mark.parametrize(
        'username_length',
        [1, 5, 17, 50, 100]
    )
    def test_api__add_user__incorrect_username_length(self, username_length):
        """
        Негативный тест добавления пользователя с именем пользователя некорректной длины

        Шаги:
        1. Отправка запроса с именем пользователя некорректной длины

        ОР: Код ответа: 304. Пользователь не создан
        """

        username = self.fake.get_random_string(username_length)
        email = self.fake.get_email()
        password = self.fake.get_password()
        self.myapp_api.add_user(username, email, password, expected_status=self.select_status_code(304))
        assert self.myapp_db.check.is_not_user_exists(username=username, password=password, email=email)

    @pytest.mark.parametrize(
        'email_length',
        [1, 5]
    )
    def test_api__add_user__incorrect_email_length(self, email_length):
        """
        Негативный тест добавления пользователя с email некорректной длины

        Шаги:
        1. Отправка запроса с email некорректной длины

        ОР: Код ответа: 304. Пользователь не создан
        """

        email = self.fake.get_random_string(email_length)
        username = self.fake.get_username()
        password = self.fake.get_password()
        self.myapp_api.add_user(username, email, password, expected_status=self.select_status_code(304))
        assert self.myapp_db.check.is_not_user_exists(username=username, password=password, email=email)

    @pytest.mark.parametrize(
        'password_length',
        [1, 5]
    )
    def test_api__add_user__incorrect_password_length(self, password_length):
        """
        Негативный тест добавления пользователя с коротким паролем (меньше 6 символов)

        Шаги:
        1. Отправка запроса с паролем некорректной длины

        ОР: Код ответа: 304. Пользователь не создан
        """

        password = self.fake.get_random_string(password_length)
        username = self.fake.get_username()
        email = self.fake.get_email()
        self.myapp_api.add_user(username, email, password, expected_status=self.select_status_code(304))
        assert self.myapp_db.check.is_not_user_exists(username=username, password=password, email=email)

    def test_api__delete_user__positive(self):
        """
        Тест удаления существующего пользователя

        Шаги:
        1. Создать пользователя в БД
        2. Отправить запрос на удаление пользователя

        ОР: Код ответа: 204. Пользователь удален
        """

        user = self.users_builder.generate_user()
        self.myapp_api.delete_user(username=user.username, expected_status=self.select_status_code(204))
        assert self.myapp_db.check.is_not_user_exists(username=user.username, password=user.password, email=user.email)

    def test_api__delete_nonexistent_user(self):
        """
        Тест удаления несуществующего пользователя

        Шаги:
        1. Отправить запрос на удаление несуществующего пользователя

        ОР: Код ответа: 404
        """

        response = self.myapp_api.delete_user(username=self.fake.get_username(),
                                              expected_status=self.select_status_code(404))
        if self.check_response_status:
            assert response.text == td_api.USER_DOES_NOT_EXIST

    def test_api__block_user__positive(self):
        """
        Тест блокировки пользователя

        Шаги:
        1. Создать незаблокированного пользователя в БД
        2. Отправка запроса на блокировку данного пользователя

        ОР: Код ответа: 200. Пользователь заблокирован
        """

        user = self.users_builder.generate_user()

        temp_client = self.create_new_myapp_api_client()
        temp_client.login(user.username, user.password)
        response1 = temp_client.get_main_page()
        assert furl(response1.url).path == furl(temp_client.url_main_page).path

        response2 = self.myapp_api.block_user(user.username, expected_status=self.select_status_code(200))
        assert response2.text == td_api.USER_BLOCKED
        assert self.myapp_db.get_user(username=user.username).access == 0

        response3 = temp_client.get_main_page()
        assert furl(response3.url).path == furl(temp_client.url_login).path

    def test_api__block_blocked_user(self):
        """
        Тест блокировки заблокированного пользователя

        Шаги:
        1. Создать заблокированного пользователя в БД
        2. Отправка запроса на блокировку данного пользователя

        ОР: Код ответа: 304. Пользователь заблокирован
        """

        user = self.users_builder.generate_user(access=0)
        self.myapp_api.block_user(user.username, expected_status=self.select_status_code(304))
        assert self.myapp_db.get_user(username=user.username).access == 0

    def test_api__block_nonexistent_user(self):
        """
        Тест блокировки несуществующего пользователя

        Шаги:
        1. Отправка запроса на блокировку несуществующего пользователя

        ОР: Код ответа: 404
        """

        response = self.myapp_api.block_user(self.fake.get_username(), expected_status=self.select_status_code(404))
        if self.check_response_status:
            assert response.text == td_api.USER_DOES_NOT_EXIST

    def test_api__unblock_user__positive(self):
        """
        Тест разблокировки пользователя

        Шаги:
        1. Создать заблокированного пользователя в БД
        2. Отправка запроса на разблокировку данного пользователя

        ОР: Код ответа: 200. Пользователь не заблокирован
        """

        user = self.users_builder.generate_user(access=0)

        temp_client = self.create_new_myapp_api_client()
        temp_client.login(user.username, user.password, expected_status=self.select_status_code(401))

        response = self.myapp_api.accept_user(user.username, expected_status=self.select_status_code(200))
        if self.check_response_status:
            assert response.text == td_api.USER_UNBLOCKED
        assert self.myapp_db.get_user(username=user.username).access == 1

        temp_client.login(user.username, user.password)
        response2 = temp_client.get_main_page()
        assert furl(response2.url).path == furl(temp_client.url_main_page).path

    def test_api__unblock_unblocked_user(self):
        """
        Тест разблокировки незаблокированного пользователя

        Шаги:
        1. Создать незаблокированного пользователя в БД
        2. Отправка запроса на разблокировку данного пользователя

        ОР: Код ответа: 304. Пользователь не заблокирован
        """

        user = self.users_builder.generate_user(access=1)
        self.myapp_api.accept_user(user.username, expected_status=self.select_status_code(304))
        assert self.myapp_db.get_user(username=user.username).access == 1

    def test_api__unblock_nonexistent_user(self):
        """
        Тест разблокировки несуществующего пользователя

        Шаги:
        1. Отправка запроса на разблокировку несуществующего пользователя

        ОР: Код ответа: 404
        """

        response = self.myapp_api.accept_user(self.fake.get_username(), expected_status=self.select_status_code(404))
        if self.check_response_status:
            assert response.text == td_api.USER_DOES_NOT_EXIST


class TestMyappApiAuthWithoutStatusCodeChecking(TestMyappApiAuthWithStatusCodeChecking):
    check_response_status = False


class TestMyappApiNoAuthAccess(BaseAPINoAuthTestCase):
    def test_api__no_auth_access__add_user(self):
        """
        Тест добавления пользователя без предварительной авторизации

        Шаги:
        1. Создание случайных данных пользователя
        2. Отправка данных

        ОР: Код ответа: 401. Пользователь не создан
        """
        user, response = self.create_user_data_and_send_post_request(expected_status=401)
        assert response.json().get('error') == td_api.AUTHORIZATION_FAILED
        assert self.myapp_db.check.is_not_user_exists(**user)

    def test_api__no_auth_access__delete_user(self):
        """
        Тест удаления пользователя без предварительной авторизации

        Шаги:
        1. Создать пользователя в БД
        2. Отправка запроса на удаление данного пользователя

        ОР: Код ответа: 401. Пользователь не удален
        """

        user = self.users_builder.generate_user()
        response = self.myapp_api.delete_user(user.username, expected_status=401)
        assert response.json().get('error') == td_api.AUTHORIZATION_FAILED
        assert self.myapp_db.check.is_user_exists(username=user.username)

    def test_api__no_auth_access__block_user(self):
        """
        Тест блокировки пользователя без предварительной авторизации

        Шаги:
        1. Создать не заблокированного пользователя в БД
        2. Отправка запроса на блокировку данного пользователя

        ОР: Код ответа: 401. Пользователь не заблокирован
        """

        user = self.users_builder.generate_user()
        response = self.myapp_api.block_user(user.username, expected_status=401)
        assert response.json().get('error') == td_api.AUTHORIZATION_FAILED
        assert self.myapp_db.get_user(username=user.username).access == 1

    def test_api__no_auth_access__unblock_user(self):
        """
        Тест разблокировки пользователя без предварительной авторизации

        Шаги:
        1. Создать заблокированного пользователя в БД
        2. Отправка запроса на разблокировку данного пользователя

        ОР: Код ответа: 401. Пользователь заблокирован
        """

        user = self.users_builder.generate_user(access=0)
        response = self.myapp_api.accept_user(user.username, expected_status=401)
        assert response.json().get('error') == td_api.AUTHORIZATION_FAILED
        assert self.myapp_db.get_user(username=user.username).access == 0


class TestMyappStatus(BaseAPINoAuthTestCase):
    def check_myapp_status(self):
        response = self.myapp_api.app_status(expected_status=200)
        assert response.json()['status'] == 'ok'

    def test_api__no_auth__myapp_status(self):
        """
        Тест проверки статуса приложения без авторизации

        Шаги:
        1. Отправка запроса

        ОР: Код ответа: 200. Статус: 'ok'
        """

        self.check_myapp_status()

    def test_api__auth__myapp_status(self):
        """
        Тест проверки статуса приложения с предварительной авторизацией

        Шаги:
        1. Авторизация
        2. Отправка запроса

        ОР: Код ответа: 200. Статус: 'ok'
        """

        user = self.users_builder.generate_user()
        self.myapp_api.login(user.username, user.password)
        self.check_myapp_status()
