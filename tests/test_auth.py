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

    @patch('mpesa.auth.auth.APIClient.get')
    def test_get_token_success(self, mock_get):
        """Test successful token retrieval."""
        mock_response = {
            "access_token": "test_access_token",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        mock_get.return_value = mock_response

        with patch(
                'mpesa.auth.auth.TokenResponseModel'
        ) as MockTokenResponseModel:
            MockTokenResponseModel.return_value = TokenResponseModel(
                **mock_response)

            token = self.auth.get_token()

            self.assertEqual(token.access_token, "test_access_token")
            self.assertEqual(token.token_type, "Bearer")
            self.assertEqual(token.expires_in, 3600)


if __name__ == "__main__":
    unittest.main()
