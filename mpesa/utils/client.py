#!/usr/bin/python3
"""
HTTP client for interacting with APIs in the M-Pesa SDK.

This module provides a reusable client for sending HTTP requests
and processing responses from RESTful APIs, with robust error handling.
"""
import logging
from typing import Dict, Any
import requests
from requests.exceptions import (
    Timeout,
    RequestException,
    HTTPError,
    ConnectionError
    )
from mpesa.config import Config
from mpesa.utils.logger import get_logger
from mpesa.utils.exceptions import (
        APIError,
        InvalidClientIDError,
        InvalidAuthenticationError,
        InvalidAuthorizationHeaderError,
        InvalidGrantTypeError,
        )

logger = get_logger(__name__)


class APIClient:
    """
    A client for making API requests.

    This class provides methods to perform GET requests
    to a specified base URL, and handles API responses, including
    error codes, using custom exceptions.
    """
    def __init__(self, base_url: str, timeout: int = 10):
        """
        Initialize the APIClient instance.

        Args:
            base_url (str): The base URL for the API.
            timeout (int, optional): The request timeout in seconds.
        """
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def __enter__(self):
        """
        Enter the runtime context related to this object.

        Returns:
            APIClient: The APIClient instance for use in the with statement.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the runtime context and clean up resources.
        Closes the session to release connections.
        """
        self.session.close()

    def get(
            self, endpoint: str, headers: Dict[str, str],
            params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends a GET request to the to the specified API endpoint.

        Args:
            endpoint (str): The API endpoint to query.
            headers (Dict[str, str]): HTTP headers to include in the request.
            params (Dict[str, Any]): Query parameters for the request.
            timeout (int, optional): The request timeout in seconds.
            Defaults to 10.

        Returns:
            Dict[str, Any]: Parsed JSON response from the API.

        Raises:
            APIError: For network issues, timeouts, or unexpected errors.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(
                url, headers=headers, params=params,
                timeout=self.timeout)
            return self._handle_response(response)
        except Timeout:
            logger.error(f"Request timed out for URL: {url}")
            raise APIError("The request timed out. Please try again later.")
        except ConnectionError as e:
            logger.error(f"Connection error for the URL: {url} - {str(e)}")
            raise APIError(
                "A network error occurred. Please check your connection.")
        except RequestException as e:
            logger.error(f"Unexpected error for URL: {url} - {str(e)}")
            raise APIError("An unexpected error occurred. Please try again.")

    def _handle_response(
            self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API responses and raise appropriate exceptions for errors.

        Args:
            response (requests.Response): The HTTP response object.

        Returns:
            Dict[str, Any]: Parsed JSON response if the request is successful.

        Raises:
            APIError: For generic API errors.
            InvalidClientIDError: If the client ID is invalid
            InvalidAuthenticationError: For authentication issues
            InvalidAuthorizationHeaderError: For invalid headers
            InvalidGrantTypeError: For incorrect grant type
            HTTPError: For non-JSON errors or unhandled HTTP errors
        """
        try:
            # Raises HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()
            response_data = response.json()
        except HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            raise APIError(f"HTTP error occurred: {http_err}")
        except ValueError as json_err:
            logger.error(f"Error parsing JSON response: {json_err}")
            raise APIError(
                "Failed to parse response JSON." +
                "Invalid response format.")

        if response.status_code >= 400:
            result_code = response_data.get("resultCode")
            error_message = response_data.get(
                "resultDesc", "No description provided")

            if result_code == "999991":
                raise InvalidClientIDError(error_message)
            elif result_code == "999996":
                raise InvalidAuthenticationError(error_message)
            elif result_code == "999997":
                raise InvalidAuthorizationHeaderError(error_message)
            elif result_code == "999998":
                raise InvalidGrantTypeError(error_message)
            else:
                logger.error(f"Unknown API error: {error_message}")
                raise APIError(f"Unknown API error: {error_message}")
        return response_data
