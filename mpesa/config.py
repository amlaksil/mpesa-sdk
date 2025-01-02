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
    BASE_URL = getenv('BASE_URL', 'https://apisandbox.safaricom.et')
    CLIENT_KEY = getenv('CLIENT_KEY', 'client key')
    CLIENT_SECRET = getenv('CLIENT_SECRET', 'client secret')
    TIMEOUT = getenv('TIMEOUT', '30')
