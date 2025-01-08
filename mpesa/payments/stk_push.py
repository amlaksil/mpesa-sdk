#!/usr/bin/python3
import base64
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel, ValidationError
from mpesa.auth.auth import Auth
from mpesa.payments.models import STKPushPayload
from mpesa.utils.logger import get_logger
from mpesa.utils.client import APIClient
from mpesa.utils.exceptions import (
        APIError, AuthenticationError,
        TimeoutError, NetworkError, HTTPError,
        TooManyRedirects, ValidationError
        )

logger = get_logger(__name__)


class STKPush:
    """
    STKPush handles M-PESA STK push payment initiation.
    """
    def __init__(
            self, base_url: str, access_token: str,
            client: APIClient = None):
        """
        Initializes an instance of the STKPush class.

        Args:
            base_url (str): The base URL for the M-PESA API.
            access_token (str): The access token for authenticating
        API requests.
            client (APIClient, optional): A custom HTTP client.
        Defaults to an internal `APIClient` instance.
        """
        self.base_url = base_url
        self.client = client or APIClient(base_url)
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def send_stk_push(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initiates an STK Push request to the M-PESA API.

        This method validates the provided payload using the `STKPushPayload`
        model and sends the request to the API. It handles exceptions and logs
        errors if they occur.

        Args:
            payload (dict): The request body containing payment details.
        Must adhere to the `STKPushPayload` model.

        Returns:
            dict: The API response, including transaction details
        if successful or error details if an exception occurs.

        Raises:
            ValidationError: If the payload fails validation.
            APIError: For general API errors.
            AuthenticationError: If authentication fails.
            TimeoutError: For request timeouts.
            NetworkError: For network connectivity issues.
            HTTPError: For HTTP-related errors.
            TooManyRedirects: If too many redirects occur.
        """
        try:
            stk_payload = STKPushPayload(**payload)
            validated_payload = stk_payload.model_dump()
            logger.info("Payload validation successful.")
        except ValidationError as e:
            self.client.handle_exception(type(e), e, __name__)

        endpoint = "/mpesa/stkpush/v3/processrequest"
        try:
            response = self.client.post(
                    endpoint, headers=self.headers, data=validated_payload)
            logger.info(
                f"STK Push request sent successfully. Response: {response}")
            return response
        except (APIError, AuthenticationError,
                TimeoutError, NetworkError, HTTPError,
                TooManyRedirects, ValidationError) as e:
            self.client.handle_exception(type(e), e, __name__)
