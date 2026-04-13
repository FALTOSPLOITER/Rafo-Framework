"""Unit tests for files/validate.py"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from files.validate import (
    validate_ip,
    validate_cidr,
    validate_domain,
    validate_host,
    validate_port,
    validate_port_range,
    validate_mac,
)


class TestValidateIP:
    def test_valid_ipv4(self):
        assert validate_ip('192.168.1.1')

    def test_valid_ipv6(self):
        assert validate_ip('::1')

    def test_invalid_ip(self):
        assert not validate_ip('999.999.999.999')

    def test_domain_is_not_ip(self):
        assert not validate_ip('example.com')


class TestValidateCIDR:
    def test_valid_cidr(self):
        assert validate_cidr('192.168.1.0/24')

    def test_invalid_cidr(self):
        assert not validate_cidr('not-a-cidr')


class TestValidateDomain:
    def test_valid_domain(self):
        assert validate_domain('example.com')

    def test_valid_subdomain(self):
        assert validate_domain('sub.example.com')

    def test_invalid_domain(self):
        assert not validate_domain('not_a_domain!')


class TestValidateHost:
    def test_ip_as_host(self):
        assert validate_host('10.0.0.1')

    def test_domain_as_host(self):
        assert validate_host('scanme.nmap.org')

    def test_cidr_as_host(self):
        assert validate_host('10.0.0.0/8')


class TestValidatePort:
    def test_valid_port(self):
        assert validate_port(80)
        assert validate_port('443')

    def test_port_zero(self):
        assert not validate_port(0)

    def test_port_too_high(self):
        assert not validate_port(70000)


class TestValidatePortRange:
    def test_valid_range(self):
        assert validate_port_range(1, 1000)

    def test_reversed_range(self):
        assert not validate_port_range(1000, 1)

    def test_invalid_ports(self):
        assert not validate_port_range(0, 80)


class TestValidateMAC:
    def test_valid_mac_colon(self):
        assert validate_mac('aa:bb:cc:dd:ee:ff')

    def test_valid_mac_dash(self):
        assert validate_mac('AA-BB-CC-DD-EE-FF')

    def test_invalid_mac(self):
        assert not validate_mac('not-a-mac')
