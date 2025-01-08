#!/usr/bin/python3
import unittest
from unittest.mock import patch, MagicMock
from mpesa.payments.stk_push import STKPush
from mpesa.utils.client import APIClient
from mpesa.payments.models import STKPushPayload, TransactionReferenceItem
from pydantic import ValidationError


class TestSTKPush(unittest.TestCase):
    """Unit tests for the STKPush class."""
    def setUp(self):
        self.base_url = "https://sandbox.safaricom.co.ke"
        self.access_token = "test_access_token"
        self.short_code = "123456"
        self.pass_key = "test_pass_key"
        self.stk_push = STKPush(self.base_url, self.access_token)
        self.payload = {
            "MerchantRequestID": "12345",
            "BusinessShortCode": "123456",
            "Password": "encoded_password",
            "Timestamp": "20250108095636",
            "TransactionType": "CustomerPayBillOnline",
            "Amount": 100,
            "PartyA": "251700000000",
            "PartyB": 123456,
            "PhoneNumber": "251700000000",
            "CallBackURL": "https://callback.url",
            "AccountReference": "Test123",
            "TransactionDesc": "Payment",
            "ReferenceData": [
                {"Key": "Item", "Value": "TestItem"}
            ]
        }

    @patch.object(APIClient, 'post')
    def test_send_stk_push_successful(self, mock_post):
        """Test successful STK push request."""
        msg = f"Success. Request accepted for processing"
        mock_post.return_value = {
                "MerchantRequestID": "9cae-431a-9bb5-0e58fd6aced6",
                "CheckoutRequestID": "ws_CO_1202202404292020468057",
                "ResponseCode": "0",
                "ResponseDescription": msg,
                "CustomerMessage": msg
                }
        response = self.stk_push.send_stk_push(self.payload)

        self.assertEqual(
            response["MerchantRequestID"], "9cae-431a-9bb5-0e58fd6aced6")
        self.assertEqual(
            response["CheckoutRequestID"], "ws_CO_1202202404292020468057")
        self.assertEqual(response["ResponseCode"], "0")
        self.assertEqual(response["ResponseDescription"], msg)
        self.assertEqual(response["CustomerMessage"], msg)
        mock_post.assert_called_once()

    def test_send_stk_push_validation_error(self):
        """Test STK push with invalid payload."""
        invalid_payload = self.payload
        del invalid_payload['PhoneNumber']

        with self.assertRaises(ValidationError):
            self.stk_push.send_stk_push(invalid_payload)

    @patch.object(APIClient, 'post')
    def test_send_stk_push_api_error(self, mock_post):
        """Test API error handling in STK push request."""
        mock_post.side_effect = Exception("APIError")

        data = self.payload
        data['Password'] = 'Not_encoded_password'

        with self.assertRaises(Exception) as context:
            self.stk_push.send_stk_push(data)

        self.assertEqual(str(context.exception), "APIError")

    def test_create_payload_successful(self):
        """Test payload creation with valid data."""
        del self.payload['Password']
        del self.payload['Timestamp']
        new_payload = self.stk_push.create_payload(
            short_code=self.short_code,
            pass_key=self.pass_key,
            **self.payload
        )

        self.assertIn("Password", new_payload)
        self.assertIn("Timestamp", new_payload)


if __name__ == "__main__":
    unittest.main()
