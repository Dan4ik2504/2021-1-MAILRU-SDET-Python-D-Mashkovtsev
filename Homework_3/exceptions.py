# Base exceptions

class CacheException(Exception):
    """
    Thrown when no cache is created or loaded from a cache file
    """


class TestException(Exception):
    """
    Base test exception
    """


# Response exceptions

class InvalidResponse(TestException):
    """
    Thrown when server response is invalid
    """


class ResponseUnserializableToJSON(InvalidResponse):
    """
    Thrown when server response unserializable to JSON
    """


# Authorization exceptions

class AuthorizationException(TestException):
    """
    Authorization test exception
    """


class LoginError(AuthorizationException):
    """
    Thrown when login failed
    """


class LogoutError(AuthorizationException):
    """
    Thrown when logout failed
    """


# Campaign exceptions

class CampaignException(TestException):
    """
    Campaign test exception
    """


class CampaignNotExist(CampaignException):
    """
    Thrown when campaign does not exist
    """


# Segment exceptions

class SegmentException(TestException):
    """
    Segment test exception
    """


class SegmentNotExists(SegmentException):
    """
    Thrown when segment does not exist
    """