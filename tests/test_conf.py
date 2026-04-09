"""Unit tests for files/conf.py — verify no API keys are hardcoded."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestConf:
    def test_api_keys_not_hardcoded(self):
        """API keys should not be literal strings in conf.py."""
        conf_path = os.path.join(os.path.dirname(__file__), '..', 'files', 'conf.py')
        with open(conf_path) as f:
            source = f.read()
        # Check that the old hardcoded key values are gone
        assert 'Q4wtGdNmqnaQ267zzUb2rQztDRayEISI' not in source, \
            'Shodan API key still hardcoded in conf.py'
        assert '8d53c2357c2a13' not in source, \
            'IPInfo API key still hardcoded in conf.py'

    def test_wordlist_paths_are_strings(self):
        from files import conf
        assert isinstance(conf.PASSWORDS_WORDLIST, str)
        assert isinstance(conf.SUBDOMAINS_WORDLIST, str)
        assert isinstance(conf.DIRECTORIES_WORDLIST, str)

    def test_dns_mapping_records_is_dict(self):
        from files import conf
        assert isinstance(conf.DNS_MAPPING_RECORDS, dict)
