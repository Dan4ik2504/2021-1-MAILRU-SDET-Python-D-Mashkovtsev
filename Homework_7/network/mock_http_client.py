from urllib.parse import urljoin

from network.http_client import HttpClient
import settings
import exceptions


class MockHTTPClient:
    url = settings.MOCK_SETTINGS.USER_ACTIONS_URL
    url_base = settings.MOCK_SETTINGS.USER_ACTIONS_URL_BASE

    def __init__(self):
        self.http_client = HttpClient()

    def get_user_last_name(self, first_name):
        response = self.http_client.get(self.url_base.format(str(first_name)))
        return response

    def set_user_last_name(self, last_name, first_name):
        json_data = {'first_name': first_name,
                     'last_name': last_name}
        response = self.http_client.post(self.url, json=json_data)
        return response

    def update_user_last_name(self, first_name, last_name):
        json_data = {'last_name': last_name}
        response = self.http_client.put(self.url_base.format(str(first_name)), json=json_data)
        return response

    def delete_user_last_name(self, first_name):
        response = self.http_client.delete(self.url_base.format(str(first_name)))
        return response
