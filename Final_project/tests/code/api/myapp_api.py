import logging
from urllib.parse import urljoin
import allure

from api.client import ApiClient
import settings


class MyappApi:
    urls = settings.APP_SETTINGS.API_URLS

    def __init__(self, api_client):
        self.api: ApiClient = api_client
        self.url_base = settings.APP_SETTINGS.URL_API
        self.url_api = urljoin(self.url_base, self.urls.API_PREFIX)
        self.url_login = urljoin(self.url_base, settings.APP_SETTINGS.URLS.LOGIN)
        self.url_add_login = urljoin(self.url_api, self.urls.ADD_USER)
        self.logger = logging.getLogger(settings.TESTS.LOGGER_NAME)

    @allure.step("Login via API. Username: {username}. Password: {password}")
    def login(self, username, password):
        self.logger.info(f"Login via API. Username: {username}. Password: {password}")
        data = {
            'username': {username},
            'password': {password},
            'submit': 'Login'
        }
        self.api.post_request(self.url_login, data=data, expected_status=200, return_json_data=False)

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

        response = self.api.post_request(url=self.url_add_login, json=data, expected_status=expected_status,
                                         return_json_data=return_json_data)
        return response
