'''
This is the Rafo configuration file. Change the configuration based on your specific needs.
API keys are loaded from environment variables or a .env file in the project root.
Copy .env.example to .env and fill in your keys.
'''

import os

# Load .env file if present (python-dotenv optional)
try:
    from dotenv import load_dotenv

    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
except ImportError:
    pass

# API KEYS — loaded from environment variables
SHODAN_API_KEY = os.environ.get('SHODAN_API_KEY', '')
IPINFO_API_KEY = os.environ.get('IPINFO_API_KEY', '')

# DEFAULT WORDLISTS
_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASSWORDS_WORDLIST = os.path.join(_base, 'files', 'txt', 'passwords.txt')
SUBDOMAINS_WORDLIST = os.path.join(_base, 'files', 'txt', 'subdomains.txt')
DIRECTORIES_WORDLIST = os.path.join(_base, 'files', 'txt', 'directories.txt')

# DEFAULT WIRELESS INTERFACE
DEFAULT_WIRELESS_INTERFACE = os.environ.get('DEFAULT_WIRELESS_INTERFACE', '')

# DNS MAPPING RECORDS DICTIONARY
DNS_MAPPING_RECORDS = {
    'www.google.com': '185.199.109.153',
    'google.com': '185.199.109.153',
}
