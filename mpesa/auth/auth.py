#!/usr/bin/python3
"""
Authentication module for the M-Pesa SDK.

This module handles the authentication process required to interact with
the M-Pesa API. It is responsible for obtaining an access token that is
required for authenticating subsequent API requests.
"""
import logging
import base64
from typing import Dict, Any
from mpesa.config import Config
from mpesa.utils.logger import get_logger
from mpesa.auth.models import ConfigModel, TokenResponseModel
from mpesa.utils.client import APIClient
from mpesa.utils.exceptions import (
        APIError, AuthenticationError,
        TimeoutError, NetworkError, HTTPError,
        TooManyRedirects, ValidationError
        )
from mpesa.utils.error_handler import handle_error

logger = get_logger(__name__)


class Auth:
    """
    Handles authentication for the M-Pesa API.

    Attributes:
        config (ConfigModel): Validated configuration for the API client.
        client (APIClient): Client for communicating with the API.
    """
    def __init__(self, base_url: str, client_key: str, client_secret: str):
        """
        Initializes the Auth class with API configuration.

        Args:
            base_url (str): The base URL of the M-Pesa API.
            client_key (str): The client key for authentication.
            client_secret (str): The client secret for authentication.

        Raises:
            ValidationError: If the configuration parameters are invalid.
        """
        try:
            self.config = ConfigModel(
                    base_url=base_url,
                    client_key=client_key,
                    client_secret=client_secret
                    )
        except ValidationError as e:
            handle_error(ValidationError(e), __name__)
        self.client = APIClient(base_url=self.config.base_url)

    def get_token(self) -> Dict[str, Any]:
        """
        Fetches an access token from the M-Pesa API.

        Returns:
            Dict[str, Any]: A dictionary with the access token, token type,
            and expiration details (expires_in and valid_for).

        Raises:
            ValidationError: If the API response does not
            match the expected schema.
            APIError: If the API request fails.
            Exception: If an unexpected error occurs.
        """
        auth_string = f"{self.config.client_key}:{self.config.client_secret}"
        encoded_credentials = base64.b64encode(auth_string.encode()).decode()
        headers = {"Authorization": f"Basic {encoded_credentials}"}
        params = {"grant_type": "client_credentials"}
        endpoint = Config.TOKEN_GENERATE_ENDPOINT

        try:
            token_response = self.client.get(
                    endpoint,
                    headers=headers,
                    params=params
                    )
            validated_response = TokenResponseModel(**token_response)
            logger.info("Access token successfully retrieved.")

            valid_for = self.convert_expiry_time(
                validated_response.expires_in)

            return {
                    "access_token": validated_response.access_token,
                    "token_type": validated_response.token_type,
                    "expires_in": validated_response.expires_in,
                    "valid_for": valid_for
                }
        except (APIError, AuthenticationError,
                TimeoutError, NetworkError, HTTPError,
                TooManyRedirects, ValidationError) as e:
            self.client.handle_exception(type(e), e, __name__)

    def convert_expiry_time(self, expiry_seconds):
        """
        Converts seconds to a human-readable time format

        Args:
            expiry_seconds (int): Expiry time in seconds.

        Returns:
            str: A human-readable string representation of the expiry time.
        """
        days, remainder = divmod(expiry_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)

        readable_expiry = []
        if days > 0:
            readable_expiry.append(
                f"{days} day{'s' if days > 1 else ''}")
        if hours > 0:
            readable_expiry.append(
                f"{hours} hour{'s' if hours > 1 else ''}")
        if minutes > 0:
            readable_expiry.append(
                f"{minutes} minute{'s' if minutes > 1 else ''}")
        if seconds > 0:
            readable_expiry.append(
                f"{seconds} second{'s' if seconds > 1 else ''}")

        return ', '.join(readable_expiry) if readable_expiry else "0 seconds"
