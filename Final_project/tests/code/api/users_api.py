import logging
from urllib.parse import urljoin
import allure

from api.client import ApiClient
import settings


class UsersApi:
    def __init__(self, api_client):
        self.api: ApiClient = api_client
        self.url = settings.APP_SETTINGS.URL_API
        self.logger = logging.getLogger(settings.TESTS.LOGGER_NAME)

    @allure.step("Login via API. Username: {username}. Password: {password}")
    def login(self, username, password):
        self.logger.info(f"Login via API. Username: {username}. Password: {password}")
        url = urljoin(self.url, settings.APP_SETTINGS.URLS.LOGIN)
        data = {
            'username': {username},
            'password': {password},
            'submit': 'Login'
        }
        self.api.post_request(url, data=data, expected_status=200, jsonify=False)
