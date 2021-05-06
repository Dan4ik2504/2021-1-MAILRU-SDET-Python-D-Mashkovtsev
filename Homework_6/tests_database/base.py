import pytest

from database.builder import DBBuilder


class DBTestsBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.database = mysql_client
        self.database_builder = DBBuilder(mysql_client)
