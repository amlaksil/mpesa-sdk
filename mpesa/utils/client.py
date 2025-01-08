#!/usr/bin/python3
"""
HTTP client for interacting with APIs in the M-Pesa SDK.

This module provides a reusable client for sending HTTP requests
and processing responses from RESTful APIs, with robust error handling.
"""
import logging
from typing import Dict, Any, Type
import requests
from requests.exceptions import (
    Timeout,
    HTTPError as http,
    ConnectionError,
    TooManyRedirects as many,
    RequestException
    )
from mpesa.config import Config
from mpesa.utils.logger import get_logger
from mpesa.utils.exceptions import (
        APIError, AuthenticationError,
        TimeoutError, NetworkError, HTTPError,
        TooManyRedirects, ValidationError
        )
from mpesa.utils.error_handler import handle_error

logger = get_logger(__name__)


class APIClient:
    """
    A client for making API requests.

    This class provides methods to perform GET and POST requests
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
            response.raise_for_status()
            return self._handle_get_response(response)
        except (APIError, AuthenticationError,
                TimeoutError, NetworkError, http,
                many, ValidationError) as e:
            self.handle_exception(type(e), e, __name__)

    def _handle_get_response(
            self, response: requests.Response) -> Dict[str, Any]:
        """
        Handle API responses and raise appropriate exceptions for errors.

        Args:
            response (requests.Response): The HTTP response object.

        Returns:
            Dict[str, Any]: Parsed JSON response if the request is successful.
        """
        try:
            response_data = response.json()
        except ValueError as e:
            handle_error(APIError(e))

        if "resultCode" in response_data:
            result_code = response_data.get("resultCode")
            error_message = response_data.get(
                "resultDesc", "No description provided")
            handle_error(
                AuthenticationError(result_code, error_message))
        return response_data

    def post(self, endpoint: str, headers: Dict[str, str],
             data: Dict[str, str],
             params: Dict[str, str] = {}) -> Dict[str, Any]:
        """
        Sends a POST request to the specified API endpoint.

        Args:
            endpoint (str): The API endpoint to query.
            headers (Dict[str, str]): HTTP headers to include in the
        request.
            data (Any): The request payload.

        Returns:
            Dict[str, Any]: Parsed JSON response from the API.
        """
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.post(
                    url, headers=headers, params=params,
                    json=data, timeout=self.timeout
                    )
            response.raise_for_status()
            return response.json()
        except (APIError, AuthenticationError,
                TimeoutError, NetworkError, HTTPError,
                TooManyRedirects, ValidationError) as e:
            self.handle_exception(type(e), e, __name__)

    def handle_exception(
            self, exc_type: Type[Exception], e: Exception,
            module: str) -> None:
        """
        Handles exceptions by passing the exception to the
        handle_error function.

        Args:
            exc_type (Type[Exception]): The type of the exception.
            e (Exception): The exception instance that was caught.
            module (str): The name of the module where the exception occurred.
        """
        handle_error(exc_type(str(e)), module)
