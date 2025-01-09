#!/usr/bin/python3
"""
Load environment variables and configure API settings
for the application.
"""
from dotenv import load_dotenv
from os import getenv


class Config:
    """
    Configuration class to load and manage environment variables
    for the application.
    """
    load_dotenv()
    BASE_URL = "https://apisandbox.safaricom.et"
    TOKEN_GENERATE_ENDPOINT = "/v1/token/generate"
    STK_PUSH_ENDPOINT = "/mpesa/stkpush/v3/processrequest"
    C2B_REGISTER_URL_ENDPOINT = "/v1/c2b-register-url/register"
    C2B_PAYMENTS_ENDPOINT = "/v1/c2b/payments"
    B2C_PAYMENT_REQUEST_ENDPOINT = "/mpesa/b2c/v1/paymentrequest"

    CLIENT_KEY = getenv('CLIENT_KEY')
    CLIENT_SECRET = getenv('CLIENT_SECRET')
    TIMEOUT = getenv('TIMEOUT')
    MPESA_LOG_DIR = getenv('MPESA_LOG_DIR')
    LOG_LEVEL = getenv('LOG_LEVEL')
    ENVIRONMENT = getenv('ENVIRONMENT')
