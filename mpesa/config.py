#!/usr/bin/python3
"""
Load environment variables and configure API settings
for the application.
"""
from typing import Optional, Dict
from dotenv import load_dotenv
from os import getenv, environ


class Config:
    """
    Configuration class to load and manage environment variables
    for the application from either a '.env' file or system environment.
    """
    @classmethod
    def load_config(cls, env_file: str = '.env') -> None:
        """
        Load environment variables from a specified .env file,
        but allow overriding with system environment variables.

        Args:
            env_file (str): Path to the .env file (default is '.env').
        """
        load_dotenv(env_file)

        cls.BASE_URL = getenv("BASE_URL", "https://apisandbox.safaricom.et")
        cls.TOKEN_GENERATE_ENDPOINT = getenv(
            "TOKEN_GENERATE_ENDPOINT", "/v1/token/generate")
        cls.STK_PUSH_ENDPOINT = getenv(
            "STK_PUSH_ENDPOINT", "/mpesa/stkpush/v3/processrequest")
        cls.C2B_REGISTER_URL_ENDPOINT = getenv(
            "C2B_REGISTER_URL_ENDPOINT", "/v1/c2b-register-url/register")
        cls.C2B_PAYMENTS_ENDPOINT = getenv(
            "C2B_PAYMENTS_ENDPOINT", "/v1/c2b/payments")
        cls.B2C_PAYMENT_REQUEST_ENDPOINT = getenv(
            "B2C_PAYMENT_REQUEST_ENDPOINT", "/mpesa/b2c/v1/paymentrequest")

        cls.CLIENT_KEY = getenv('CLIENT_KEY')
        cls.CLIENT_SECRET = getenv('CLIENT_SECRET')
        cls.TIMEOUT = getenv('TIMEOUT')
        cls.MPESA_LOG_DIR = getenv('MPESA_LOG_DIR')
        cls.LOG_LEVEL = getenv('LOG_LEVEL')
        cls.ENVIRONMENT = getenv('ENVIRONMENT')

    @classmethod
    def set_env_variable(cls, key: str, value: str) -> None:
        """
        Set or update an environment variable directly in the system
        environment.
        This will update both os.environ and the class-level variable.


        Args:
            key (str): The environment variable key.
            value (str): The value to set for the environment variable.
        """
        environ[key] = value
        setattr(cls, key, value)

    @classmethod
    def display_config(cls) -> Dict[str, Optional[str]]:
        """
        Return the current configuration as a dictionary for debugging
        or logging purposes.

        Returns:
            Dict[str, Optional[str]]: A dictionary containing the
        configuration key-value pairs.
        """
        config_values = {
            "BASE_URL": cls.BASE_URL,
            "TOKEN_GENERATE_ENDPOINT": cls.TOKEN_GENERATE_ENDPOINT,
            "STK_PUSH_ENDPOINT": cls.STK_PUSH_ENDPOINT,
            "C2B_REGISTER_URL_ENDPOINT": cls.C2B_REGISTER_URL_ENDPOINT,
            "C2B_PAYMENTS_ENDPOINT": cls.C2B_PAYMENTS_ENDPOINT,
            "B2C_PAYMENT_REQUEST_ENDPOINT": cls.B2C_PAYMENT_REQUEST_ENDPOINT,
            "CLIENT_KEY": cls.CLIENT_KEY,
            "CLIENT_SECRET": cls.CLIENT_SECRET,
            "TIMEOUT": cls.TIMEOUT,
            "MPESA_LOG_DIR": cls.MPESA_LOG_DIR,
            "LOG_LEVEL": cls.LOG_LEVEL,
            "ENVIRONMENT": cls.ENVIRONMENT
            }
        return config_values

    @classmethod
    def get(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get the current value of an environment variable, or return a default.

        Args:
            key (str): The environment variable key.
            default (Optional[str]): The default value to return if the
            key is not found.

        Returns:
            Optional[str]: The value of the environment variable, or the
        default value.
        """
        return getattr(cls, key, default)


# Load configuration from the .env file (or system environment)
Config.load_config()
