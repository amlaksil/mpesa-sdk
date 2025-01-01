#!/usr/bin/python3
"""
Authentication module for the M-Pesa SDK.

Provides functionality to authenticate with the M-Pesa API
and retrieve access tokens.
"""
import logging
import base64
from pydantic.v1 import ValidationError
from mpesa.auth.models import ConfigModel, TokenResponseModel
from mpesa.utils.client import APIClient
from mpesa.utils.exceptions import (
        APIError,
        InvalidClientIDError,
        InvalidAuthenticationError,
        InvalidAuthorizationHeaderError,
        InvalidGrantTypeError,
        )

logger = logging.getLogger(__name__)


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
            logger.error(f"Configuration validation failed: {e}")
            raise
        self.client = APIClient(base_url=self.config.base_url)

    def get_token(self) -> TokenResponseModel:
        """
        Fetches an access token from the M-Pesa API.

        Returns:
            TokenResponseModel: Validated response containing the access
            token and expiry time.
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
        endpoint = "/v1/token/generate"

        try:
            token_response = self.client.get(
                    endpoint,
                    headers=headers,
                    params=params
                    )
            validated_response = TokenResponseModel(**token_response)
            logger.info("Access token successfully retrieved.")
            return validated_response
        except (InvalidClientIDError,
                InvalidAuthenticationError,
                InvalidAuthorizationHeaderError,
                InvalidGrantTypeError,
                APIError) as e:
            self.handle_error(e, logger)
        except ValidationError as e:
            logger.error(f"Token response validation failed: {e}")
            raise
        except Exception as e:
            logger.critical(f"Unexpected error occurred: {e}", exc_info=True)
            raise

    def handle_error(self, error: Exception, logger: logging.Logger) -> None:
        """
        A helper method to log error messages and their mitigation.
        Args:
            error: The caught exception.
            logger: The logger instance used for logging messages.
        """
        logger.error(f"{error.__class__.__name__}: {error}")
        if getattr(error, 'mitigation', None):
            logger.info(f"Mitigation: {error.mitigation}")
