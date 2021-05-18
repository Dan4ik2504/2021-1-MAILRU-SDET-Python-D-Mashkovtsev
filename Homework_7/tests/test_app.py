import pytest

import settings
from mock import app_mock
from network.http_client import HttpClient

app_url = settings.APP_SETTINGS.URL
http_client = HttpClient()


class TestsApp:
    @pytest.fixture(scope='session', autouse=True)
    def setup(self, request):
        request.getfixturevalue("start_app")
        request.getfixturevalue("start_stub")
        request.getfixturevalue("start_mock")

    def test_add_get_user(self):
        resp = http_client.post(f'{app_url}/user', json={'first_name': 'Ilya'})
        assert resp.status_code == 201
        user_id_from_add = resp.json["data"]['entry_id']

        resp = http_client.get(f'{app_url}/user/Ilya')
        assert resp.status_code == 200
        user_id_from_get = resp.json["data"]['entry_id']

        assert user_id_from_add == user_id_from_get

    def test_get_non_existent_user(self):
        resp = http_client.get(f'{app_url}/user/dnsfndksfnkjsdnfjkdsjkfnsd')
        assert resp.status_code == 404

    def test_add_existent_user(self):
        http_client.post(f'{app_url}/user', json={'first_name': 'Ilya1'})
        resp = http_client.post(f'{app_url}/user', json={'first_name': 'Ilya1'})
        assert resp.status_code == 409

    def test_get_age(self):
        http_client.post(f'{app_url}/user', json={'first_name': 'Vasya'})

        resp = http_client.get(f'{app_url}/user/Vasya')

        assert isinstance(resp.json["data"]['age'], int)
        assert 0 <= resp.json["data"]['age'] <= 100

    def test_has_surname(self):
        app_mock.table_last_names.insert(first_name='Olya', last_name='Zaitceva')

        http_client.post(f'{app_url}/user', json={'first_name': 'Olya'})

        resp = http_client.get(f'{app_url}/user/Olya')
        assert resp.json['data']['last_name'] == 'Zaitceva'

    def test_has_not_surname(self):
        http_client.post(f'{app_url}/user', json={'first_name': 'Sveta'})

        resp = http_client.get(f'{app_url}/user/Sveta')
        assert resp.json['data']['last_name'] is None

    def test_fail(self):
        response = http_client.post(f'{app_url}/user', json={'asd': 'dsa'})
        assert response.status_code == 400
