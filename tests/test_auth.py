#!/usr/bin/python3

import unittest
from unittest.mock import patch, MagicMock
from mpesa.auth.auth import Auth
from mpesa.auth.models import ConfigModel, TokenResponseModel
from mpesa.utils.exceptions import APIError


class TestAuth(unittest.TestCase):
    def setUp(self):
        """Set up test data and mocks."""
        self.base_url = "https://sandbox.safaricom.et"
        self.client_key = "test_client_key"
        self.client_secret = "test_client_secret"

        self.auth = Auth(
            base_url=self.base_url,
            client_key=self.client_key,
            client_secret=self.client_secret
        )

    @patch('mpesa.auth.auth.ConfigModel')
    def test_init_valid_config(self, MockConfigModel):
        """Test that the Auth class initializes with valid configuration."""
        MockConfigModel.return_value = ConfigModel(
            base_url=self.base_url,
            client_key=self.client_key,
            client_secret=self.client_secret
        )

        auth_instance = Auth(
            base_url=self.base_url,
            client_key=self.client_key,
            client_secret=self.client_secret
        )

        self.assertEqual(auth_instance.config.base_url, self.base_url)
        self.assertEqual(auth_instance.config.client_key, self.client_key)
        self.assertEqual(
                auth_instance.config.client_secret, self.client_secret)


if __name__ == "__main__":
    unittest.main()
