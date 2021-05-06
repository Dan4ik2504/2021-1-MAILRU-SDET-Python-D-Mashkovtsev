import os
from utils.paths import path


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


LOG_FILE_NAME = 'access.log'
LOG_FILE_PATH = os.path.join(path.repo_root, LOG_FILE_NAME)
