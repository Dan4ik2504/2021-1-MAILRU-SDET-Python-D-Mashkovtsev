from logging import INFO as LOG_LEVEL_INFO
from utils.paths import paths

BASE_URL = 'http://localhost'


# App settings

class DATABASE_SETTINGS:
    HOST = 'myapp_db'
    PORT = 3306
    USER = 'root'
    PASSWORD = 'pass'


class MOCK_SETTINGS:
    HOST = '0.0.0.0'
    PORT = '8008'
    URL = f'{BASE_URL}:{PORT}'
    DB_NAME = 'vk_api_db'
    TABLE_VK_ID_NAME = 'vk_id_table'


class APP_SETTINGS:
    HOST = '0.0.0.0'
    PORT = '8070'
    URL = f'{BASE_URL}:{PORT}'
