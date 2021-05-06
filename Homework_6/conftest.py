import pytest

from database.client import MysqlClient
import settings


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user=settings.DB.USER, password=settings.DB.PASSWORD, db_name=settings.DB.DB_NAME)
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


def is_master(config):
    return not hasattr(config, 'workerinput')


def recreate_db():
    mysql_client = MysqlClient(user=settings.DB.USER, password=settings.DB.PASSWORD, db_name=settings.DB.DB_NAME)
    mysql_client.recreate_db()

    mysql_client.connect()
    mysql_client.create_tables_for_log_analyzer()

    mysql_client.connection.close()


def pytest_configure(config):
    if is_master(config):
        recreate_db()
