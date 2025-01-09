#!/usr/bin/python3

from pydantic import BaseModel, Field, HttpUrl, condecimal, validator
from typing import List


class TransactionReferenceItem(BaseModel):
    Key: str = Field(..., description="The key for the reference data item.")

    Value: str = Field(
        ..., description="The value associated with the reference data key.")


class STKPushPayload(BaseModel):
    """
    Represents the request body for M-PESA's STK Push (Customer to Business)
    API, used to initiate a payment request from a merchant to a customer via
    USSD Push for payment.
    """
    MerchantRequestID: str = Field(
        ..., description="A globally unique identifier for the " +
        "payment request.")
    BusinessShortCode: str = Field(
        ..., pattern=r"^\d{6}$",
        description="The business shortcode, exactly 6 digits.")
    Password: str = Field(..., description="The base64 encoded password.")
    Timestamp: str = Field(
        ..., pattern=r"^\d{14}$",
        description="The timestamp in the format " + "YYYYMMDDHHMMSS.")
    TransactionType: str = Field(
        ..., pattern=r"^(CustomerPayBillOnline|CustomerBuyGoodsOnline)$",
        description="Transaction type for M-Pesa.")
    Amount: float = Field(
        ..., ge=0, description="The transaction amount. Must " +
        "be a positive number.")
    PartyA: str = Field(
        ..., pattern=r"^2517\d{8}$",
        description="The phone number sending money in the format " +
        "2517XXXXXXXX.")
    PartyB: int = Field(
        ...,
        description="The receiving organization's shortcode, 5 to 6 digits.")
    PhoneNumber: str = Field(
        ..., pattern=r"^2517\d{8}$",
        description="The mobile number to receive the STK Pin Prompt.")
    TransactionDesc: str = Field(
        ..., max_length=13, description="Additional information/comment " +
        "for the transaction.")
    CallBackURL: HttpUrl = Field(
        ..., description="The secure URL to receive notifications " +
        "from M-Pesa API.")
    AccountReference: str = Field(
        ..., max_length=12, description="Alpha-numeric identifier of " +
        "the transaction.")
    ReferenceData: List[TransactionReferenceItem] = Field(
        ..., description="A list of key-value pairs for additional " +
        "transaction details.")

    @validator('Amount')
    def validate_amount(cls, v):
        """
        Validator for the Amount field.
        The amount must be a positive, non-zero value.

        Args:
            v (condecimal): The amount to be validated.

        Returns:
            condecimal: The validated amount.

        Raises:
            ValueError: If the amount is zero or negative.
        """
        if v <= 0:
            raise ValueError('Amount must be greater than zero')
        return v

    @validator('PartyB')
    def validate_party_b(cls, v):
        """
        Checks whether the given value for PartyB is an integer
        between 10000 and 999999, inclusive.

        Args:
            v (int): The value of PartyB to validate.

        Returns:
            int: The validated PartyB value.

        Raises:
            ValueError: If PartyB is not a 5-6 digit integer.
        """
        if not 10000 <= v <= 999999:
            raise ValueError('PartyB must be a 5-6 digit integer')
        return v

    @validator('CallBackURL', pre=False, always=True)
    def convert_callback_url_to_string(cls, value):
        """
        Convert CallBackURL to a string after validation.
        """
        return str(value)
