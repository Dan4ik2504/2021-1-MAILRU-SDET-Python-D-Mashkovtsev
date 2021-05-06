from tests_database.base import DBTestsBase
from log_analyzer import log_analyzer
from database import models


class TestLoggerDataWriteInDB(DBTestsBase):

    def test_number_of_requests(self):
        response = log_analyzer.number_of_requests()
        self.database_builder.create_entry_number_of_requests(response)
        assert self.database.session.query(models.NumberOfRequests).count() >= 1

    def test_number_of_requests_by_type(self):
        response = log_analyzer.number_of_requests_by_type()
        for entry in response:
            self.database_builder.create_entry_number_of_requests_by_type(**entry)
        assert self.database.session.query(models.NumberOfRequestsByType).count() >= len(response)

    def test_most_frequent_requests(self):
        response = log_analyzer.most_frequent_requests()
        for entry in response:
            self.database_builder.create_entry_most_frequent_requests(**entry)
        assert self.database.session.query(models.MostFrequentRequests).count() >= len(response)

    def test_largest_requests(self):
        response = log_analyzer.largest_requests()
        for entry in response:
            self.database_builder.create_entry_largest_requests(**entry)
        assert self.database.session.query(models.LargestRequests).count() >= len(response)

    def test_users_by_number_of_requests(self):
        response = log_analyzer.users_by_number_of_requests()
        for entry in response:
            self.database_builder.create_entry_users_by_number_of_requests(**entry)
        assert self.database.session.query(models.UsersByNumberOfRequests).count() >= len(response)
