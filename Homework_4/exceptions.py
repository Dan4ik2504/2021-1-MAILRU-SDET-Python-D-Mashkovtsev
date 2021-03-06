# Base exceptions

class TestException(Exception):
    """
    Base test exception
    """


# Actions exceptions

class ActionException(TestException):
    """
    Action exception
    """


class IncorrectSwipeDirection(ActionException):
    """
    Thrown when 'swipe_to' method got incorrect direction
    """


class ElementNotFound(ActionException):
    """
    Thrown when element is not found
    """


class WaitException(ActionException):
    """
    Thrown when timeout has expired
    """


# Checking exceptions

class CheckException(TestException):
    """
    Checking exception
    """


# News sources setup page exceptions

class NewsSourcesPageException(TestException):
    """
    News sources setup page exceptions
    """


class CheckedSourceNotFound(NewsSourcesPageException):
    """
    Thrown when checked source is not found
    """
