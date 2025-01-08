#!/usr/bin/python3
import unittest
from pydantic import ValidationError
from mpesa.payments.models import RegisterURLRequest


class TestRegisterURLRequest(unittest.TestCase):
    def setUp(self):
        """
        Set up valid payload for the tests.
        """
        self.valid_payload = {
            "ShortCode": "123456",
            "ResponseType": "Completed",
            "CommandID": "RegisterURL",
            "ConfirmationURL": "https://example.com/confirmation",
            "ValidationURL": "https://example.com/validation"
        }

    def test_valid_payload(self):
        """
        Test that a valid payload successfully creates an instance.
        """
        request = RegisterURLRequest(**self.valid_payload)
        self.assertEqual(request.ShortCode, "123456")
        self.assertEqual(request.ResponseType, "Completed")
        self.assertEqual(request.CommandID, "RegisterURL")
        self.assertEqual(
            request.ConfirmationURL, "https://example.com/confirmation")
        self.assertEqual(
            request.ValidationURL, "https://example.com/validation")

    def test_invalid_short_code(self):
        """
        Test invalid ShortCode (less than 6 digits).
        """
        invalid_payload = self.valid_payload.copy()
        invalid_payload["ShortCode"] = "12345"

        with self.assertRaises(ValidationError) as context:
            RegisterURLRequest(**invalid_payload)
        self.assertIn(
            "String should match pattern '^\\d{6,}$'",
            str(context.exception))

    def test_invalid_response_type(self):
        """
        Test invalid ResponseType (not 'Completed' or 'Cancelled').
        """
        invalid_payload = self.valid_payload.copy()
        invalid_payload["ResponseType"] = "InvalidResponse"
        with self.assertRaises(ValidationError) as context:
            RegisterURLRequest(**invalid_payload)
        self.assertIn(
            "String should match pattern '^(Completed|Cancelled)$'",
            str(context.exception))

    def test_invalid_command_id(self):
        """
        Test invalid CommandID (not 'RegisterURL').
        """
        invalid_payload = self.valid_payload.copy()
        invalid_payload["CommandID"] = "InvalidCommand"
        with self.assertRaises(ValidationError) as context:
            RegisterURLRequest(**invalid_payload)
        self.assertIn(
            "String should match pattern '^RegisterURL$'",
            str(context.exception))

    def test_invalid_confirmation_url(self):
        """
        Test invalid ConfirmationURL (not a valid URL).
        """
        invalid_payload = self.valid_payload.copy()
        invalid_payload["ConfirmationURL"] = "invalid-url"
        with self.assertRaises(ValidationError) as context:
            RegisterURLRequest(**invalid_payload)
        self.assertIn(
            "Input should be a valid URL", str(context.exception))

    def test_invalid_validation_url(self):
        """
        Test invalid ValidationURL (not a valid URL).
        """
        invalid_payload = self.valid_payload.copy()
        invalid_payload["ValidationURL"] = "invalid-url"
        with self.assertRaises(ValidationError) as context:
            RegisterURLRequest(**invalid_payload)
        self.assertIn(
            "Input should be a valid URL", str(context.exception))

    def test_confirmation_url_as_string(self):
        """
        Test that ConfirmationURL is converted to a string.
        """
        request = RegisterURLRequest(**self.valid_payload)
        self.assertIsInstance(request.ConfirmationURL, str)

    def test_validation_url_as_string(self):
        """
        Test that ValidationURL is converted to a string.
        """
        request = RegisterURLRequest(**self.valid_payload)
        self.assertIsInstance(request.ValidationURL, str)


if __name__ == "__main__":
    unittest.main()
