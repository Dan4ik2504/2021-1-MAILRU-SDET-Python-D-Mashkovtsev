class DB:
    USER = 'root'
    PASSWORD = 'pass'
    HOST = '127.0.0.1'
    PORT = 3306
    DB_NAME = 'TEST_SQL'


class LOGGING:
    BASE_TEST_DIR_LINUX = '/tmp/selenium_tests'
    BASE_TEST_DIR_WINDOWS = 'C:\\tmp\\selenium_tests'
    LOGGER_NAME = 'mysql_test'
    TEST_LOG_FILE_NAME = LOGGER_NAME + '.log'
    LOG_STRING_FORMAT = "'%(asctime)s - %(filename)-20s - %(levelname)-6s - %(message)s'"
