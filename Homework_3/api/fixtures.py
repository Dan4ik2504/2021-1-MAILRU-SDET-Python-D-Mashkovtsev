import pytest

from api.client import ApiClient


@pytest.fixture(scope='function')
def api_client():
    return ApiClient()
