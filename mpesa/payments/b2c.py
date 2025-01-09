#!/usr/bin/python3
"""
This module provides the implementation of the Business-to-Customer (B2C)
payment API for facilitating seamless and secure transactions between
businesses and individual customers via M-PESA. It supports a variety of
business use cases, such as:

- Salary disbursements
- Betting win payouts
- Bulk payments
- Cashback rewards
- Promotional payouts
- Loan disbursements
"""
from typing import Dict, Any
from mpesa.config import Config
from mpesa.utils.client import APIClient
from mpesa.payments.models import B2CRequestModel
from mpesa.payments.stk_push import STKPush
from mpesa.utils.logger import get_logger
from mpesa.utils.exceptions import (
        APIError, AuthenticationError,
        TimeoutError, NetworkError, HTTPError,
        TooManyRedirects, ValidationError
        )

logger = get_logger(__name__)


class B2C(STKPush):
    """
    This class provides the functionality to initiate and manage B2C payments
    via the M-PESA API. It extends the `STKPush` class to leverage shared
    features, such as API communication and authentication, while adding
    specific capabilities for B2C transactions.
    """
    def __init__(
            self, base_url: str, access_token: str, client: APIClient = None):
        """
        Initialize a B2C instance.

        Args:
            base_url (str): The base URL for the M-PESA API.
            access_token (str): Access token for authenticating API requests.
            client (APIClient, optional): Custom HTTP client.
        Defaults to an internal `APIClient`.
        """
        super().__init__(base_url, access_token, client)
        self.endpoint = Config.B2C_PAYMENT_REQUEST_ENDPOINT

    def make_payment(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Initiate a B2C payment request.

        Args:
            payload (Dict[str, Any]): Payment request data conforming
        to `B2CRequestModel`.

        Returns:
            Dict[str, Any]: API response data.

        Raises:
            APIError: If there's an error with the API call.
            AuthenticationError: If authentication fails.
            ValidationError: If the payload is invalid.
            TimeoutError: If the request times out.
            HTTPError: For HTTP-related errors.
            NetworkError: If there are connectivity issues.
        """
        try:
            b2c_payload = B2CRequestModel(**payload).model_dump()
            logger.info(
                f"Initiating B2C payment to endpoint: {self.endpoint}" +
                "with payload: {b2c_payload}"
            )

            response = self.client.post(
                self.endpoint, headers=self.headers, data=b2c_payload
            )
            logger.info(
                f"Payment request successful. Response: {response.text}")
            return response
        except (APIError, AuthenticationError,
                TimeoutError, NetworkError, HTTPError,
                TooManyRedirects, ValidationError) as e:
            self.client.handle_exception(type(e), e, __name__)
