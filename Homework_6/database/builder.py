import allure
import logging

from database import models
import settings


class DBBuilder:

    def __init__(self, client):
        self.client = client
        self.logger = logging.getLogger(settings.LOGGING.LOGGER_NAME)

    @allure.step('Creating a database entry in the table "number_of_requests"')
    def create_entry_number_of_requests(self, count):
        entry = models.NumberOfRequests(count=count)
        self.client.session.add(entry)
        self.logger.info(f'Created a database entry in the table "number_of_requests". '
                         f'Count: "{count}"')
        return entry

    @allure.step('Creating a database entry in the table "number_of_requests_by_type"')
    def create_entry_number_of_requests_by_type(self, method, count):
        entry = models.NumberOfRequestsByType(method=method, count=count)
        self.client.session.add(entry)
        self.logger.info(f'Created a database entry in the table "number_of_requests_by_type". '
                         f'Method: "{method}". Count: "{count}"')
        return entry

    @allure.step('Creating a database entry in the table "most_frequent_requests"')
    def create_entry_most_frequent_requests(self, url, count):
        entry = models.MostFrequentRequests(url=url, count=count)
        self.client.session.add(entry)
        self.logger.info(f'Created a database entry in the table "most_frequent_requests". '
                         f'URL: "{url}". Count: "{count}"')
        return entry

    @allure.step('Creating a database entry in the table "largest_requests".')
    def create_entry_largest_requests(self, url, status_code, size, ip):
        entry = models.LargestRequests(url=url, status_code=status_code, size=size, ip=ip)
        self.client.session.add(entry)
        self.logger.info(f'Created a database entry in the table "largest_requests". '
                         f'URL: "{url}". Status code: "{status_code}". Size: "{size}". Ip: "{ip}"')
        return entry

    @allure.step('Creating a database entry in the table "users_by_number_of_requests"')
    def create_entry_users_by_number_of_requests(self, ip, count):
        entry = models.UsersByNumberOfRequests(ip=ip, count=count)
        self.client.session.add(entry)
        self.logger.info(f'Created a database entry in the table "users_by_number_of_requests". '
                         f'Ip: "{ip}". Count: "{count}"')
        return entry
