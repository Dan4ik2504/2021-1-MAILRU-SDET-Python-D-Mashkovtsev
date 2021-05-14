# Database exceptions

class DatabaseBaseException(Exception):
    """Database exception"""


class KeyDoesntExists(DatabaseBaseException):
    """Key does not exists in database"""


class EntryExists(DatabaseBaseException):
    """Entry with specified id already exists"""


# Application exceptions

class AppBaseException(Exception):
    """Application exception"""

class AppConnectionError(AppBaseException):
    """App connection error"""


# Stub exceptions

class StubBaseException(Exception):
    """Stub base exception"""


class StubConnectionError(StubBaseException):
    """Stub connection error"""


# Mock exceptions

class MockBaseException(Exception):
    """Mock base exception"""


class MockConnectionError(MockBaseException):
    """Mock connection error"""


# Network client exceptions

class NetworkClientException(Exception):
    """Network client exception"""


class ClientConnectionBrokenException(NetworkClientException):
    """Connection broken"""


# Other exceptions

class WaitTimeoutException(Exception):
    """Wait timeout"""
