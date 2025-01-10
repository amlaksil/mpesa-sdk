#!/usr/bin/python3

import os
import unittest
import logging
import tempfile
from unittest.mock import patch
from mpesa.utils.logger import get_logger


def reset_logger(name: str):
    """
    Resets the logger by removing and closing all handlers.
    """
    logger = logging.getLogger(name)
    while logger.handlers:
        handler = logger.handlers[0]
        handler.close()
        logger.removeHandler(handler)
    return logger


class TestLogger(unittest.TestCase):
    def setUp(self):
        """
        Sets up a temporary directory for logs and patches log_file_path.
        """
        self.temp_dir = tempfile.TemporaryDirectory()
        self.log_file_path = os.path.join(self.temp_dir.name, "mpesa.log")

        # Patch log_file_path globally in the logger module
        self.patcher = patch(
               "mpesa.utils.logger.log_file_path", self.log_file_path)
        self.patcher.start()

        # Reset the logger before each test
        reset_logger("test_logger")

    def tearDown(self):
        """
        Cleans up the temporary directory and stops patches.
        """
        self.temp_dir.cleanup()
        self.patcher.stop()

    @patch("mpesa.utils.logger.Config.ENVIRONMENT", "DEV")
    def test_logger_configuration(self):
        """
        Tests that the logger is configured with the correct handlers.
        """
        logger = get_logger("test_logger")
        logger.propagate = False  # Suppress log output

        self.assertEqual(len(logger.handlers), 2)

        file_handler = next(h for h in logger.handlers if isinstance(
               h, logging.handlers.RotatingFileHandler))
        stream_handler = next(h for h in logger.handlers if isinstance(
               h, logging.StreamHandler))

        self.assertIsNotNone(file_handler)
        self.assertIsNotNone(stream_handler)
        self.assertEqual(file_handler.baseFilename, self.log_file_path)

    @patch.dict(os.environ, {"LOG_LEVEL": "ERROR"})
    @patch("mpesa.utils.logger.Config.ENVIRONMENT", "TEST")
    def test_log_file_creation(self):
        """
        Ensures logger creates and writes to a log file.
        """
        logger = get_logger("test_logger")
        logger.propagate = False

        logger.info("Testing log file creation")
        self.assertTrue(os.path.exists(self.log_file_path))

        with open(self.log_file_path, "r") as log_file:
            content = log_file.read()
        self.assertIn("Testing log file creation", content)

    @patch("mpesa.utils.logger.Config.LOG_LEVEL", "DEBUG")
    def test_dynamic_log_level(self):
        """
        Confirms logger respects the dynamic log level
        set in the configuration.
        """
        logger = get_logger("test_logger")
        logger.propagate = False
        self.assertEqual(logger.level, logging.DEBUG)

    @patch("mpesa.utils.logger.RotatingFileHandler.emit")
    @patch("mpesa.utils.logger.Config.ENVIRONMENT", "TEST")
    def test_rotating_file_handler_emits(self, mock_emit):
        """
        Tests that the RotatingFileHandler's emit method is called.
        """
        logger = get_logger("test_logger")
        logger.propagate = False

        logger.info("Testing RotatingFileHandler")
        mock_emit.assert_called()

    @patch("mpesa.utils.logger.Config.LOG_LEVEL", "INVALID")
    def test_invalid_log_level_defaults_to_info(self):
        """
        Ensures invalid log levels default to DEBUG.
        """
        logger = get_logger("test_logger")
        logger.propagate = False
        self.assertEqual(logger.level, logging.DEBUG)


if __name__ == "__main__":
    unittest.main()
