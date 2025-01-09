#!/usr/bin/python3
import unittest
from pydantic import ValidationError
from mpesa.payments.models import B2CRequestModel


class TestB2CRequestModel(unittest.TestCase):

    def setUp(self):
        """
        Set up valid input data for testing.
        """
        self.valid_data = {
            "InitiatorName": "testapi",
            "SecurityCredential": "iSHJEgQYt3xidNqpM/ytL5incRQISaAYX/",
            "CommandID": "BusinessPayment",
            "Amount": 12.50,
            "PartyA": 101010,
            "PartyB": "251712345678",
            "Remarks": "Test transaction",
            "QueueTimeOutURL": "https://mydomain.com/b2c/timeout",
            "ResultURL": "https://mydomain.com/b2c/result",
            "Occassion": "Disbursement"
        }

    def test_valid_data(self):
        """
        Test that valid data initializes the model without errors.
        """
        model = B2CRequestModel(**self.valid_data)
        self.assertEqual(model.Amount, 12.50)
        self.assertEqual(model.PartyB, "251712345678")

    def test_invalid_amount(self):
        """
        Test that an invalid (negative) amount raises a ValidationError.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["Amount"] = -5.0
        with self.assertRaises(ValidationError):
            B2CRequestModel(**invalid_data)

    def test_invalid_partyb_format(self):
        """
        Test that an invalid PartyB format raises a ValidationError.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["PartyB"] = "1234567890"
        with self.assertRaises(ValidationError):
            B2CRequestModel(**invalid_data)

    def test_missing_required_field(self):
        """
        Test that missing a required field raises a ValidationError.
        """
        invalid_data = self.valid_data.copy()
        del invalid_data["InitiatorName"]
        with self.assertRaises(ValidationError):
            B2CRequestModel(**invalid_data)

    def test_invalid_url_format(self):
        """
        Test that an invalid URL format raises a ValidationError.
        """
        invalid_data = self.valid_data.copy()
        invalid_data["QueueTimeOutURL"] = "invalid-url"
        with self.assertRaises(ValidationError):
            B2CRequestModel(**invalid_data)

    def test_optional_occassion(self):
        """
        Test that the Occassion field is optional.
        """
        valid_data = self.valid_data.copy()
        valid_data.pop("Occassion")
        model = B2CRequestModel(**valid_data)
        self.assertIsNone(model.Occassion)


if __name__ == "__main__":
    unittest.main()
