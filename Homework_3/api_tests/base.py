import pytest


class ApiBase:
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, login_page_api, api_client):
        self.api_client = api_client
        self.login_page_api = login_page_api

        if self.authorize:
            self.login_page_api.post_login()
