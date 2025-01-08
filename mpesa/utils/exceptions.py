from pydantic import ValidationError as ValError


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
        message = f"Authentication Error - Code: {result_code}, " + \
            "Description: {result_description}"
        super().__init__(message, mitigation)


class ValidationError(APIError):
    """Error for handling Pydantic validation errors."""
    def __init__(self, validation_error: ValError):
        error_messages = self.format_errors(validation_error)
        super().__init__(
            "Data validation error occurred.",
            "Ensure the provided data meets the required schema."
        )
        self.validation_error = validation_error
        self.error_details = error_messages

    @staticmethod
    def format_errors(validation_error):
        """Formats the validation error details."""
        error_messages = []
        for error in validation_error.errors():
            loc = ".".join(map(str, error['loc']))
            msg = error['msg']
            error_messages.append(f"Field: {loc} | Issue: {msg}")
        return error_messages

    def __str__(self):
        """String representation with all error details."""
        formatted_errors = "\n".join(self.error_details)
        return f"{super().__str__()}\nDetails:\n{formatted_errors}"
