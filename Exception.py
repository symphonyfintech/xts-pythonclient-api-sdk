import requests
import json
from requests import exceptions
from requests.exceptions import HTTPError
from requests import ConnectTimeout, HTTPError, Timeout, ConnectionError

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
                Here we have declared all the exception and responses
    If there is any exception occurred we have this code to convey the messages
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class XTSException(Exception):
    """
    Base exception class representing a XTS client exception.

    Every specific XTS client exception is a subclass of this
    and  exposes two instance variables `.code` (HTTP error code)
    and `.message` (error text).
    """

    def __init__(self, message, code=500):
        """Initialize the exception."""
        super(XTSException, self).__init__(message)
        self.code = code


class XTSGeneralException(XTSException):
    """An unclassified, general error. Default code is 500."""

    def __init__(self, message, code=500):
        """Initialize the exception."""
        super(XTSGeneralException, self).__init__(message, code)


class XTSTokenException(XTSException):
    """Represents all token and authentication related errors. Default code is 400."""

    def __init__(self, message, code=400):
        """Initialize the exception."""
        super(XTSTokenException, self).__init__(message, code)


class XTSPermissionException(XTSException):
    """Represents permission denied exceptions for certain calls. Default code is 400."""

    def __init__(self, message, code=400):
        """Initialize the exception."""
        super(XTSPermissionException, self).__init__(message, code)


class XTSOrderException(XTSException):
    """Represents all order placement and manipulation errors. Default code is 500."""

    def __init__(self, message, code=400):
        """Initialize the exception."""
        super(XTSOrderException, self).__init__(message, code)


class XTSInputException(XTSException):
    """Represents user input errors such as missing and invalid parameters. Default code is 400."""

    def __init__(self, message, code=400):
        """Initialize the exception."""
        super(XTSInputException, self).__init__(message, code)


class XTSDataException(XTSException):
    """Represents a bad response from the backend Order Management System (OMS). Default code is 500."""

    def __init__(self, message, code=500):
        """Initialize the exception."""
        super(XTSDataException, self).__init__(message, code)


class XTSNetworkException(XTSException):
    """Represents a network issue between XTS and the backend Order Management System (OMS). Default code is 500."""

    def __init__(self, message, code=500):
        """Initialize the exception."""
        super(XTSNetworkException, self).__init__(message, code)
