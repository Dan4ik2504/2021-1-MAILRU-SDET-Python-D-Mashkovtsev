import pytest


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, login_api, campaigns_api):
        self.api_client = api_client
        self.login_api = login_api
        self.campaigns_api = campaigns_api

        if self.authorize:
            self.login_api.post_login()
