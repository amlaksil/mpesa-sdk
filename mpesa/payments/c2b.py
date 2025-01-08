#!/usr/bin/python3
from typing import Dict, Any
from mpesa.payments.models import RegisterURLRequest
from mpesa.utils.client import APIClient
from mpesa.utils.logger import get_logger
from mpesa.utils.exceptions import (
        APIError, AuthenticationError,
        TimeoutError, NetworkError, HTTPError,
        TooManyRedirects, ValidationError
        )
logger = get_logger(__name__)


class C2B:
    """
    This class provides functionality for M-Pesa Customer-to-Business (C2B)
    integrations.
    """
    def __init__(self, base_url: str, client: APIClient = None):
        """
        Initializes the C2B class with the base URL and an optional API client.

        Args:
            base_url (str): The base URL for the M-Pesa API.
            client (APIClient, optional): An instance of the APIClient.
           If not provided, a new instance will be created.
        """
        self.base_url = base_url
        self.client = client or APIClient(base_url)

    def register_url(
            self, username: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Registers the validation and confirmation URLs with the M-Pesa API.

        This method validates the provided payload, ensuring it conforms to
        the required schema before making the API request to register the URLs.

        Args:
            username (str): The API key for authenticating the request.
            payload (Dict[str, Any]): A dictionary containing the registration
        payload data.

        Returns:
            Dict[str, Any]: The response from the M-Pesa API.

        Raises:
            APIError: If the API returns a general error.
            AuthenticationError: If authentication fails.
            TimeoutError: If the request times out.
            NetworkError: If there is a network issue.
            HTTPError: If the server returns an HTTP error.
            TooManyRedirects: If too many redirects occur.
            ValidationError: If the provided payload fails schema validation.
        """
        endpoint = "/v1/c2b-register-url/register"
        params = {f"apikey={username}"}
        try:
            validated_payload = RegisterURLRequest(**payload).model_dump()
            response = self.client.post(
                    endpoint, params=params, data=validated_payload
            )
            logger.info("Successfully registered C2B URLs.")
            return response
        except (APIError, AuthenticationError,
                TimeoutError, NetworkError, HTTPError,
                TooManyRedirects, ValidationError) as e:
            logger.error(
                f"Failed to register C2B URLs due to {type(e).__name__}.")
            self.client.handle_exception(type(e), e, __name__)
