import logging
from dataclasses import dataclass
from datetime import datetime

import settings
from db.vk_api_client import VkApiDBClient
from db.myapp_client import MyappDBClient
from utils.random_values import random_different_values as rand_val_diff


@dataclass
class User:
    username: str
    password: str
    email: str
    access: bool
    active: bool
    start_active_time: datetime


class VkApiBuilder:
    def __init__(self, client: VkApiDBClient):
        self.client = client
        self.logger = logging.getLogger(settings.TESTS.LOGGER_NAME)

    def generate_vk_id(self, username):
        vk_id = rand_val_diff.get_id()
        self.client.set_vk_id(username, vk_id)
        return vk_id


class UserBuilder:
    def __init__(self, client: MyappDBClient):
        self.client = client
        self.logger = logging.getLogger(settings.TESTS.LOGGER_NAME)

    def generate_user(self, username=None, password=None, email=None, access=True, active=None, start_active_time=None,
                      save_in_db=True):
        username = username if username is not None else rand_val_diff.get_username()
        password = password if password is not None else rand_val_diff.get_password()
        email = email if email is not None else rand_val_diff.get_email()

        if save_in_db:
            obj = self.client.create_user(username=username, password=password, email=email, access=access,
                                          active=active,
                                          start_active_time=start_active_time)
            return obj
        else:
            return User(username, password, email, access, active, start_active_time)
