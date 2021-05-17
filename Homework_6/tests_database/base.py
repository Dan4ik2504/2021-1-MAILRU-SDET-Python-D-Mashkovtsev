import pytest

from database.builder import DBBuilder
from database.client import MysqlClient


class DBTestsBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, logger, sqlalchemy_logs):
        self.database: MysqlClient = mysql_client
        self.database_builder = DBBuilder(mysql_client)
        self.logger = logger

        self.logger.debug('Initial setup done!')
