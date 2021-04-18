import pytest
import requests

import settings
from api.login import LoginApi
from api.client import ApiClient
from api.campaigns import CampaignsApi
from api.segments import SegmentsApi


@pytest.fixture(scope='function')
def api_login(login_api):
    login_api.login(login=settings.User.LOGIN, password=settings.User.PASSWORD)


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


@pytest.fixture(scope='function')
def segments_api(api_session):
    return SegmentsApi(api_session)
