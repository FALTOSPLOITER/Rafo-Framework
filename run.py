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
        default = [1-1000], 
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
        help = 'specify wordlist
