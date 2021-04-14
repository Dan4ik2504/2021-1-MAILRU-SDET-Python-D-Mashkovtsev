import pytest
import requests

from api.login import LoginApi
from api.client import ApiClient
from api.campaigns import CampaignsApi


@pytest.fixture(scope='function')
def api_session():
    return requests.Session()


@pytest.fixture(scope='function')
def api_client(api_session):
    return ApiClient(api_session)


@pytest.fixture(scope='function')
def login_api(api_session):
    return LoginApi(api_session)


@pytest.fixture(scope='function')
def campaigns_api(api_session):
    return CampaignsApi(api_session)

