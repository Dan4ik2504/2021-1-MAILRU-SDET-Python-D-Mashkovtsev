import pytest

from db.myapp_client import MyappDBClient
from db.vk_api_client import VkApiDBClient


@pytest.fixture(scope='session')
def myapp_client():
    client = MyappDBClient()
    yield client
    client.connection.close()


@pytest.fixture(scope='session')
def vk_api_client():
    client = VkApiDBClient()
    yield client
    client.connection.close()
