class APIError(Exception):
    """Base class for all API errors."""
    def __init__(self, message, mitigation=None):
        super().__init__(message)
        self.mitigation = mitigation

    def __str__(self):
        return f"{self.args[0]} | Mitigation: {self.mitigation}"


class NetworkError(APIError):
    """Error for network connectivity issues."""
    def __init__(self, message="A network error occurred."):
        super().__init__(
            message, "Check your internet connection and retry.")


class TimeoutError(NetworkError):
    """Error for request timeouts."""
    def __init__(self):
        super().__init__(
            "The request timed out.", "Retry the request later.")


class HTTPError(APIError):
    """Error for HTTP-related issues."""
    def __init__(
            self, message="An HTTP error occurred.",
            mitigation="Check the response status code and API request."):
        super().__init__(message, mitigation)


class TooManyRedirects(APIError):
    """Error for excessive redirects."""
    def __init__(self,
                 message="Too many redirects occurred.",
                 mitigation="Ensure the URL is correct and check " +
                 "for redirection loops."):
        super().__init__(message, mitigation)


class AuthenticationError(APIError):
    """Error for authentication failures."""
    error_mapping = {
        "999991": "Ensure the correct client ID is used.",
        "999996": "Ensure the authentication type is Basic Auth.",
        "999997": "Ensure the authorization header is correctly formatted.",
        "999998": "Use client_credentials as the grant type."
        }

    def __init__(self, result_code, result_description):
        mitigation = self.error_mapping.get(
            result_code, "Check your authentication details and retry.")
        message = f"Authentication Error - Code: {result_code}, " +
        "Description: {result_description}"
        super().__init__(message, mitigation)


class ValidationError(APIError):
    """Error for data validation failures."""
    def __init__(self, message="Data validation error occurred."):
        super().__init__(
            message, "Ensure the data structure is correct.")
