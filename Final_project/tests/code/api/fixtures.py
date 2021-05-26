import pytest
import requests

from api.client import ApiClient
from api.users_api import UsersApi


@pytest.fixture(scope='function')
def api_session():
    return requests.Session()


@pytest.fixture(scope='function')
def api_client(api_session):
    return ApiClient(api_session)


@pytest.fixture(scope='function')
def users_api(api_client):
    return UsersApi(api_client)
