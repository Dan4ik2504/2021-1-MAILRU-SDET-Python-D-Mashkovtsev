import pytest


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, login_api, api_client):
        self.api_client = api_client
        self.login_api = login_api

        if self.authorize:
            self.login_api.post_login()
