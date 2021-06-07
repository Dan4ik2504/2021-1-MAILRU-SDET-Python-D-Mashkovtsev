import logging
from urllib.parse import urljoin

import allure

import settings
from api.client import ApiClient


class MyappApi:
    urls = settings.APP_SETTINGS.API_URLS

    def __init__(self, api_client):
        self.api: ApiClient = api_client
        self.url_base = settings.APP_SETTINGS.URL_API
        self.url_login = urljoin(self.url_base, settings.APP_SETTINGS.URLS.LOGIN)
        self.url_logout = urljoin(self.url_base, settings.APP_SETTINGS.URLS.LOGOUT)
        self.url_app_status = urljoin(self.url_base, self.urls.APP_STATUS)
        self.url_add_user = urljoin(self.url_base, self.urls.ADD_USER)
        self.url_delete_user = urljoin(self.url_base, self.urls.DELETE_USER)
        self.url_block_user = urljoin(self.url_base, self.urls.BLOCK_USER)
        self.url_accept_user = urljoin(self.url_base, self.urls.ACCEPT_USER)
        self.url_main_page = urljoin(self.url_base, settings.APP_SETTINGS.URLS.MAIN)
        self.logger = logging.getLogger(settings.TESTS.LOGGER_NAME)

    @allure.step("Login via API. Username: {username}. Password: {password}")
    def login(self, username, password, expected_status=200):
        self.logger.info(f"Login via API. Username: {username}. Password: {password}")
        data = {
            'username': {username},
            'password': {password},
            'submit': 'Login'
        }
        response = self.api.post_request(self.url_login, data=data, expected_status=expected_status,
                                         return_json_data=False)
        return response

    @allure.step("Logout via API")
    def logout(self):
        self.logger.info(f"Logout via API")
        response = self.api.get_request(self.url_logout)
        return response

    def get_main_page(self, expected_status=200):
        return self.api.get_request(self.url_main_page, expected_status=expected_status)

    @allure.step("Add user via API")
    def add_user(self, username=None, email=None, password=None, expected_status=201, return_json_data=False):
        self.logger.info(f"Add user via API. Username: {username}. Password: {password}. Email: {email}")
        data = {}

        if username is not None:
            data["username"] = username

        if email is not None:
            data["email"] = email

        if password is not None:
            data["password"] = password

        response = self.api.post_request(url=self.url_add_user, json=data, expected_status=expected_status,
                                         return_json_data=return_json_data)
        return response

    @allure.step("Delete user via API")
    def delete_user(self, username, expected_status=204, return_json_data=False):
        self.logger.info(f"Delete user via API. Username: {username}")
        url = self.url_delete_user.format(username=username)
        response = self.api.get_request(url=url, expected_status=expected_status, return_json_data=return_json_data)
        return response

    @allure.step("Block user via API")
    def block_user(self, username, expected_status=200, return_json_data=False):
        self.logger.info(f"Block user via API. Username: {username}")
        url = self.url_block_user.format(username=username)
        response = self.api.get_request(url=url, expected_status=expected_status, return_json_data=return_json_data)
        return response

    @allure.step("Unblock user via API")
    def accept_user(self, username, expected_status=200, return_json_data=False):
        self.logger.info(f"Unblock user via API. Username: {username}")
        url = self.url_accept_user.format(username=username)
        response = self.api.get_request(url=url, expected_status=expected_status, return_json_data=return_json_data)
        return response

    @allure.step("Checking app status")
    def app_status(self, expected_status=200, return_json_data=False):
        self.logger.info(f"Checking app status")
        response = self.api.get_request(url=self.url_app_status, expected_status=expected_status,
                                        return_json_data=return_json_data)
        return response
