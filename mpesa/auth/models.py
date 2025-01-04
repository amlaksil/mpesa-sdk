#!/usr/bin/python3
"""
Data models for the M-Pesa SDK.

Defines schemas for configuration and token response validation.
"""
from pydantic.v1 import BaseModel, Field, AnyHttpUrl, validator


class ConfigModel(BaseModel):
    """
    Schema for validating API configuration parameters.

    Attributes:
        base_url (AnyHttpUrl): The base URL of the API.
        client_key (str): The client key for authentication.
        client_secret (str): The client secret for authentication.
    """
    base_url: AnyHttpUrl = Field(..., description="Base URL of the M-Pesa API")
    client_key: str = Field(..., description="Client key for authentication")
    client_secret: str = Field(
        ..., description="Client secret for authentication")

    @validator("client_key", "client_secret")
    def validate_non_empty_string(cls, value, field):
        """
        Ensure that the value is not an empty string or only whitespace.
        """
        if not value.strip():
            raise ValueError(f"{field.name} cannot be an empty string")
        return value


class TokenResponseModel(BaseModel):
    """
    Schema for validating the token response from the M-Pesa API.

    Attributes:
        access_token (str): The access token for API requests.
        token_type (str): The type of token (Bearer).
        expires_in (int): The token's expiry time in seconds.
    """
    access_token: str = Field(..., description="Access token for API requests")
    token_type: str = Field(..., description="Type of token (e.g., Bearer)")
    expires_in: int = Field(..., description="Token expiry time in seconds")

    @validator("expires_in", pre=True)
    def parse_expires_in(cls, value):
        """
        Converts expires_in to an integer if provided as a string.

        Args:
            value (str or int): The expires_in value.

        Returns:
            int: The parsed expiry time in seconds.

        Raises:
            ValueError: If the value cannot be converted to an integer.
        """
        if isinstance(value, str):
            return int(value)
        return value
