import pytest
import itertools

from tests.base import BaseMockTestCase
from utils.builder import Builder
from faker import Faker

builder = Builder()
fake = Faker()


class TestMockGet(BaseMockTestCase):
    def test_get_nonexistent_entry(self):
        response = self.mock_client.get_user_last_name('qweoirhqwflcnqsknbiwqhewqfuuchqweiufhw')
        assert response.status_code == 404

    @pytest.mark.parametrize(
        ("first_name", "last_name"),
        (
                ('test_first_name', 'test_last_name'),
                ('name', 'name'),
                ('123', '456'),
                ("""ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_""",
                 """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"""),
                *builder.get_users_list_of_tuples(5)
        )
    )
    def test_get_existent_entry(self, first_name, last_name):
        self.mock_db.insert(first_name=first_name, last_name=last_name)

        response = self.mock_client.get_user_last_name(first_name)
        assert response.status_code == 200
        assert response.json['data']['last_name'] == last_name


class TestMockPost(BaseMockTestCase):
    @pytest.mark.parametrize(
        ("first_name", "last_name"),
        (
                ('test_first_name', 'test_last_name'),
                ('name', 'name'),
                ('123', '456'),
                ("""ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_""",
                 """ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"""),
                *builder.get_users_list_of_tuples(5)
        )
    )
    def test_add_entry_positive(self, first_name, last_name):
        response = self.mock_client.set_user_last_name(first_name=first_name, last_name=last_name)
        assert response.status_code == 201

        assert len(self.mock_db.select(first_name=first_name, last_name=last_name)) == 1

    @pytest.mark.parametrize(
        ("first_name", "last_name"),
        (
                ('', ''),
                ('', 'test_last_name'),
                ('test_first_name', '')
        )
    )
    def test_add_entry_send_incorrect_json_data(self, first_name, last_name):
        response = self.mock_client.set_user_last_name(first_name=first_name, last_name=last_name)
        assert response.status_code == 400

        assert len(self.mock_db.select(first_name=first_name, last_name=last_name)) == 0

    @pytest.mark.parametrize(
        ("first_name", "last_name"),
        (
                *builder.get_users_list_of_tuples(5),
        )
    )
    def test_add_existent_entry(self, first_name, last_name):
        self.mock_db.insert(first_name=first_name, last_name=last_name)

        response = self.mock_client.set_user_last_name(first_name=first_name, last_name=last_name)
        assert response.status_code == 409


class TestMockPut(BaseMockTestCase):
    @pytest.mark.parametrize(
        ("first_name", "prev_last_name", "next_last_name"),
        (
                ('test_first_name', 'test_last_name_prev', 'test_last_name_next'),
                *[(fake.first_name(), *builder.get_different_last_names(2)) for _ in range(5)]
        )
    )
    def test_update_entry_positive(self, first_name, prev_last_name, next_last_name):
        self.mock_db.insert(first_name=first_name, last_name=prev_last_name)

        response = self.mock_client.update_user_last_name(first_name=first_name, last_name=next_last_name)
        assert response.status_code == 201

        assert len(self.mock_db.select(first_name=first_name, last_name=prev_last_name)) == 0
        assert len(self.mock_db.select(first_name=first_name, last_name=next_last_name)) == 1

    @pytest.mark.parametrize(
        ("first_name", "prev_last_name", "next_last_name"),
        (
                *[(fake.first_name(), fake.last_name(), '') for _ in range(5)],
        )
    )
    def test_update_entry_send_incorrect_json_data(self, first_name, prev_last_name, next_last_name):
        self.mock_db.insert(first_name=first_name, last_name=prev_last_name)

        response = self.mock_client.update_user_last_name(first_name=first_name, last_name=next_last_name)
        assert response.status_code == 400

        assert len(self.mock_db.select(first_name=first_name, last_name=prev_last_name)) == 1
        assert len(self.mock_db.select(first_name=first_name, last_name=next_last_name)) == 0

    def test_update_nonexistent_entry(self):
        response = self.mock_client.update_user_last_name(first_name='test_first_name', last_name='test_last_name')
        assert response.status_code == 404


class TestMockDelete(BaseMockTestCase):
    def test_delete_nonexistent_entry(self):
        first_name = 'test_first_name'
        response = self.mock_client.delete_user_last_name(first_name)
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "first_name",
        ('test_first_name', '123', *[fake.first_name() for _ in range(5)])
    )
    def test_delete_positive(self, first_name):
        last_name = fake.last_name()
        self.mock_db.insert(first_name=first_name, last_name=last_name)

        response = self.mock_client.delete_user_last_name(first_name)
        assert response.status_code == 200

        assert len(self.mock_db.select(first_name=first_name, last_name=last_name)) == 0


class TestRequestMethods(BaseMockTestCase):
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    @pytest.mark.parametrize(
        ("method", "path"),
        list(itertools.product(methods,
                               ('', 'first_name', 'test_nonexistent_path',
                                'last_name/test_last_name/test_nonexistent_path', '123')))
    )
    def test_request_nonexistent_path(self, method, path):
        url = self.mock_url + '/' + path if path else self.mock_url
        response = self.http_client.request(method, url)
        assert response.status_code == 404

    @pytest.mark.parametrize(
        ("method", "path"),
        (
                ('GET', 'last_name'),
                ('PUT', 'last_name'),
                ('DELETE', 'last_name'),
                ('POST', 'last_name/test_last_name')
        )
    )
    def test_request_incorrect_methods(self, method, path):
        url = self.mock_url + '/' + path if path else self.mock_url
        response = self.http_client.request(method, url)
        assert response.status_code == 405

    @pytest.mark.parametrize(
        ("method", "path", "json_data"),
        (
                ('POST', 'last_name', ''),
                ('POST', 'last_name', 'test'),
                ('POST', 'last_name', 12345),
                ('POST', 'last_name', ()),
                ('POST', 'last_name', ('test1', 'test2')),
                ('POST', 'last_name', dict()),
                ('POST', 'last_name', {'first_name': 'test', 'last_name': 'test2', 'incorrect_field': 'test3'}),
                ('POST', 'last_name', {'first_name': 'test', 'incorrect_field': 'test3'}),
                ('POST', 'last_name', {'incorrect_field': 'test3'}),
                ('PUT', 'last_name/test_last_name', ''),
                ('PUT', 'last_name/test_last_name', 'test'),
                ('PUT', 'last_name/test_last_name', 12345),
                ('PUT', 'last_name/test_last_name', ()),
                ('PUT', 'last_name/test_last_name', ('test1', 'test2')),
                ('PUT', 'last_name/test_last_name', dict()),
                ('PUT', 'last_name/test_last_name', {'first_name': 'test', 'last_name': 'test2'}),
                ('PUT', 'last_name/test_last_name', {'last_name': 'test', 'incorrect_field': 'test2'}),
                ('PUT', 'last_name/test_last_name', {'first_name': 'test', 'incorrect_field': 'test2'}),
                ('PUT', 'last_name/test_last_name', {'incorrect_field': 'test2'}),
        )
    )
    def test_request_incorrect_json(self, method, path, json_data):
        url = self.mock_url + '/' + path if path else self.mock_url
        response = self.http_client.request(method, url, json=json_data)
        assert response.status_code == 400
