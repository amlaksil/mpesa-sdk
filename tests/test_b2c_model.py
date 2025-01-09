#!/usr/bin/python3
from datetime import datetime

import unittest
from pydantic import ValidationError
from mpesa.payments.models import (
    ParameterItem,
    ReferenceDataItem,
    Initiator,
    Party,
    PaymentRequest
)


class TestPayMod(unittest.TestCase):
    def setUp(self):
        """Set up common test data for reuse."""
        self.valid_parameter = {"key": "Amount", "value": "500"}
        self.valid_reference_data = {"key": "AppVersion", "value": "v0.2"}
        self.valid_initiator = {
            "identifier_type": 1,
            "identifier": "251712345678",
            "security_credential": "secure123",
            "secret_key": "secret456",
        }
        self.valid_party = {
            "identifier_type": 1,
            "identifier": "123456",
            "short_code": "654321",
        }
        self.valid_payment_request = {
            "request_ref_id": "123e4567-e89b-12d3-a456-426614174000",
            "command_id": "CustomerPayBillOnline",
            "remark": "Payment for order #1234",
            "channel_session_id": "session1234",
            "source_system": "USSD",
            "timestamp": "2025-01-09T12:30:45.123+03:00",
            "parameters": [self.valid_parameter],
            "reference_data": [self.valid_reference_data],
            "initiator": self.valid_initiator,
            "primary_party": self.valid_party,
            "receiver_party": self.valid_party,
        }

    def test_parameter_item_valid(self):
        """Test creating a valid ParameterItem."""
        item = ParameterItem(**self.valid_parameter)
        self.assertEqual(item.key, "Amount")
        self.assertEqual(item.value, "500")

    def test_parameter_item_invalid(self):
        """Test creating an invalid ParameterItem."""
        with self.assertRaises(ValidationError):
            ParameterItem(key=123, value="500")

    def test_reference_data_item_valid(self):
        """Test creating a valid ReferenceDataItem."""
        item = ReferenceDataItem(**self.valid_reference_data)
        self.assertEqual(item.key, "AppVersion")
        self.assertEqual(item.value, "v0.2")

    def test_reference_data_item_invalid(self):
        """Test creating an invalid ReferenceDataItem."""
        with self.assertRaises(ValidationError):
            ReferenceDataItem(key="AppVersion", value=123)

    def test_initiator_valid(self):
        """Test creating a valid Initiator."""
        initiator = Initiator(**self.valid_initiator)
        self.assertEqual(initiator.identifier_type, 1)
        self.assertEqual(initiator.identifier, "251712345678")

    def test_initiator_invalid(self):
        """Test creating an invalid Initiator."""
        with self.assertRaises(ValidationError):
            Initiator(
                identifier_type=1,
                identifier="invalid_number",
                security_credential="secure123",
                secret_key="secret456",
            )

    def test_party_valid(self):
        """Test creating a valid Party."""
        party = Party(**self.valid_party)
        self.assertEqual(party.identifier_type, 1)
        self.assertEqual(party.identifier, "123456")
        self.assertEqual(party.short_code, "654321")

    def test_party_invalid(self):
        """Test creating an invalid Party."""
        with self.assertRaises(ValidationError):
            Party(
                identifier_type=1,
                identifier="short",  # Too short to match regex
                short_code="invalid_short_code",  # Does not match regex
            )

    def test_payment_request_valid(self):
        """Test creating a valid PaymentRequest."""
        request = PaymentRequest(**self.valid_payment_request)
        self.assertEqual(
            request.request_ref_id, "123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(request.command_id, "CustomerPayBillOnline")
        self.assertEqual(request.remark, "Payment for order #1234")

    def test_payment_request_invalid(self):
        """Test creating an invalid PaymentRequest."""
        invalid_request = self.valid_payment_request.copy()
        invalid_request["timestamp"] = "invalid_timestamp"  # Not ISO 8601

        with self.assertRaises(ValidationError):
            PaymentRequest(**invalid_request)

    def test_payment_request_missing_field(self):
        """Test creating a PaymentRequest with a missing required field."""
        invalid_request = self.valid_payment_request.copy()
        del invalid_request["request_ref_id"]  # Missing required field

        with self.assertRaises(ValidationError):
            PaymentRequest(**invalid_request)


if __name__ == "__main__":
    unittest.main()
