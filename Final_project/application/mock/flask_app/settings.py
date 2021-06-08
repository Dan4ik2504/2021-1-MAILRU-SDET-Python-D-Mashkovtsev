from logging import INFO as LOG_LEVEL_INFO
from utils.paths import paths
import os

BASE_URL = 'http://localhost'


# App settings

class DATABASE_SETTINGS:
    HOST = 'myapp_db'
    PORT = os.environ.get("MYAPP_DB_PORT", 3306)
    USER = 'root'
    PASSWORD = 'pass'


class MOCK_SETTINGS:
    HOST = '0.0.0.0'
    PORT = os.environ.get("VK_API_PORT", '8008')
    URL = f'{BASE_URL}:{PORT}'
    DB_NAME = 'vk_api_db'
    TABLE_VK_ID_NAME = 'vk_id_table'


class APP_SETTINGS:
    HOST = '0.0.0.0'
    PORT = os.environ.get("MYAPP_PROXY_PORT", '8070')
    URL = f'{BASE_URL}:{PORT}'
