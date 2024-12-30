#!/usr/bin/python3
"""
HTTP client for interacting with APIs in the M-Pesa SDK.

This module provides a reusable client for interacting with RESTful APIs.
"""
import logging
import requests
from mpesa.config import Config
from mpesa.utils.exceptions import (
        APIError,
        InvalidClientIDError,
        InvalidAuthenticationError,
        InvalidAuthorizationHeaderError,
        InvalidGrantTypeError,
        )

logger = logging.getLogger(__name__)


class APIClient:
    """
    A client for making API requests.

    This class provides methods to perform GET requests
    to a specified base URL, and handles API responses, including
    error codes, using custom exceptions.
    """
    def __init__(self, base_url: str):
        """
        Initialize the APIClient instance.

        Args:
            base_url (str): The base URL for the API.
        """
        self.base_url = base_url

    def get(self, endpoint: str, headers: dict, params: dict):
        """
        Sends a GET request to the to the specified API endpoint.

        Args:
            endpoint (str): The API endpoint to query.
            headers (dict): Headers to include in the request.
            params (dict): Query parameters for the request.

        Returns:
            dict: Parsed JSON response from the API.

        Raises:
            APIError: If an error occurs during the request.
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(
                url, headers=headers,
                params=params
                )
        return self._handle_response(response)

    def _handle_response(self, response):
        """
        Handle API responses and raise appropriate exceptions for errors.

        Args:
            response (requests.Response): The HTTP response object.

        Returns:
            dict: Parsed JSON response if the request is successful.

        Raises:
            APIError: For generic API errors.
            InvalidClientIDError: If the client ID is invalid
            InvalidAuthenticationError: For authentication issues
            InvalidAuthorizationHeaderError: For invalid headers
            InvalidGrantTypeError: For incorrect grant type
            HTTPError: For non-JSON errors or unhandled HTTP errors
        """
        if response.status_code >= 400:
            try:
                error_data = response.json()
                result_code = error_data.get("resultCode")
                error_message = error_data.get(
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
                    logger.error(f"Unknown API error: {error_data}")
                    raise APIError(f"Unknown API error: {error_data}")
            except ValueError:
                logger.exception("Error parsing JSON response.")
                response.raise_for_status()
        return response.json()
