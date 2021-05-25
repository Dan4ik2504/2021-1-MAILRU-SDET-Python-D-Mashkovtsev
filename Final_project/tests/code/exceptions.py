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


class CheckingException(UIException):
    """
    Exception in check functions
    """


class ComparisonException(CheckingException):
    """
    Comparison exception
    """


class ElementNotVisibleException(CheckingException):
    """
    Element not visible
    """


class ElementVisibleException(CheckingException):
    """
    Element visible
    """


class ElementNotExistsException(CheckingException):
    """
    Element does not exists
    """


class ElementExistsException(CheckingException):
    """
    Element exists
    """


class PageNotOpenedException(CheckingException):
    """
    Page not opened
    """


class PageUrlDoesNotMatchDriverUrl(CheckingException):
    """
    Page url != driver url
    """
