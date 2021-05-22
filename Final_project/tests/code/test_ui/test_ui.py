from datetime import datetime
import time

import pytest

import settings
from base import BaseCase
from db.myapp_client import MyappDBClient
from db.vk_api_client import VkApiDBClient
from utils.random_values import random_values


class TestLoginPage(BaseCase):
    def test_test(self):
        self.login_page.open_page()
        time.sleep(30)


class TestDB:
    @pytest.fixture(scope='function', autouse=True)
    def start(self):
        self.vkapi_db = VkApiDBClient()
        self.myapp_db = MyappDBClient()


    def test_db1(self):
        username = 'test2'
        assert self.vkapi_db.get_vk_id(username=username) is None
        self.vkapi_db.set_vk_id(username=username, vk_id=123)
        assert self.vkapi_db.get_vk_id(username=username) == 123

    def test_db2(self):
        username = 'testuser1'
        password = 'testpsswd'
        email = 'test@test.t'
        assert self.myapp_db.get_user(username=username, password=password, email=email) is None
        self.myapp_db.create_user(username=username, password=password, email=email)
        usr = self.myapp_db.get_user(username=username, password=password, email=email)
        assert usr is not None
        assert (usr.username, usr.password, usr.email) == (username, password, email)
        password2 = 'testpsswd2'
        usr.password = password2
        usr2 = self.myapp_db.get_user(username=username, email=email)
        assert usr2 is not None
        assert usr2.password == password2
        self.myapp_db.create_user(username='testuser2', password=password, email='test3@t.t')
        self.myapp_db.create_user(username='testuser3', password=password, email='test2@t.t')
        assert len(self.myapp_db.get_all_users()) == 3
        assert len(self.myapp_db.get_users(password=password)) == 2

        new_usr = 'usr'
        dati = datetime.now()
        self.myapp_db.create_user(username=new_usr, password=password, email='test4@t.t', access=True, active=True,
                                  start_active_time=dati)
        usr3 = self.myapp_db.get_user(username=new_usr)
        assert (usr3.username, usr3.access, usr3.active, usr3.start_active_time.day) == (new_usr, True, True, dati.day)


import logging
logger = logging.getLogger(settings.TESTS.LOGGER_NAME)


class TestRandomizer:
    def test_random(self):
        logger.info(random_values.email)
        logger.info(random_values.phone_number)
        logger.info(random_values.password)

    def test_random2(self):
        logger.info(random_values.email)
        logger.info(random_values.phone_number)
        logger.info(random_values.password)
