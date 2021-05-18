import logging

from network.http_client import HttpClient
import settings

logger = logging.getLogger(settings.LOGGING.LOGGER_NAME)


class MockHTTPClient:
    url = settings.MOCK_SETTINGS.USER_ACTIONS_URL
    url_base = settings.MOCK_SETTINGS.USER_ACTIONS_URL_BASE

    def __init__(self):
        self.http_client = HttpClient()

    def get_user_last_name(self, first_name):
        logger.info(f'Getting the last name of the user with the first name "{first_name}"')
        response = self.http_client.get(self.url_base.format(str(first_name)))
        return response

    def set_user_last_name(self, last_name, first_name):
        logger.info(f'Setting the last name of the user with the first name "{first_name}"')
        json_data = {'first_name': first_name,
                     'last_name': last_name}
        response = self.http_client.post(self.url, json=json_data)
        return response

    def update_user_last_name(self, first_name, last_name):
        logger.info(f'Updating the last name of the user with the first name "{first_name}"')
        json_data = {'last_name': last_name}
        response = self.http_client.put(self.url_base.format(str(first_name)), json=json_data)
        return response

    def delete_user_last_name(self, first_name):
        logger.info(f'Removing the last name of the user with the first name "{first_name}"')
        response = self.http_client.delete(self.url_base.format(str(first_name)))
        return response
