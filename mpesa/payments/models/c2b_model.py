#!/usr/bin/python3

from pydantic import BaseModel, Field, HttpUrl, condecimal, validator, constr
from typing import List, Optional


class RegisterURLRequest(BaseModel):
    """
    Represents a request payload for registering M-PESA validation
    and confirmation URLs.
    """
    ShortCode: str = Field(
        ..., pattern=r'^\d{6,}$',
        description="A unique numeric identifier tagged to an M-PESA " +
        "pay bill/till number.")
    ResponseType: str = Field(
        ..., pattern=r'^(Completed|Cancelled)$',
        description="Specifies action if validation URL is unreachable. " +
        "Use 'Completed' or 'Cancelled'.")
    CommandID: str = Field(
        ..., pattern=r'^RegisterURL$',
        description="Differentiates the service from others. " +
        "Must be 'RegisterURL'.")
    ConfirmationURL: HttpUrl = Field(
        ..., description="URL to receive confirmation request upon " +
        "payment completion.")
    ValidationURL: HttpUrl = Field(
        ..., description="URL to receive validation request upon " +
        "payment submission.")

    @validator('ConfirmationURL', pre=False, always=True)
    def convert_confirmation_url_to_string(cls, value):
        """
        Convert ConfirmationURL to a string after validation.
        """
        return str(value)

    @validator('ValidationURL', pre=False, always=True)
    def convert_validation_url_to_string(cls, value):
        """
        Convert ValidationURL to a string after validation.
        """
        return str(value)


class ParameterItem(BaseModel):
    key: str = Field(
        ..., description="Key for the parameter, e.g., 'Amount'.")
    value: str = Field(
        ..., description="Value for the parameter, e.g., '500'.")


class ReferenceDataItem(BaseModel):
    key: str = Field(
        ..., description="Key for the reference data, e.g., 'AppVersion'.")
    value: str = Field(
        ..., description="Value for the reference data, e.g., 'v0.2'.")


class Initiator(BaseModel):
    identifier_type: int = Field(
        ..., description="Type of the identifier (e.g., 1 for MSISDN).")
    identifier: constr(pattern=r'^2517\d{8}$') = Field(
        ..., description="A unique numeric identifier, such as a phone number."
    )
    security_credential: str = Field(
        ..., description="A secure, encrypted string for the " +
        "initiator's credentials."
    )
    secret_key: str = Field(
        ..., description="The secret key for the initiator, used " +
        "for authentication."
    )


class Party(BaseModel):
    identifier_type: int = Field(
        ...,
        description="Type of the identifier " +
        "(e.g., 1 for MSISDN, 4 for organization).")
    identifier: constr(pattern=r'^\d{6,12}$') = Field(
        ...,
        description="A unique numeric identifier for the party."
    )
    short_code: Optional[constr(pattern=r'^\d{6,}$')] = Field(
        None,
        description="A unique numeric shortcode for the receiver " +
        "party, if applicable."
    )


class PaymentRequest(BaseModel):
    request_ref_id: constr(pattern=r'^[\w-]{36}$') = Field(
        ...,
        description="A unique reference ID for the request (UUID format)."
    )
    command_id: str = Field(
        ..., description="Command for the transaction, e.g., " +
        "'CustomerPayBillOnline'.")
    remark: Optional[str] = Field(
        None, description="Optional remarks for the transaction.")
    channel_session_id: str = Field(
        ..., description="A unique session ID for the channel.")
    source_system: str = Field(
        ..., description="The source system initiating the " +
        "transaction, e.g., 'USSD'.")
    timestamp: constr(
        pattern=r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{2}:\d{2}$'
    ) = Field(
        ..., description="ISO 8601 timestamp, " +
        "e.g., '2014-09-30T11:03:19.111+03:00'."
    )
    parameters: List[ParameterItem] = Field(
        ..., description="A list of key-value pairs for transaction " +
        "parameters."
    )
    reference_data: List[ReferenceDataItem] = Field(
        ...,
        description="A list of key-value pairs for reference data."
    )
    initiator: Initiator = Field(
        ..., description="Information about the transaction initiator.")
    primary_party: Party = Field(
        ..., description="Details about the primary party in the " +
        "transaction.")
    receiver_party: Party = Field(
        ..., description="Details about the receiver party in the " +
        "transaction.")
