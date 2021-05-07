import os
from utils.paths import paths


class COLUMN_NAMES:
    IP = "ip"
    DATE_TIME = "date_time"
    METHOD = "method"
    URL = "url"
    HTTP_VERSION = "http_version"
    STATUS_CODE = "status_code"
    SIZE = "size"
    COUNT = "count"
    TITLE = "title"
    DATA = "data"


TABLE_NAMES = [
    'number_of_requests',
    'number_of_requests_by_type',
    'most_frequent_requests',
    'largest_requests',
    'users_by_number_of_requests',
]


LOG_FILE_NAME = 'access.log'
LOG_FILE_PATH = os.path.join(paths.repo_root, LOG_FILE_NAME)
