#!/usr/bin/python3
"""
Unit tests for verifying the version of the mpesa SDK module.
"""
import mpesa
import unittest


class TestVersion(unittest.TestCase):
    def test_version(self):
        """Test the version of mpesa_sdk."""
        self.assertEqual(mpesa.__version__, "1.0.0")
