#!/usr/bin/python3

import unittest
from unittest.mock import patch, MagicMock
from pydantic.v1 import ValidationError
from mpesa.auth.auth import Auth
from mpesa.auth.models import ConfigModel, TokenResponseModel
from mpesa.config import Config
from mpesa.utils.exceptions import APIError, InvalidClientIDError
from mpesa.utils.exceptions import (
        APIError,
        InvalidClientIDError,
        InvalidAuthenticationError,
        InvalidAuthorizationHeaderError,
        InvalidGrantTypeError,
        )


class TestAuth(unittest.TestCase):
    def setUp(self):
        """Set up test data and mocks."""
        self.base_url = Config.BASE_URL
        self.client_key = Config.CLIENT_KEY
        self.client_secret = Config.CLIENT_SECRET

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

    @patch('mpesa.auth.auth.APIClient.get')
    def test_get_token_validation_error(self, mock_get):
        """Test token response validation error handling."""
        mock_get.return_value = {
            "access_token": None,
            "token_type": "Bearer",
            "expires_in": "invalid"
        }
        with self.assertRaises(Exception):
            with self.assertLogs(level='WARNING') as log:
                self.auth.get_token()

                # Check if the specific warning messages occurred in the logs
                self.assertIn(
                    "Token response validation failed: 2 validation errors" +
                    "for TokenResponseModel", log.output[1])
                self.assertIn(
                    "access_token  none is not an allowed value",
                    log.output[2])
                self.assertIn(
                    "expires_in  invalid literal for int() with base " +
                    "10: 'invalid'", log.output[3])

    @patch('mpesa.auth.auth.Auth.get_token')
    def test_get_token_api_error(self, mock_get):
        """Test API error handling during token retrieval."""
        mock_get.side_effect = APIError("API error occurred.")

        with self.assertRaises(APIError):
            self.auth.get_token()

    @patch("mpesa.auth.auth.Auth.get_token")
    def test_get_token_invalid_client_id(self, mock_get):
        """Test handling of InvalidClientIDError."""
        mock_get.side_effect = InvalidClientIDError()

        with self.assertRaises(InvalidClientIDError):
            self.auth.get_token()

    @patch("mpesa.auth.auth.Auth.get_token")
    def test_get_token_invalid_authentication(self, mock_get):
        """Test token retrieval with an invalid authentication type."""
        mock_get.side_effect = InvalidAuthenticationError()

        with self.assertRaises(InvalidAuthenticationError):
            self.auth.get_token()

    @patch("mpesa.auth.auth.Auth.get_token")
    def test_get_token_invalid_authorization_header(self, mock_get):
        """Test token retrieval with an invalid client secret (password)."""
        mock_get.side_effect = InvalidAuthorizationHeaderError()

        with self.assertRaises(InvalidAuthorizationHeaderError):
            self.auth.get_token()

    @patch("mpesa.auth.auth.Auth.get_token")
    def test_get_token_invalid_grant_type(self, mock_get):
        """Test token retrieval with an invalid or empty grant type."""
        mock_get.side_effect = InvalidGrantTypeError()

        with self.assertRaises(InvalidGrantTypeError):
            self.auth.get_token()

    @patch("mpesa.auth.auth.APIClient.get")
    def test_unexpected_error(self, mock_get):
        """Test handling of unexpected exceptions."""
        mock_get.side_effect = Exception("Unexpected error.")

        with self.assertLogs("mpesa.auth.auth", level="CRITICAL") as cm:
            with self.assertRaises(Exception):
                self.auth.get_token()

            self.assertIn("Unexpected error occurred", cm.output[0])

    def test_invalid_all_params(self):
        """Ensure Auth raises ValidationError and
        logs errors for invalid parameters."""

        with self.assertRaises(ValidationError):
            with self.assertLogs(level="ERROR") as log:
                Auth(base_url="", client_key="", client_secret="")

            self.assertTrue(
                    any("Configuration validation failed: 3 validation" +
                        "errors for ConfigModel"
                        in message for message in log.output
                        ),
                    "Expected error message not found in logs"
                    )


if __name__ == "__main__":
    unittest.main()
