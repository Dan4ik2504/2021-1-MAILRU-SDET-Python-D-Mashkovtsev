import logging

import settings


class VkApiBuilder:
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(settings.TESTS.LOGGER_NAME)


class UserBuilder:
    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(settings.TESTS.LOGGER_NAME)
