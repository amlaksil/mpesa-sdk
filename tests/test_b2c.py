import unittest
from unittest.mock import MagicMock
from mpesa.payments.b2c import B2C
from pydantic import ValidationError


class TestB2C(unittest.TestCase):
    def setUp(self):
        """Set up common test variables."""
        self.base_url = "https://sandbox.safaricom.et"
        self.access_token = "test_access_token"
        self.client = MagicMock()
        self.b2c = B2C(
            base_url=self.base_url,
            access_token=self.access_token,
            client=self.client
        )

        self.valid_payload = {
            "InitiatorName": "testapi",
            "SecurityCredential": "secure_credential",
            "CommandID": "BusinessPayment",
            "Amount": 100.5,
            "PartyA": 101010,
            "PartyB": "251700100100",
            "Remarks": "Test Payment",
            "QueueTimeOutURL": "https://example.com/timeout",
            "ResultURL": "https://example.com/result",
            "Occassion": "Promotion",
        }
        self.invalid_payload = {
            **self.valid_payload,
            "Amount": -10,
        }

    def test_make_payment_validation_error(self):
        """Test validation error for invalid payload."""
        with self.assertRaises(ValidationError) as context:
            self.b2c.make_payment(self.invalid_payload)

        # Assert the ValidationError contains the expected message
        exception = context.exception
        self.assertTrue("Amount" in str(exception))
        self.assertTrue("greater than or equal to 0" in str(exception))

    def test_make_payment_success(self):
        """Test successful payment."""
        self.client.post.return_value.json.return_value = {
            "ConversationID": "AG123",
            "ResponseCode": "0",
        }
        self.b2c.make_payment(self.valid_payload)
        self.client.post.assert_called_once_with(
            '/mpesa/b2c/v1/paymentrequest',
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json',
            },
            data=self.valid_payload,
        )


if __name__ == "__main__":
    unittest.main()
