"""
Example Rafo Plugin — HTTP Header Inspector
Usage: -httpheaders -host <HOST>

This demonstrates the plugin interface. Copy this file and modify it
to add your own tools without touching run.py.
"""

import requests
import sys
from colorama import Fore, Style

COMMAND = "httpheaders"
DESCRIPTION = "Inspect HTTP response headers of a host"
ARGS = [
    # Note: -host is already defined in run.py; plugins share common args.
    # Add only plugin-specific args here.
]


def run(args):
    if not args.host:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Please specify a host with -host.')
        sys.exit(1)

    for host in args.host:
        url = host if host.startswith('http') else f'http://{host}'
        try:
            print(f'[{Fore.YELLOW}?{Style.RESET_ALL}] Fetching headers from {Fore.YELLOW}{url}{Style.RESET_ALL}...')
            resp = requests.head(url, timeout=5, allow_redirects=True)
            print(f'[{Fore.GREEN}+{Style.RESET_ALL}] Status: {Fore.GREEN}{resp.status_code}{Style.RESET_ALL}')
            for k, v in resp.headers.items():
                print(f'  {Fore.CYAN}{k}{Style.RESET_ALL}: {v}')
        except requests.RequestException as e:
            print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}{e}{Style.RESET_ALL}')
