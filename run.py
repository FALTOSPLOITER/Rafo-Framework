import argparse
import os
import sys
import ipaddress
import textwrap
from colorama import Fore, Back, Style

from files.conf import *

from tasks.ifconfig import ifconfig
from tasks.ns import ns, nsconv
from tasks.whoisinfo import whoisinfo
from tasks.sdenum import sdenum
from tasks.dirbust import dirbust
from tasks.ping import ping
from tasks.traceroute import traceroute
from tasks.banner import bannerWithPort
from tasks.scan import scanStatus, scan, scanWithPort, scanLocalDevices
from tasks.vulnscan import vulnscan
from tasks.offense.sniff import sniff
from tasks.offense.ipspoof import ipspoof
from tasks.offense.macspoof import macspoof
from tasks.offense.synflood import synflood
from tasks.getmac import getmac
from tasks.offense.deauth import deauth
from tasks.offense.bruteforce import bruteforce
from tasks.ifacemode import turn_monitor, turn_managed
from tasks.save import save
from autoscan import *
from files.plugin_loader import discover_plugins, register_plugins, dispatch_plugins

ap = argparse.ArgumentParser(description='Hawk', formatter_class=argparse.RawDescriptionHelpFormatter,
epilog=textwrap.dedent('''

Examples:
        -ifconfig
        -ping <HOST(s) IP/URL>
        -traceroute <HOST IP/URL>
        -scan -host <HOST(s) IP/URL> -prange <START PORT> <END PORT>
        -scanlan
        -getmac -host <HOST(s) IP>
        -grab -host <HOST(S) IP/URL> -p <PORT(s)>
        -ns <HOST(s) IP/URL>
        -whois <HOST(s) IP/URL>

        -sdenum <DOMAIN>
        -sdenum <DOMAIN> -wordlist <WORDLIST PATH>
        
        -dirbust <HOST IP/URL> -wordlist <WORDLIST PATH> 
        -vulnscan -host <HOST(s) IP/URL>
        -sniff
        -macspoof -source <SOURCE MAC> -iface <INTERFACE>
        -ipspoof -source <SOURCE IP> <SOURCE PORT> -target <TARGET IP/URL> <TARGET PORT>
        -synflood -source <SOURCE PORT> -target <TARGET IP/URL> <TARGET PORT>
        -deauth -target <TARGET MAC> -gateway <GATEWAY MAC> -iface <INTERFACE> 

        -bruteforce <SERVICE> -target <TARGET IP/URL> -user <USERNAME>
        -bruteforce <SERVICE> -target <TARGET IP/URL> -user <USERNAME> -wordlist <WORDLIST PATH>

        -autoscan <HOST(s) IP/URL>
        -mode <MODE> -iface <INTERFACE>

'''))

ap.add_argument('-ifconfig', action = 'store_true', 
        help = 'display current TCP/IP network configuration')
ap.add_argument('-ping', type = str,
        nargs = '+',
        help = 'send ICMP packets to a host to check connectivity.')
ap.add_argument('-traceroute',
        nargs = 1,
        help = 'diagnose route paths and measure transit delays.')
ap.add_argument('-ns', type = str,
        nargs = '+',
        help = 'obtain domain name or IP address mapping.')
ap.add_argument('-whois', type = str,
        nargs = '+',
        help = 'obtain WHOIS protocol information.')
ap.add_argument('-sdenum', type = str, 
        nargs = 1,
        help = 'perform subdomain enumeration.') 
ap.add_argument('-dirbust', type = str, 
        nargs = 1,
        help = 'perform directory busting on a host.') 
ap.add_argument('-scantcp', action = 'store_true',
        help = 'perform TCP scan for open ports')
ap.add_argument('-scanack', action = 'store_true',
        help = 'perform ACK scan for open ports')
ap.add_argument('-scansyn', action = 'store_true',
        help = 'perform SYN scan for open ports (root privileges needed)')
ap.add_argument('-scanudp', action = 'store_true',
        help = 'perform UDP scan for open ports (root privileges needed)')
ap.add_argument('-scan', action = 'store_true',
        help = 'perform comprehensive scan for open ports (root privileges needed)')
ap.add_argument('-scanlan', action = 'store_true',
        help = 'perform scan to detect local devices')
ap.add_argument('-vulnscan', action = 'store_true',
        help = 'perform vulnerabilty scan on a host')
ap.add_argument('-grab', action = 'store_true',
        help = 'perform banner grabbing')
ap.add_argument('-getmac', action = 'store_true',
        help = 'Get MAC address of a host IP address in the same LAN (root privileges needed)')
ap.add_argument('-macspoof', action = 'store_true',
        help = 'perform MAC spoofing on a target (root privileges needed)')
ap.add_argument('-ipspoof', action = 'store_true',
        help = 'perform IP spoofing on a target (root privileges needed)')
ap.add_argument('-synflood', action = 'store_true',
        help = 'perform SYN flooding on a target (root privileges needed)')
ap.add_argument('-sniff', action = 'store_true',
        help = 'perform packet sniffing (root privileges needed)')
ap.add_argument('-deauth', action = 'store_true',
        help = 'perform deauthentication attack (root privileges needed)')
ap.add_argument('-bruteforce',
        nargs=1,
        help = 'Attempt brute-force attack on a service to guess password')
ap.add_argument('-autoscan',
        nargs = '+',
        help = 'Automated reconnaissance.')
ap.add_argument('-mode', '-m', type = str,
        nargs = 1,
        help = 'turn on specified mode (root privileges needed)')
ap.add_argument('-s', type = str,
        nargs = 1,
        help = 'save output as file to the specified path.')

ap.add_argument('-host', type = str,
        nargs = '+',
        help = 'specify one or more hosts')
ap.add_argument('-iprange', type = str,
        nargs = 2,
        help = 'specify IP range of hosts')
ap.add_argument('-p', type = int,
        nargs = '+',
        help = 'specify one or more ports')
ap.add_argument('-prange', type = int,
        default = [1, 1000],
        nargs = 2,
        help = 'specify port range')
ap.add_argument('-source', '-src', type = str,
        nargs = '+',
        help = 'specify one source')
ap.add_argument('-target', '-trg', type = str,
        nargs = '+',
        help = 'specify one or more targets')
ap.add_argument('-gateway', '-gtw', type = str,
        nargs = '+',
        help = 'specify the gateway MAC address')
ap.add_argument('-iface', '-i', type = str,
        nargs = 1,
        help = 'specify interface')
ap.add_argument('-user', '-usr', type = str,
        nargs = 1,
        help = 'specify username')
ap.add_argument('-wordlist', '-wl', type = str,
        nargs = 1,
        help = 'specify wordlist')
ap.add_argument('-threads', type = int,
        default = 8,
        help = 'number of threads for enumeration tasks (default: 8)')
ap.add_argument('-format', type = str,
        choices = ['txt', 'json', 'csv'],
        default = 'txt',
        help = 'output file format when used with -s (default: txt)')

# Load and register plugins from plugins/ directory
_plugins = discover_plugins()
if _plugins:
    register_plugins(ap, _plugins)

args = ap.parse_args()

# --- Command Dispatch ---

if args.ifconfig:
    ifconfig()

elif args.ping:
    for host in args.ping:
        ping(host)

elif args.traceroute:
    traceroute(args.traceroute[0])

elif args.ns:
    for host in args.ns:
        ns(host, IPINFO_API_KEY)

elif args.whois:
    for host in args.whois:
        whoisinfo(host)

elif args.sdenum:
    wordlist = args.wordlist[0] if args.wordlist else SUBDOMAINS_WORDLIST
    sdenum(args.sdenum[0], wordlist, threads=args.threads)

elif args.dirbust:
    wordlist = args.wordlist[0] if args.wordlist else DIRECTORIES_WORDLIST
    dirbust(args.dirbust[0], wordlist, threads=args.threads)

elif args.scan or args.scantcp or args.scanack or args.scansyn or args.scanudp:
    if args.scantcp:
        scantype = '-sT'
    elif args.scanack:
        scantype = '-sA'
    elif args.scansyn:
        scantype = '-sS'
    elif args.scanudp:
        scantype = '-sU'
    else:
        scantype = '-sT'

    if not args.host:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}Please specify a host with -host.{Style.RESET_ALL}')
        sys.exit(1)

    prstart = args.prange[0]
    prend = args.prange[1]

    for i, host in enumerate(args.host):
        if args.p:
            for j, port in enumerate(args.p):
                scanWithPort(host, False, port, i, j, scantype)
        else:
            scan(host, False, prstart, prend, scantype)

elif args.scanlan:
    scanLocalDevices()

elif args.vulnscan:
    if not args.host:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}Please specify a host with -host.{Style.RESET_ALL}')
        sys.exit(1)
    for host in args.host:
        vulnscan(host, SHODAN_API_KEY)

elif args.grab:
    if not args.host or not args.p:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}Please specify -host and -p <PORT>.{Style.RESET_ALL}')
        sys.exit(1)
    for host in args.host:
        for port in args.p:
            bannerWithPort(host, port)

elif args.getmac:
    if not args.host:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}Please specify a host with -host.{Style.RESET_ALL}')
        sys.exit(1)
    for i, host in enumerate(args.host):
        getmac(host, i)

elif args.macspoof:
    if not args.source or not args.iface:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}Please specify -source <MAC> and -iface <INTERFACE>.{Style.RESET_ALL}')
        sys.exit(1)
    macspoof(args.source[0], args.iface[0], DEFAULT_WIRELESS_INTERFACE)

elif args.ipspoof:
    if not args.source or len(args.source) < 2 or not args.target or len(args.target) < 2:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}Please specify -source <IP> <PORT> and -target <IP> <PORT>.{Style.RESET_ALL}')
        sys.exit(1)
    ipspoof(args.source[0], args.source[1], args.target[0], args.target[1])

elif args.synflood:
    if not args.source or not args.target or len(args.target) < 2:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}Please specify -source <PORT> and -target <IP> <PORT>.{Style.RESET_ALL}')
        sys.exit(1)
    synflood(args.source[0], args.target[0], args.target[1])

elif args.sniff:
    sniff()

elif args.deauth:
    if not args.target or not args.gateway or not args.iface:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}Please specify -target <MAC>, -gateway <MAC>, and -iface <INTERFACE>.{Style.RESET_ALL}')
        sys.exit(1)
    deauth(args.target[0], args.gateway[0], args.iface[0], DEFAULT_WIRELESS_INTERFACE)

elif args.bruteforce:
    service = args.bruteforce[0]
    if not args.target or not args.user:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}Please specify -target <HOST> and -user <USERNAME>.{Style.RESET_ALL}')
        sys.exit(1)
    wordlist = args.wordlist[0] if args.wordlist else PASSWORDS_WORDLIST
    bruteforce(service, args.target[0], args.user[0], wordlist)

elif args.autoscan:
    for target in args.autoscan:
        autoscan(target)

elif args.mode:
    if not args.iface:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}Please specify -iface <INTERFACE>.{Style.RESET_ALL}')
        sys.exit(1)
    mode = args.mode[0].lower()
    iface = args.iface[0]
    if mode == 'monitor':
        turn_monitor(iface, DEFAULT_WIRELESS_INTERFACE)
    elif mode == 'managed':
        turn_managed(iface, DEFAULT_WIRELESS_INTERFACE)
    else:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}Unknown mode "{mode}". Use "monitor" or "managed".{Style.RESET_ALL}')

elif args.s:
    print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}Specify a command to save alongside -s.{Style.RESET_ALL}')

elif _plugins and dispatch_plugins(args, _plugins):
    pass  # plugin handled the command

else:
    ap.print_help()

# Handle output saving: re-run the command and capture output if -s is set
if args.s and len(sys.argv) > 3:
    cmd_parts = [a for a in sys.argv[1:] if a not in ('-s', args.s[0], '-format', getattr(args, 'format', 'txt'))]
    save(' '.join(cmd_parts), args.s[0], fmt=getattr(args, 'format', 'txt'))
