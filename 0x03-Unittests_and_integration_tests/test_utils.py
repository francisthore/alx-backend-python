#!/usr/bin/env python3
"""
    Unit test for the utils module
"""
import unittest
from unittest.mock import Mock, patch
from utils import access_nested_map, get_json
from parameterized import parameterized
from fixtures import TEST_PAYLOAD
import requests


class TestAccessNestedMap(unittest.TestCase):
    """
        Unittesting for the access nested map function
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
            Tests a nested map access
        """
        result = access_nested_map(nested_map, path)
        self.assertEqual(result, expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected):
        """
            Test the exception raised in access function
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
        Tests the functionality of the get json function
    """
    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """
            Tests the get json function
        """
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = TEST_PAYLOAD

        mock_get.return_value = mock_response

        url = "https://api.somedummyapi.com/payload"
        result = get_json(url)
        self.assertEqual(result, TEST_PAYLOAD)
        mock_get.assert_called_once_with(url)


if __name__ == '__main__':
    unittest.main()
