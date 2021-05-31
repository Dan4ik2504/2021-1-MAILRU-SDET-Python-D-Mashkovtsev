import pytest
import requests

from api.client import ApiClient
from api.myapp_api import MyappApi


@pytest.fixture(scope='function')
def api_session():
    return requests.Session()


@pytest.fixture(scope='function')
def api_client(api_session):
    return ApiClient(api_session)


@pytest.fixture(scope='function')
def myapp_api(api_client):
    return MyappApi(api_client)
