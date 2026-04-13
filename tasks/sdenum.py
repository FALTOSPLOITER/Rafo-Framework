import requests
import sys
from threading import Thread, Lock
from queue import Queue
from colorama import Fore, Back, Style

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


def sdenum(domain, wordlist, threads=8):

    q = Queue()
    list_lock = Lock()
    discovered_domains = []

    def scan_subdomains():
        while True:
            try:
                subdomain = q.get()
                url = f"http://{subdomain}.{domain}"
                requests.get(url, timeout=5)
            except requests.ConnectionError:
                pass
            except KeyboardInterrupt:
                sys.exit('^C')
            except Exception as e:
                print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}{e}{Style.RESET_ALL}')
            else:
                print(f'[{Fore.GREEN}+{Style.RESET_ALL}] Discovered subdomain: {Fore.GREEN}{url}{Style.RESET_ALL}')
                with list_lock:
                    discovered_domains.append(url)
            finally:
                q.task_done()

    print(f'[{Fore.YELLOW}?{Style.RESET_ALL}] Performing subdomain enumeration on {Fore.YELLOW}{domain}{Style.RESET_ALL}...\nPress CTRL-C to cancel.')

    try:
        subdomains = open(wordlist).read().splitlines()

        if TQDM_AVAILABLE:
            for subdomain in tqdm(subdomains, desc='Queuing subdomains', unit='entry'):
                q.put(subdomain)
        else:
            print(f'This might take a while. Looking for subdomains in {Fore.YELLOW}{domain}{Style.RESET_ALL}...')
            for subdomain in subdomains:
                q.put(subdomain)

        for _ in range(threads):
            worker = Thread(target=scan_subdomains)
            worker.daemon = True
            worker.start()

        q.join()

        if len(discovered_domains) > 0:
            if len(discovered_domains) == 1:
                print(f'\nScan completed. {Fore.GREEN}{len(discovered_domains)}{Style.RESET_ALL} subdomain was discovered.\n')
            else:
                print(f'\nScan completed. {Fore.GREEN}{len(discovered_domains)}{Style.RESET_ALL} subdomains were discovered.\n')
        else:
            print(f'Scan completed. No subdomains were discovered.\n')

    except KeyboardInterrupt:
        sys.exit('^C')
    except Exception as e:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}{e}{Style.RESET_ALL}')
