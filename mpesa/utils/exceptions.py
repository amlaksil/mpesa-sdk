#!/usr/bin/python3

class APIError(Exception):
    """Base class for all API errors."""
    def __init__(self, message, mitigation=None):
        super().__init__(message)
        self.mitigation = mitigation


class InvalidClientIDError(APIError):
    """Error for invalid client ID."""
    def __init__(self, message="Invalid client ID passed."):
        super().__init__(
            message, mitigation="Ensure the correct client ID is used.")


class InvalidAuthenticationError(APIError):
    """Error for invalid authentication."""
    def __init__(self, message="Invalid authentication passed."):
        super().__init__(
            message,
            mitigation="Ensure the authentication type is 'Basic Auth'.")


class InvalidAuthorizationHeaderError(APIError):
    """Error for invalid authorization header."""
    def __init__(self, message="Invalid authorization header."):
        super().__init__(
            message,
            mitigation="Ensure the authorization header" +
            "is correctly formatted.")


class InvalidGrantTypeError(APIError):
    """Error for invalid grant type."""
    def __init__(self, message="Invalid grant type provided."):
        super().__init__(
            message, mitigation="Use 'client_credentials' as the grant type.")
