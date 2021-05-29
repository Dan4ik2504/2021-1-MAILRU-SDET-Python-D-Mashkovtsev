# Database exceptions

class DatabaseBaseException(Exception):
    """Database exception"""


class KeyDoesntExists(DatabaseBaseException):
    """Key does not exists in database"""


class EntryExists(DatabaseBaseException):
    """Entry with specified id already exists"""


# Flask server exceptions

class FlaskServerException(Exception):
    """Flask server exception"""


class FlaskServerConnectionError(FlaskServerException):
    """Flask server connection error"""


# HTTP client errors (4**)

class HTTPClientError(Exception):
    """Base HTTP client error"""
    status_code = None

    def __init__(self, err_name=None, err_msg=None):
        self.err_name = err_name
        self.err_msg = err_msg


class HTTPBadRequestError(HTTPClientError):
    """Bad request (400) error"""
    status_code = 400


class HTTPNotFoundError(HTTPClientError):
    """Not found (404) error"""
    status_code = 404


class HTTPConflictError(HTTPClientError):
    """Conflict (409) error"""
    status_code = 409


# Network client exceptions

class NetworkClientException(Exception):
    """Network client exception"""


class ClientConnectionBrokenException(NetworkClientException):
    """Connection broken"""


# Response parser exceptions

class ResponseParserException(Exception):
    """HTTP response parser exception"""


class InvalidResponseError(ResponseParserException):
    """Thrown when the HTTP response is invalid"""


# Other exceptions

class WaitTimeoutException(Exception):
    """Wait timeout"""


class InvalidJSONException(Exception):
    """Invalid JSON exception"""
    err_name = 'Invalid JSON'
    status_code = 400

    def __init__(self, err_msg=None):
        self.err_msg = err_msg
