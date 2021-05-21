import pytest
import requests

from api.client import ApiClient


@pytest.fixture(scope='function')
def api_session():
    return requests.Session()


@pytest.fixture(scope='function')
def api_client(api_session):
    return ApiClient(api_session)

