from tests_database.base import DBTestsBase
from log_analyzer import log_analyzer
from database import models


class TestLoggerDataWriteInDB(DBTestsBase):

    def test_number_of_requests(self):
        response = log_analyzer.number_of_requests()
        self.database_builder.create_entry_number_of_requests(response)

        table = models.NumberOfRequests
        query = self.database.session.query(table)
        assert query.count() > 0
        assert query.filter(table.count == response).count() > 0

    def test_number_of_requests_by_type(self):
        response = log_analyzer.number_of_requests_by_type()
        for entry in response:
            self.database_builder.create_entry_number_of_requests_by_type(**entry)

        table = models.NumberOfRequestsByType
        query = self.database.session.query(table)
        assert query.count() >= len(response)
        for entry in response:
            assert query.filter_by(**entry).count() > 0

    def test_most_frequent_requests(self):
        response = log_analyzer.most_frequent_requests()
        for entry in response:
            self.database_builder.create_entry_most_frequent_requests(**entry)

        table = models.MostFrequentRequests
        query = self.database.session.query(table)
        assert query.count() >= len(response)
        for entry in response:
            assert query.filter_by(**entry).count() > 0

    def test_largest_requests(self):
        response = log_analyzer.largest_requests()
        for entry in response:
            self.database_builder.create_entry_largest_requests(**entry)

        table = models.LargestRequests
        query = self.database.session.query(table)
        assert query.count() >= len(response)
        for entry in response:
            assert query.filter_by(**entry).count() > 0

    def test_users_by_number_of_requests(self):
        response = log_analyzer.users_by_number_of_requests()
        for entry in response:
            self.database_builder.create_entry_users_by_number_of_requests(**entry)

        table = models.UsersByNumberOfRequests
        query = self.database.session.query(table)
        assert query.count() >= len(response)
        for entry in response:
            assert query.filter_by(**entry).count() > 0
