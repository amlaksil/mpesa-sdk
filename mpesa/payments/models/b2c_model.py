#!/usr/bin/python3

from pydantic import BaseModel, Field, HttpUrl, condecimal, validator
from typing import List


class B2CRequestModel(BaseModel):
    """
    Represents a request payload for making payment
    """
    InitiatorName: str = Field(
        ..., description="API user created by the Business Administrator of " +
        "the M-PESA disbursement account.")
    SecurityCredential: str = Field(
        ..., description="Encrypted API initiator password.")
    CommandID: str = Field(
        ..., description="Defines the B2C transaction type.",
        examples=["SalaryPayment", "BusinessPayment", "PromotionPayment"])
    Amount: float = Field(
        ..., description="The amount of money being sent to the customer.",
        ge=0)
    PartyA: int = Field(
        ...,
        description="The receiving organization's shortcode, 5 to 6 digits.")

    PartyB: str = Field(
        ..., pattern=r"^2517\d{8}$",
        description="Customer mobile number to receive the amount.")

    Remarks: str = Field(
        ..., description="Additional information to be associated with the " +
        "transaction.", max_length=100)
    QueueTimeOutURL: HttpUrl = Field(
        ..., description="URL to send notification if the payment request " +
        "times out.")
    ResultURL: HttpUrl = Field(
        ..., description="URL to send notification upon processing of the " +
        "payment request.")
    Occassion: str = Field(
        None, description="Additional information to be associated with the " +
        "transaction.", max_length=100)

    @validator('QueueTimeOutURL', pre=False, always=True)
    def convert_queue_timeout_url_to_string(cls, value):
        """
        Convert QueueTimeOutURL to a string after validation.
        """
        return str(value)

    @validator('ResultURL', pre=False, always=True)
    def convert_result_url_to_string(cls, value):
        """
        Convert ResultURL to a string after validation.
        """
        return str(value)
