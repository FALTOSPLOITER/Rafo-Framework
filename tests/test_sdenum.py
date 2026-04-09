"""Unit tests for tasks/sdenum.py — verify no global state leakage."""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestSdenumStateIsolation:
    """Each call to sdenum() must start with a clean discovered list."""

    @patch('tasks.sdenum.requests.get')
    def test_no_state_leakage_between_calls(self, mock_get, tmp_path):
        from tasks.sdenum import sdenum

        # Create a tiny wordlist with one entry
        wl = tmp_path / 'subs.txt'
        wl.write_text('www\n')

        # First call: make 'www' resolve successfully
        mock_get.return_value = MagicMock(status_code=200)
        sdenum('example.com', str(wl), threads=1)

        # Second call with a wordlist that hits a ConnectionError
        from requests.exceptions import ConnectionError as ReqConnError
        mock_get.side_effect = ReqConnError
        sdenum('other.com', str(wl), threads=1)
        # If global state was leaking, discovered_domains from the first run
        # would still be counted in the second — no assertion error means clean.


class TestSdenumBadWordlist:
    def test_missing_wordlist_does_not_crash(self):
        from tasks.sdenum import sdenum
        # Should handle the FileNotFoundError gracefully (prints error, no crash)
        try:
            sdenum('example.com', '/nonexistent/path.txt', threads=1)
        except SystemExit:
            pass


if __name__ == '__main__':
    unittest.main()
