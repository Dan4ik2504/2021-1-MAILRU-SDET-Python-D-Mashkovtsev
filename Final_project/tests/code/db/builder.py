import logging

import settings
from db.vk_api_client import VkApiDBClient
from db.myapp_client import MyappDBClient
from utils.random_values import random_different_values


class VkApiBuilder:
    def __init__(self, client: VkApiDBClient):
        self.client = client
        self.logger = logging.getLogger(settings.TESTS.LOGGER_NAME)

    def generate_vk_id(self):
        vk_id = random_different_values.id
        self.client.set_vk_id(vk_id)
        return vk_id


class UserBuilder:
    def __init__(self, client: MyappDBClient):
        self.client = client
        self.logger = logging.getLogger(settings.TESTS.LOGGER_NAME)

    def generate_user(self, username=None, password=None, email=None, access=True, active=None, start_active_time=None):
        username = username if username is not None else random_different_values.username
        password = password if password is not None else random_different_values.password
        email = email if email is not None else random_different_values.email

        self.client.create_user(username=username, password=password, email=email, access=access, active=active,
                                start_active_time=start_active_time)

        return {
            'username': username,
            'password': password,
            'email': email,
            'access': access,
            'active': active,
            'start_active_time': start_active_time
        }

