import pytest
from _pytest.fixtures import FixtureRequest


class ApiTestsBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request: FixtureRequest, api_client, login_api, campaigns_api, segments_api):
        self.api_client = api_client
        self.login_api = login_api
        self.campaigns_api = campaigns_api
        self.segments_api = segments_api

        if self.authorize:
            request.getfixturevalue("api_login")
