import pytest
from network.http_client import HttpClient
from network.mock_http_client import MockHTTPClient
from mocks.app_mock import table_last_names as mock_db_table
import settings


class BaseMockTestCase:
    mock_url = settings.MOCK_SETTINGS.URL
    mock_actions_url = settings.MOCK_SETTINGS.USER_ACTIONS_URL_BASE
    mock_actions_url_base = settings.MOCK_SETTINGS.USER_ACTIONS_URL_BASE
    truncate_mock_database = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, logger, start_mock):
        self.logger = logger
        self.http_client = HttpClient()
        self.mock_client = MockHTTPClient()
        self.mock_db = mock_db_table

        if self.truncate_mock_database:
            mock_db_table.truncate()
