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

    @allure.step('Login via API: "{login}"')
    def post_login(self, login=settings.User.LOGIN, password=settings.User.PASSWORD):
        """POST request to get authorization cookie"""
        self.logger.info(f'Login via API: "{login}"')

        location = settings.Url.POST_LOGIN

        headers = {
            'Referer': settings.Url.BASE,
        }

        data = {
            'email': login,
            'password': password,
        }
        self.logger.debug(f'Login POST request data: "{"; ".join([f"{k}: {v}" for k, v in data.items()])}"')

        response = self._request(self.Methods.POST, location, headers=headers, data=data, jsonify=False,
                                 allow_redirects=False, expected_status=302)

        auth_cookie = self.get_cookie(settings_api.CookieNames.SESSION)
        if auth_cookie is None:
            raise self.Exceptions.InvalidLogin("Unsuccessful login. Authorization cookie doesn't exists.")

        return response

    @allure.step("Logout via API")
    def logout(self):
        """GET request to delete authorization cookie"""
        self.logger.info("Logout via API")
        self.get_request(settings.Url.LOGOUT, jsonify=False)
        if self.get_cookie(settings_api.CookieNames.SESSION) is not None:
            raise self.Exceptions.InvalidLogout("Unsuccessful logout. Authorization cookie exists.")
