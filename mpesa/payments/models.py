#!/usr/bin/python3

from pydantic.v1 import BaseModel, Field, HttpUrl, condecimal, validator
from typing import List


class ReferenceDataItem(BaseModel):
    Key: str = Field(
        ..., description="The key for the reference data item.")
    Value: str = Field(
        ..., description="The value associated with the reference data key.")


class STKPushBody(BaseModel):
    """
    STKPushBody is a Pydantic model representing the request body for M-PESA's
    STK Push (Customer to Business) API, used to initiate a payment request
    from a merchant to a customer via USSD Push for payment.
    """
    MerchantRequestID: str = Field(
        ..., description="A globally unique identifier for the " +
        "payment request.")
    BusinessShortCode: str = Field(
        ..., pattern=r"^\d{6}$",
        description="The business shortcode, exactly 6 digits.")
    Password: str = Field(..., description="The base64 encoded password.")
    Timestamp: str = Field(
        ..., pattern=r"^\d{14}$", description="The timestamp in the format " +
        "YYYYMMDDHHMMSS.")
    TransactionType: str = Field(
        ..., pattern=r"^(CustomerPayBillOnline|CustomerBuyGoodsOnline)$",
        description="Transaction type for M-Pesa.")
    Amount: float = Field(
        ..., ge=0, description="The transaction amount. Must " +
        "be a positive number.")
    PartyA: str = Field(
        ..., pattern=r"^251\d{9}$",
        description="The phone number sending money in the format " +
        "2517XXXXXXXX.")
    PartyB: str = Field(
        ..., pattern=r"^\d{5,6}$",
        description="The receiving organization's shortcode, 5 to 6 digits.")
    PhoneNumber: str = Field(
        ..., pattern=r"^254\d{9}$",
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
    ReferenceData: List[ReferenceDataItem] = Field(
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
