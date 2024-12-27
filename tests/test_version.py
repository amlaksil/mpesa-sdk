#!/usr/bin/python3
import mpesa_sdk
import unittest


class TestVersion(unittest.TestCase):
    def test_version(self):
        """Test the version of mpesa_sdk."""
        self.assertEqual(mpesa_sdk.__version__, "1.0.0")
