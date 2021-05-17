import allure

from tests_database.base import DBTestsBase
from log_analyzer import log_analyzer
from database import models


class TestLoggerDataWriteInDB(DBTestsBase):

    def test_number_of_requests(self):
        log_msg = 'Getting the total number of requests and writing it to the database'
        self.logger.info(log_msg)
        with allure.step(log_msg):
            response = log_analyzer.number_of_requests()
            self.database_builder.create_entry_number_of_requests(response)

        log_msg = 'Checking entries in the database'
        self.logger.info(log_msg)
        with allure.step(log_msg):
            table = models.NumberOfRequests
            query = self.database.session.query(table)
            assert query.count() > 0
            assert query.filter(table.count == response).count() > 0

    def test_number_of_requests_by_type(self):
        log_msg = 'Getting the number of requests by request method and writing it to the database'
        self.logger.info(log_msg)
        with allure.step(log_msg):
            response = log_analyzer.number_of_requests_by_type()
            for entry in response:
                self.database_builder.create_entry_number_of_requests_by_type(**entry)

        log_msg = 'Checking entries in the database'
        self.logger.info(log_msg)
        with allure.step(log_msg):
            table = models.NumberOfRequestsByType
            query = self.database.session.query(table)
            assert query.count() >= len(response)
            for entry in response:
                assert query.filter_by(**entry).count() > 0

    def test_most_frequent_requests(self):
        log_msg = 'Getting the 10 most frequent requests and writing it to the database'
        self.logger.info(log_msg)
        with allure.step(log_msg):
            response = log_analyzer.most_frequent_requests(limit=10)
            for entry in response:
                self.database_builder.create_entry_most_frequent_requests(**entry)

        log_msg = 'Checking entries in the database'
        self.logger.info(log_msg)
        with allure.step(log_msg):
            table = models.MostFrequentRequests
            query = self.database.session.query(table)
            assert query.count() >= len(response)
            for entry in response:
                assert query.filter_by(**entry).count() > 0

    def test_largest_requests(self):
        log_msg = 'Getting the 5 largest requests with status code "4**" and writing it to the database'
        self.logger.info(log_msg)
        with allure.step(log_msg):
            response = log_analyzer.largest_requests(limit=5)
            for entry in response:
                self.database_builder.create_entry_largest_requests(**entry)

        log_msg = 'Checking entries in the database'
        self.logger.info(log_msg)
        with allure.step(log_msg):
            table = models.LargestRequests
            query = self.database.session.query(table)
            assert query.count() >= len(response)
            for entry in response:
                assert query.filter_by(**entry).count() > 0

    def test_users_by_number_of_requests(self):
        log_msg = 'Getting the 5 users by number of requests with status code "5**" and writing it to the database'
        self.logger.info(log_msg)
        with allure.step(log_msg):
            response = log_analyzer.users_by_number_of_requests(limit=5)
            for entry in response:
                self.database_builder.create_entry_users_by_number_of_requests(**entry)

        log_msg = 'Checking entries in the database'
        self.logger.info(log_msg)
        with allure.step(log_msg):
            table = models.UsersByNumberOfRequests
            query = self.database.session.query(table)
            assert query.count() >= len(response)
            for entry in response:
                assert query.filter_by(**entry).count() > 0
