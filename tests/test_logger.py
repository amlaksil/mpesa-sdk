#!/usr/bin/python3
import os
import unittest
import logging
from unittest.mock import patch, MagicMock
from mpesa.utils.logger import get_logger, log_file_path
from mpesa.config import Config


class TestLogger(unittest.TestCase):
    """
    Test suite for the logger configuration and functionality.
    """
    def setUp(self):
        """
        Sets up a clean environment for testing by ensuring
        the log directory is empty.
        """
        self.log_dir = os.getenv(
            Config.MPESA_LOG_DIR, os.path.join(os.getcwd(), "logs"))
        self.log_file_path = log_file_path

        if os.path.exists(self.log_dir):
            for f in os.listdir(self.log_dir):
                os.remove(os.path.join(self.log_dir, f))
        else:
            os.makedirs(self.log_dir, exist_ok=True)

    def tearDown(self):
        """
        Cleans up the log directory after each test.
        """
        if os.path.exists(self.log_dir):
            for f in os.listdir(self.log_dir):
                os.remove(os.path.join(self.log_dir, f))

    @patch('mpesa.config.Config.LOG_LEVEL', logging.DEBUG)
    @patch('mpesa.config.Config.ENVIRONMENT', 'DEV')
    def test_logger_configuration(self):
        """
        Tests that the logger is configured with the correct
        handlers and file path.
        """
        logger = get_logger('test_logger')

        # Check if logger handlers are set correctly
        self.assertEqual(len(logger.handlers), 2)

        file_handler = next(h for h in logger.handlers if isinstance(
            h, logging.handlers.RotatingFileHandler))
        stream_handler = next(h for h in logger.handlers if isinstance(
            h, logging.StreamHandler))

        self.assertIsNotNone(file_handler)
        self.assertIsNotNone(stream_handler)

        self.assertEqual(file_handler.baseFilename, self.log_file_path)


if __name__ == '__main__':
    unittest.main()
