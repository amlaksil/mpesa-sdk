#!/usr/bin/python3
from mpesa.utils.logger import get_logger
from mpesa.utils.exceptions import (
        APIError, NetworkError,
        TimeoutError, AuthenticationError,
        HTTPError, TooManyRedirects,
        ValidationError
        )

logger = get_logger(__name__)


def handle_error(exception, module_name=None):
    """
    Handles different types of exceptions by logging
    the error and raising the exception.
    """

    logger = get_logger(module_name or __name__)
    if isinstance(exception, NetworkError):
        logger.error(f"Network issue: {exception}")
    elif isinstance(exception, TimeoutError):
        logger.warning(f"Request timeout: {exception}")
    elif isinstance(exception, AuthenticationError):
        logger.error(f"Authentication failure: {exception}")
    elif isinstance(exception, APIError):
        logger.error(f"General API error: {exception}")
    elif isinstance(exception, ValidationError):
        logger.error(f"Validaion error: {exception}")
    else:
        logger.critical(f"Unexpected error: {exception}")
    raise exception
