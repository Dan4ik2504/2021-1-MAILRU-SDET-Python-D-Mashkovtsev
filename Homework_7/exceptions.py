# Database exceptions

class DatabaseBaseException(Exception):
    """Database exception"""


class KeyDoesntExists(DatabaseBaseException):
    """Key does not exists in database"""


class EntryExists(DatabaseBaseException):
    """Entry with specified id already exists"""

