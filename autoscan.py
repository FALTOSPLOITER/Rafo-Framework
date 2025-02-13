import sys
from files.conf import *

from tasks.ns import *
from tasks.whoisinfo import *
from tasks.scan import *
from tasks.banner import *
from tasks.vulnscan import *
from tasks.sdenum import *
from tasks.dirbust import *

def autoscan(target):
    try:
        print(f'[{Fore.YELLOW}?{Style.RESET_ALL}] Performing automated reconnaissance on {Fore.YELLOW}{target}{Style.RESET_ALL}...\n') 
        ns(target, IPINFO_API_KEY)
        whoisinfo(target)
        # save open ports on array for later banner grabbing
        open_ports = scan(target)
        vulnscan(target, SHODAN_API_KEY)
        sdenum(target, SUBDOMAINS_WORDLIST)
        dirbust(target, DIRECTORIES_WORDLIST)

    except KeyboardInterrupt:
        sys.exit()

    except Exception as e:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}{e}{Style.RESET_ALL}')
