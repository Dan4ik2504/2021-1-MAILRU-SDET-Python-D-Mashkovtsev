import allure
import pytest

import settings
from api_tests.base import ApiBase


class TestLogin(ApiBase):
    authorize = False

    @allure.title("Positive login test")
    @pytest.mark.API
    def test_positive_login(self):
        self.login_page_api.post_login()
        response = self.api_client.get(settings.Url.DASHBOARD, jsonify=False)
        assert response.status_code == 200
        assert response.url == settings.Url.DASHBOARD

    @allure.title("Negative login test")
    @pytest.mark.API
    def test_negative_login(self):
        with pytest.raises(self.login_page_api.Exceptions.InvalidLogin):
            self.login_page_api.post_login("1q2w3e", "1q2w3e")
        response = self.api_client.get(settings.Url.DASHBOARD, jsonify=False)
        assert response.status_code == 200
        assert response.url == settings.Url.BASE
