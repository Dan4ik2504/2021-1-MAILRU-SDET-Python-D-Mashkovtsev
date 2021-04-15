import allure

import settings
from api import settings_api
from api.client import ApiClient


class LoginApi(ApiClient):
    class Exceptions(ApiClient.Exceptions):
        class InvalidLogin(Exception):
            pass

        class InvalidLogout(Exception):
            pass

    @allure.step('Login via API. Login: "{login}". Password: "{password}"')
    def login(self, login=settings.User.LOGIN, password=settings.User.PASSWORD):
        """POST request to get authorization cookie"""
        self.logger.info(f'Login via API. Login: "{login}". Password: "{password}"')

        data = {
            'email': login,
            'password': password,
        }

        response = self.post_request(settings.Url.POST_LOGIN, data=data, jsonify=False, allow_redirects=False,
                                     expected_status=302)

        if not self.is_cookie_exists(settings_api.CookieNames.SESSION):
            raise self.Exceptions.InvalidLogin("Unsuccessful login. Authorization cookie doesn't exists.")

        return response

    @allure.step("Logout via API")
    def logout(self):
        """GET request to delete authorization cookie"""
        self.logger.info("Logout via API")
        self.get_request(settings.Url.LOGOUT, jsonify=False)
        if self.is_cookie_exists(settings_api.CookieNames.SESSION):
            raise self.Exceptions.InvalidLogout("Unsuccessful logout. Authorization cookie exists.")
