#!/usr/bin/python3
"""
M-Pesa Customer-to-Business (C2B) Module

This module provides a Python SDK for integrating with M-Pesa's
Customer-to-Business (C2B) APIs, enabling businesses to facilitate
mobile payment transactions securely and efficiently.

Features:
- Registering validation and confirmation URLs to handle transaction
  notifications.
- Initiating payment requests from customers to businesses.
"""
from typing import Dict, Any
from mpesa.config import Config
from mpesa.payments.models import RegisterURLRequest, PaymentRequest
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
    Provides methods for integrating with the M-Pesa C2B API. It supports the
    registration of URLs for handling validation and confirmation notifications
    and initiating payment requests for customer-to-business transactions.
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
        endpoint = Config.C2B_REGISTER_URL_ENDPOINT
        params = {"apikey": username}
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
                f"Failed to register C2B URLs due to {str(e)}.")
            self.client.handle_exception(type(e), e, __name__)

    def make_payment(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a customer-initiated payment through the M-Pesa API.

        Args:
            payload (Dict[str, Any]): A dictionary containing the payment
        request payload data.

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
        endpoint = Config.C2B_PAYMENTS_ENDPOINT
        try:
            validated_payload = PaymentRequest(**payload).model_dump()
            response = self.client.post(
                endpoint, data=validated_payload
            )
            logger.info("Payment processed successfully.")
            return response
        except (APIError, AuthenticationError,
                TimeoutError, NetworkError, HTTPError,
                TooManyRedirects, ValidationError) as e:
            logger.error(f"Failed to process payment due to {str(e)}.")
            self.client.handle_exception(type(e), e, __name__)
