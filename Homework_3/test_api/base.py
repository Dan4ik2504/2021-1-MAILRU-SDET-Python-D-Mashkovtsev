import pytest


class ApiTestsBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client, login_api, campaigns_api, segments_api):
        self.api_client = api_client
        self.login_api = login_api
        self.campaigns_api = campaigns_api
        self.segments_api = segments_api

        if self.authorize:
            self.login_api.login()