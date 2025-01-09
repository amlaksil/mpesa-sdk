#!/usr/bin/python3
import unittest
from unittest.mock import patch, MagicMock
from pydantic import ValidationError
from mpesa.payments.c2b import C2B
from mpesa.payments.models import RegisterURLRequest
from mpesa.utils.exceptions import (
    APIError, NetworkError, TimeoutError,
    AuthenticationError, HTTPError, TooManyRedirects
)


class TestC2B(unittest.TestCase):

    def setUp(self):
        """Set up a mock C2B instance and test data for use in
        each test case.
        """
        self.base_url = "https://sandbox.safaricom.et"
        self.c2b = C2B(base_url=self.base_url)
        self.api_key = "test_api_key"
        self.payload = {
            "ShortCode": "123456",
            "ResponseType": "Completed",
            "CommandID": "RegisterURL",
            "ConfirmationURL": "https://example.com/confirmation",
            "ValidationURL": "https://example.com/validation"
        }

        self.mock_client = MagicMock()
        self.c2b.client = self.mock_client

    @patch('mpesa.payments.c2b.C2B.register_url')
    def test_register_url_success(self, mock_register_url_request):
        """Test if register_url method successfully processes a
        valid payload.
        """
        mock_register_url_request.return_value = \
            {"ResponseDescription": "Success"}
        response = self.c2b.register_url(self.api_key, self.payload)
        self.assertEqual(response["ResponseDescription"], "Success")

    @patch('mpesa.payments.c2b.C2B.register_url')
    def test_register_url_api_error(self, mock_register_url_request):
        """Test if APIError is raised during API failures."""
        mock_register_url_request.side_effect = APIError(
            "API Error occurred")
        with self.assertRaises(APIError):
            self.c2b.register_url(self.api_key, self.payload)

    @patch('mpesa.payments.c2b.C2B.register_url')
    def test_register_url_validation_error(
            self, mock_register_url_request):
        """Test if a validation error occurs with an invalid payload."""
        try:
            RegisterURLRequest(**{"ShortCode": "123456"})
        except ValidationError as e:
            mock_register_url_request.side_effect = e

        with self.assertRaises(ValidationError):
            self.c2b.register_url(self.api_key, self.payload)

    @patch('mpesa.payments.c2b.C2B.register_url')
    def test_register_url_network_error(
            self, mock_register_url_request):
        """Test if a NetworkError is raised during network issues."""
        mock_register_url_request.side_effect = NetworkError(
            "Network issue")
        with self.assertRaises(NetworkError):
            self.c2b.register_url(self.api_key, self.payload)


if __name__ == "__main__":
    unittest.main()
