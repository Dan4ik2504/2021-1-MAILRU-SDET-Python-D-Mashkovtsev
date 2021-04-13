import pytest
import requests

from api.login import LoginApi
from api.client import ApiClient


@pytest.fixture(scope='function')
def login_page_api(api_session):
    return LoginApi(api_session)


@pytest.fixture(scope='function')
def api_client(api_session):
    return ApiClient(api_session)


@pytest.fixture(scope='function')
def api_session():
    return requests.Session()

