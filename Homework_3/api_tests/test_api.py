import allure
import pytest

import settings
from api_tests.base import ApiBase


class TestLogin(ApiBase):
    authorize = False

    def get_dashboard(self):
        response = self.api_client.get_request(settings.Url.DASHBOARD, jsonify=False)
        assert response.status_code == 200
        return response

    def verify_login(self):
        response = self.get_dashboard()
        assert response.url == settings.Url.DASHBOARD

    def verify_logout(self):
        response = self.get_dashboard()
        assert response.url == settings.Url.BASE

    @allure.title("Positive login test")
    @pytest.mark.API
    def test_positive_login(self):
        self.login_api.post_login()
        self.verify_login()

    @allure.title("Negative login test")
    @pytest.mark.API
    def test_negative_login(self):
        with pytest.raises(self.login_api.Exceptions.InvalidLogin):
            self.login_api.post_login("1q2w3e", "1q2w3e")
        self.verify_logout()

    @allure.title("Logout test")
    @pytest.mark.API
    def test_logout(self):
        self.login_api.post_login()
        self.verify_login()
        self.login_api.logout()
        self.verify_logout()
