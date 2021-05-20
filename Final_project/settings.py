from logging import INFO as logging_level_info


class GLOBAL_LOGGING:
    LOGS_FOLDER = '/tmp/myapp_tests_logs/'
    LEVEL = logging_level_info


class MOCK_SETTINGS:
    HOST = '0.0.0.0'
    PORT = '8008'

    class LOGGING:
        LOG_FILE_PATH = '/tmp/mock_logs.log'
        LOGGER_NAME = 'vk_api_mock_logger'

    class DB:
        HOST = 'myapp_db'
        PORT = 3306
        USER = 'root'
        PASSWORD = 'pass'
        DB_NAME = 'vk_api_db'


class APP_SETTINGS:
    HOST = '0.0.0.0'
    PORT = '8080'
