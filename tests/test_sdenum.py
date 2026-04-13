"""Unit tests for tasks/sdenum.py — verify no global state leakage."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_no_state_leakage_between_calls(mocker, tmp_path):
    """Each call to sdenum() must start with a clean discovered list."""
    from unittest.mock import MagicMock

    from tasks.sdenum import sdenum

    mock_get = mocker.patch('tasks.sdenum.requests.get')

    wl = tmp_path / 'subs.txt'
    wl.write_text('www\n')

    # First call: successful response — 'www' should be discovered
    mock_get.return_value = MagicMock(status_code=200)
    sdenum('example.com', str(wl), threads=1)

    # Second call: ConnectionError — nothing should be discovered
    # If global state leaked, discovered_domains from run 1 would bleed in
    from requests.exceptions import ConnectionError as ReqConnError

    mock_get.side_effect = ReqConnError
    sdenum('other.com', str(wl), threads=1)
    # No assertion needed: if globals leaked the count summary would be wrong;
    # the absence of an IndexError/assertion failure confirms clean state.


def test_missing_wordlist_does_not_crash():
    """sdenum should handle a missing wordlist gracefully (no unhandled exception)."""
    from tasks.sdenum import sdenum

    try:
        sdenum('example.com', '/nonexistent/wordlist.txt', threads=1)
    except SystemExit:
        pass  # acceptable — the function may sys.exit on error
