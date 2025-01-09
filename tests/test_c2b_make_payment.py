#!/usr/bin/python3
import unittest
from unittest.mock import patch, MagicMock
from pydantic import ValidationError
from mpesa.payments.c2b import C2B
from mpesa.payments.models import PaymentRequest
from mpesa.utils.exceptions import (
    APIError, NetworkError, TimeoutError,
    AuthenticationError, HTTPError, TooManyRedirects
)


class TestC2BMakePayment(unittest.TestCase):

    def setUp(self):
        """Set up a mock C2B instance and test data for use in
        each test case.
        """
        self.base_url = "https://sandbox.safaricom.et"
        self.c2b = C2B(base_url=self.base_url)

        self.payload = {
            "ShortCode": "123456",
            "CommandID": "CustomerPayBillOnline",
            "Amount": "500",
            "Msisdn": "254700000000",
            "BillRefNumber": "INV12345"
        }

        self.mock_client = MagicMock()
        self.c2b.client = self.mock_client

    @patch('mpesa.payments.c2b.C2B.make_payment')
    def test_make_payment_success(self, mock_make_payment):
        """Test if make_payment method successfully processes a
        valid payload.
        """
        mock_make_payment.return_value = {
            "RequestRefID": "29900fe1-ac90-45ce-9443-19eec5f31234",
            "ResponseCode": "0",
            "ResponseDesc": "The service request is processed successfully."
        }
        response = self.c2b.make_payment(self.payload)
        self.assertEqual(response["ResponseCode"], "0")
        self.assertEqual(
            response["ResponseDesc"],
            "The service request is processed successfully.")
        mock_make_payment.assert_called_once_with(self.payload)

    @patch('mpesa.payments.c2b.C2B.make_payment')
    def test_make_payment_validation_error(self, mock_make_payment):
        """Test if a validation error occurs with an invalid payload."""
        try:
            PaymentRequest(**{"ShortCode": "123456"})
        except ValidationError as e:
            mock_make_payment.side_effect = e

        with self.assertRaises(ValidationError):
            self.c2b.make_payment(self.payload)

    @patch('mpesa.payments.c2b.C2B.make_payment')
    def test_make_payment_api_error(self, mock_make_payment):
        """Test if APIError is raised during API failures."""
        mock_make_payment.side_effect = APIError("API Error occurred")
        with self.assertRaises(APIError):
            self.c2b.make_payment(self.payload)

    @patch('mpesa.payments.c2b.C2B.make_payment')
    def test_make_payment_network_error(self, mock_make_payment):
        """Test if a NetworkError is raised during network issues."""
        mock_make_payment.side_effect = NetworkError("Network issue")
        with self.assertRaises(NetworkError):
            self.c2b.make_payment(self.payload)

    @patch('mpesa.payments.c2b.C2B.make_payment')
    def test_make_payment_http_error(self, mock_make_payment):
        """Test if HTTPError is raised during HTTP failures."""
        mock_make_payment.side_effect = HTTPError("HTTP Error occurred")
        with self.assertRaises(HTTPError):
            self.c2b.make_payment(self.payload)

    @patch('mpesa.payments.c2b.C2B.make_payment')
    def test_make_payment_too_many_redirects(self, mock_make_payment):
        """Test if TooManyRedirects is raised during excessive redirects."""
        mock_make_payment.side_effect = TooManyRedirects(
            "Too many redirects occurred")
        with self.assertRaises(TooManyRedirects):
            self.c2b.make_payment(self.payload)


if __name__ == "__main__":
    unittest.main()
