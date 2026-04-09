"""
Input validation utilities for Rafo-Framework.
Call these at task entry points to catch bad input early.
"""

import ipaddress
import re
import os
import sys
from colorama import Fore, Style


def validate_ip(ip):
    """Return True if ip is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_cidr(cidr):
    """Return True if cidr is a valid network in CIDR notation (e.g. 192.168.1.0/24)."""
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False


def validate_domain(domain):
    """Return True if domain looks like a valid hostname/domain."""
    pattern = re.compile(
        r'^(?:[a-zA-Z0-9]'
        r'(?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*'
        r'[a-zA-Z]{2,}$'
    )
    return bool(pattern.match(domain))


def validate_host(host):
    """Return True if host is a valid IP, CIDR, or domain."""
    return validate_ip(host) or validate_cidr(host) or validate_domain(host)


def validate_port(port):
    """Return True if port is a valid port number (1-65535)."""
    try:
        p = int(port)
        return 1 <= p <= 65535
    except (ValueError, TypeError):
        return False


def validate_port_range(start, end):
    """Return True if start and end form a valid port range."""
    return validate_port(start) and validate_port(end) and int(start) <= int(end)


def validate_mac(mac):
    """Return True if mac is a valid MAC address."""
    pattern = re.compile(r'^([0-9A-Fa-f]{2}[:\-]){5}[0-9A-Fa-f]{2}$')
    return bool(pattern.match(mac))


def validate_file_exists(path):
    """Return True if the file at path exists and is readable."""
    return os.path.isfile(path) and os.access(path, os.R_OK)


def abort(message):
    """Print an error and exit with code 1."""
    print(f'[{Fore.RED}!{Style.RESET_ALL}] {Fore.RED}{message}{Style.RESET_ALL}')
    sys.exit(1)
