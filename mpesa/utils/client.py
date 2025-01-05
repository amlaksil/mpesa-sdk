#!/usr/bin/python3
"""
HTTP client for interacting with APIs in the M-Pesa SDK.

This module provides a reusable client for sending HTTP requests
and processing responses from RESTful APIs, with robust error handling.
"""
import asyncio
import logging
from typing import Dict, Any
import httpx
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

    This class provides methods to perform GET requests and
    authentication to a specified base URL, and handles API
    responses, including error codes, using custom exceptions.
    """
    def __init__(self, config):
        """
        Initialize the API client with base URL and credentials.

        Args:
            config: Configuration object
        """
        self.base_url = config.base_url
        self.client_key = config.client_key
        self.client_secret = config.client_secret
        self.token = None
        self.headers = {}

    def get(
            self, endpoint: str, headers: Dict[str, str],
            params: Dict[str, Any], timeout: int = 10) -> Dict[str, Any]:
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
            response = requests.get(
                url, headers=headers, params=params, timeout=timeout)
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
                logger.error(f"Unknown API error: {error_data}")
                raise APIError(f"Unknown API error: {error_data}")
        return response_data

    async def authenticate(self):
        """
        Authenticates with the M-Pesa API and retrieves an access token.

        Raises:
            Exception: If authentication fails.
        """
        try:
            auth = Auth(self.base_url, self.client_key, self.client_secret)
            auth_response = auth.get_token()
            self.token = auth_respose.access_token
            self.headers = {
                    "Authorization": f"Bear {self.token}",
                    "Content-Type": "application/json"
                    }
            logger.info("Authentication successful.")
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            raise

    async def post(
            self, endpoint: str, params: Dict[str, Any],
            payload: Dict[str, Any], timeout: int = 10) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url, headers=self.headers, params=params,
                    json=payload, timeout=timeout
                )
                response.raise_for_status()
                logger.info(f"Request to {url} successful.")
                return response.json()
            except httpx.RequestError as exc:
                logger.error(
                    f"Network error during request to {url}: {exc}")
                return {"error": str(exc)}
            except httpx.HTTPStatusError as exc:
                logger.error(
                    f"HTTP error: {exc.response.status_code} on " +
                    "{url}: {exc.response.text}"
                )
                return {"error": exc.response.text}
            except Exception as exc:
                logger.error(f"Unexpected error during request: {exc}")
                return {"error": str(exc)}
