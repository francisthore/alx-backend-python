#!/usr/bin/env python3
"""Module to perform unit and integration tests for the GitHub client."""
import unittest
from unittest.mock import (
    MagicMock,
    Mock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class
from requests import HTTPError
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient functionality."""

    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    @patch("client.get_json")
    def test_org_retrieval(self, org_name: str,
                           mock_response: dict,
                           mocked_get: MagicMock) -> None:
        """Test if `org` method retrieves correct org data."""
        mocked_get.return_value = MagicMock(return_value=mock_response)
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), mock_response)
        mocked_get.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_endpoint(self) -> None:
        """Validate the `_public_repos_url` property logic."""
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos"
                }
            self.assertEqual(GithubOrgClient("google")._public_repos_url,
                             "https://api.github.com/users/google/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Check if `public_repos` retrieves a list of repo names correctly."""
        sample_data = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {"name": "episodes.dart", "license": {"key": "apache-2.0"}},
                {"name": "kratu", "license": {"key": "bsd-3-clause"}}
            ]
        }
        mock_get_json.return_value = sample_data["repos"]

        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = sample_data["repos_url"]
            self.assertEqual(GithubOrgClient("google").public_repos(),
                             ["episodes.dart", "kratu"])
            mock_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "apache-2.0"}}, "apache-2.0", True),
        ({"license": {"key": "mit"}}, "apache-2.0", False),
    ])
    def test_license_check(self, repo: dict,
                           license_key: str,
                           expected_result: bool) -> None:
        """Verify the `has_license` method functionality."""
        client = GithubOrgClient("example_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected_result)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient class."""

    @classmethod
    def setUpClass(cls) -> None:
        """Initialize necessary fixtures for integration tests."""
        url_payloads = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def side_effect(url):
            if url in url_payloads:
                return Mock(**{'json.return_value': url_payloads[url]})
            return HTTPError

        cls.patcher = patch("requests.get", side_effect=side_effect)
        cls.patcher.start()

    def test_public_repos(self) -> None:
        """Check if `public_repos` returns the expected repo list."""
        self.assertEqual(GithubOrgClient("google").public_repos(),
                         self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Validate filtering repos by
        `apache-2.0` license in `public_repos`."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos
            )

    @classmethod
    def tearDownClass(cls) -> None:
        """Clean up any initialized resources after tests."""
        cls.patcher.stop()
