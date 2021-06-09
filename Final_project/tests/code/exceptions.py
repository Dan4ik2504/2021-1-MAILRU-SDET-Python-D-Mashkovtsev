class TestException(Exception):
    """
    Base exception for tests
    """


# Randomizer exceptions

class TooManyRetries(Exception):
    """
    Too many retries
    """


# API client exceptions

class APIClientException(TestException):
    """
    Base API client exception
    """


class InvalidResponse(APIClientException):
    """
    Thrown when server response is invalid
    """


class ResponseUnserializableToJSON(InvalidResponse):
    """
    Thrown when server response unserializable to JSON
    """


# DB client exceptions

class DBClientException(TestException):
    """
    Base DB client exception
    """


class DBClientCheckingException(DBClientException):
    """
    Exception in check functions in DB client
    """


# UI exceptions

class UIException(TestException):
    """
    Base UI exception
    """


class UnsupportedBrowserType(UIException):
    """
    Unsupported browser type
    """


class CustomWaitTimeoutException(UIException):
    """
    Custom wait timeout exception
    """


class FindingException(UIException):
    """
    Finding exception
    """


class UICheckingException(UIException):
    """
    Exception in check functions
    """


class UIComparisonException(UICheckingException):
    """
    Comparison exception
    """


class UIElementNotVisibleException(UICheckingException):
    """
    Element not visible
    """


class UIElementVisibleException(UICheckingException):
    """
    Element visible
    """


class UIElementNotExistsException(UICheckingException):
    """
    Element does not exists
    """


class UIElementExistsException(UICheckingException):
    """
    Element exists
    """


class UIPageNotOpenedException(UICheckingException):
    """
    Page not opened
    """


class UIUrlComparisonException(UICheckingException):
    """
    Urls do not match
    """
