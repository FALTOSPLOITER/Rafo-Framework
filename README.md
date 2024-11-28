
# Rafo

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![Size](https://img.shields.io/github/repo-size/medpaf/Rafo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


<p align="center">
  <br>
  <img src="htt" />
  <br>
  <br>
</p>


Rafo is a network and pentest utility that I developed so that I could perform different kinds of tasks using the same suite, instead of jumping from one tool to another.

Currently, this script can perform a variety of tasks such as **ifconfig**, **ping**, **traceroute**, **port scans** (including SYN, TCP, UDP, ACK, comprehensive scan, **host discovery** (scan for up devices on a local network), **MAC address detection** (get MAC address of a host IP on a local network), **banner grabbing**, **DNS checks** (with geolocation information), **WHOIS**, **subdomain enumeration**, **vulnerability reconnaissance**, **packet sniffing**, **MAC spoofing**, **IP spoofing**, **SYN flooding**, **deauth attack** and **brute-force attack** (beta).

Other features are still being implemented. Future implementations may include WAF detection, DNS enumeration, traffic analysis, XSS vulnerability scanner, ARP cache poisoning, DNS cache poisoning, MAC flooding, ping of death, network disassociation attack (not deauth attack), OSINT, email spoofing, exploits, some automated tasks and others.

![welcome banner rafo]()

## Contents

+ [Installation](#installation)
  - [Linux](#linux)
+ [Configuration](#configuration)
+ [How to use](#how-to-use)
  + Networking
    - [ifconfig (beta)](#ifconfig)
    - [ping](#ping)
    - [traceroute](#traceroute)
  + Footprinting
    - [Port scans](#port-scans)
    - [Host discovery (scan for devices on a local network)](#host-discovery)
    - [MAC address detection (get MAC address of a host IP on a local network)](#mac-address-detection)
    - [Application version detection (also known as banner grabbing)](#application-version-detection)
    - [DNS checks (with geolocation information)](#dns-checks)
    - [WHOIS](#whois)
    - [Subdomain enumeration](#subdomain-enumeration)
    - [Directory busting](#directory-busting)
    - [Vulnerability reconnaissance](#vulnerability-reconnaissance)
  + Offensive
    - [Packet sniffing](#packet-sniffing)
    - [MAC spoofing](#mac-spoofing)
    - [IP spoofing](#ip-spoofing)
    - [SYN flooding](#syn-flooding)
    - [Deauth attack](#deauth-attack)
    - [Brute-force attack (beta)](#brute-force-attack)
  + Others
    - [Turn on monitor/managed mode on an interface](#turn-on-monitor-or-managed-mode-on-an-interface)
    - [Automated reconnaissance (beta)](#automated-reconnaissance)
+ [Contribution](#contribution)
+ [License](#license)

## Installation

Note that currently, this script only runs well on Linux. If you try it in on Windows or macOS, it may run, but numerous errors will appear. 

This script was tested on:
- Kali Linux
- Ubuntu
- Pop!_OS

### Linux

To install the necessary packages so that the script can run withouth any problems simply run the `setup.sh` script with root privileges. Currently, this installation script is only supported on Debian, Red Hat and Arch based distros that has the apt, dnf and pacman package manager respectively (***Ubuntu***, ***Kali Linux***, ***Parrot OS***, ***Debian***, ***Pop!_OS***, ***Linux Mint***, ***Deepin***, ***Zorin OS***, ***MX Linux***, ***Elementary OS***, ***Fedora***, ***CentOS***, ***Red Hat Enterprise Linux***, ***Rocky Linux***, ***AlmaLinux***, ***Oracle Linux***, ***ClearOS***, ***Arch***, ***Black Arch***, ***Manjaro***, etc). On most systems, to install Rafo simply run the following commands:
```
git clone https://github.com/JINSPLOITER/Rafo-Framework.git
cd Rafo
sudo sh setup.sh
```
Then, simply follow the instructions.
Please ignore the error messages that appear during installation.

However, if you are using any other Linux distro with a different package manager, please install the packages manually using your distro's package manager. Depending on the specific distro used, some of the required packages to run this script might be already installed on your machine.
If you wish to know the necessary packages, look the `setup.sh` file.

After the installation, to run the program, simply navigate to the project's directory and run the `Rafo.py` file using python. Running the script as root is recommended for better performance and to avoid permission errors. The used command is the following:
```
sudo python3 Rafo.py
```

## Configuration
To make configurations, simply go to the configuration file at `files/conf.py` and edit it.

## How to use

### ifconfig
If you want to display your system's current TCP/IP network configuration, type the following command:

`-ifconfig`



### ping
To send ICMP packets to one or more hosts to check connectivity, simply type:

`-ping <HOST(s) IP/FQDN>`



### traceroute
To diagnose route paths and measure transit delays, use the `-traceroute` command:

`-traceroute <HOST IP/FQDN>`



### Port scans
Scanning ports helps detect potential security breaches by identifying the hosts connected to your network and the services running.

Multiple scan types are supported, including TCP SYN (`-scansyn`) [also known as  stealth scan], TCP Connect (`-scantcp`), UDP (`-scanudp`), TCP ACK (`-scanack`) and comprehensive scan (`-scan`).

`-scan -host <HOST(s) IP/FQDN>`

`-scan -host <HOST(s) IP/FQDN> -p <PORT(s)>`

If you wish to scan a IP range and/or port range, use one of the following commands:

`-scan -host <HOST(s) IP/FQDN> -prange <START PORT> <END PORT>`

`-scan -iprange <START IP> <END IP> -p <PORT(s)>`

`-scan -iprange <START IP> <END IP> -prange <START PORT> <END PORT>`



After this scan, it is possible to see that both 22 (SSH) and 80 (HTTP) ports are open.

### Host discovery
To look for current up devices on a given network type the following command:

`-scanlan`

Then type the network you want to scan.



### MAC address detection
To get a MAC address of one or more live hosts on the LAN, use the command:

`-getmac -host <HOST(s) IP>`



### Application version detection
Version detection, or banner grabbing, is a reconnaissance technique that retrieves a software banner information. This banner usually contains important information about a network service, including but not limited to, it’s software name and version. FTP, Web, SSH, and SMTP servers often expose vital information about the software they are running in their banner.

A banner attack usually starts off with a enumeration scan to find open ports. Once you identified a service you want to target, you can send specific packets and inspect the traffic for the specified information.

To perform banner grabbing, depending on your specific needs, type one of the following commands:

`-grab -host <HOST(s) IP/FQDN> -p <PORT(s)>`

`-grab -iprange <START IP> <END IP> -prange <START PORT> <END PORT>`

`-grab -host <HOST(s) IP/FQDN> -prange <START PORT> <END PORT>`

`-grab -iprange <START IP> <END IP> -p <PORT(s)>`



### DNS checks
This feature is similar to the well known `nslookup` command used on UNIX systems. If you want to do a DNS check, type the following:

`-ns <HOST(s) IP/FQDN>`


**Disclaimer**: Note that this feature uses IPinfo API. It is recommended to change the API key to yours as the key provided might be being used by other people. To change the API keys go to the configuration file at `files/conf.py`.

### WHOIS
WHOIS is a TCP protocol that aims to consult contact and DNS.
To request the WHOIS of one or more pages, just type:

`-whois <HOST(s) IP/PQDN>`



### Subdomain enumeration
Subdomain enumeration is the process of finding valid sub-domains for one or more domain.

Sub-domain enumeration can reveal a lot of domains/sub-domains that are in scope of a security assessment which in turn increases the chances of finding vulnerabilities.

If you wish to look for common subdomains of a domain, simply type:

`-sdenum <PQDN>`

This command uses a default wordlist to look for subdomains. However, if you want to use your own wordlist, type:

`-sdenum <PQDN> -wordlist <WORDLIST PATH>`



### Directory busting
Directory busting is the process of finding directories within a web server.

To perform this task type:

`-dirbust <HOST IP/FQDN>`

This command uses a default wordlist to look for subdomains. However, if you want to use your own wordlist, type:

`-dirbust <HOST IP/FQDN> -wordlist <WORDLIST PATH>`



### Vulnerability reconnaissance
To scan one or more hosts for vulnerabilities use the following command:

`-vulnscan -host <HOST(s) IP/FQDN>`



**Disclaimer**: Note that this feature uses Shodan API. It is recommended to change the API key to yours as the key provided might be being used by other people. To change the API keys go to the configuration file at `files/conf.py`.

### Packet sniffing
To perform packet sniffing, type:

`-sniff`


**Disclaimer**: If you want to sniff all the data that is passing through a network, first turn your wireless card or adapter to **monitor mode**.

### MAC spoofing
MAC spoofing is the generation of frames with a MAC address different from the address of the sending NIC.
To change the MAC address of an interface, issue the command:

`-macspoof -source <SOURCE MAC> -iface <INTERFACE>`



As you can see in the screenshot below, the MAC address of the interface was succesfully changed.



### IP spoofing
The objective of IP spoofing is to modify the correct source IP address so that the system to which a packet is directed cannot correctly identify the sender.

Note that this command only works on machines with unpached vulnerabilities. To performe IP spoofing on a host's specific port, use the following command:

`-ipspoof -source <SOURCE IP> <SOURCE PORT> -target <TARGET IP/FQDN> <TARGET PORT>`

If you want to use a random source IP, type the following command:

`-ipspoof -source r <SOURCE PORT> -target <TARGET IP/FQDN> <TARGET PORT>`

You can also use a random source port:

`-ipspoof -source <SOURCE IP> r -target <TARGET IP/FQDN> <TARGET PORT>`



**Disclaimer**: Please only use this for testing purposes and target your own machines.

### SYN flooding

SYN Flood is a DDoS attack method that causes direct overhead in the transport layer (layer 4) and indirect overhead in application layer (layer 7).

To attempt SYN flooding, type:

`-synflood -source <SOURCE PORT> -target <TARGET IP/FQDN> <TARGET PORT>`

If you want to use a random source port, type the following command:

`-synflood -source r -target <TARGET IP/FQDN> <TARGET PORT>`



**Disclaimer**: Please only use this for testing purposes and target your own machines.
### Deauth attack

A deauth attack is a type of wireless attack that targets communication between a router and one or more devices connected to that router. Effectively forcing the target machine to disconnect from the access point.

To do this attack, use the following command:

`-deauth -target <TARGET MAC> -gateway <GATEWAY MAC> -iface <INTERFACE>`

If you plan to attack all clients in a gateway, type:

`-deauth -target a -gateway <GATEWAY MAC> -iface <INTERFACE>`

You can also choose your default wireless interface (configured in `files/conf.py`) to perform the attack:

`-deauth -target <TARGET MAC> -gateway <GATEWAY MAC> -iface d`


After the command issued on the screenshot above, all the devices connected to that access point were disconnected and unable to reconnect while this script was running.

**Disclaimer**: To perform this attack, make sure you have a wireless card or adapter that supports **monitor mode** and turn it on before attempting a deauth attack.
Please only use this for testing purposes and target your own machines.

### Brute-force attack

A brute-force attack is an attempt to crack a password or username.

To perform brute-force attack and find common/weak credentials, type:

`-bruteforce <SERVICE> -target <TARGET IP/FQDN> -user <USERNAME>`

If you wish to use a custom wordlist, use the command:

`-bruteforce <SERVICE> -target <TARGET IP/FQDN> -user <USERNAME> -wordlist <WORDLIST PATH>`

For the time being, only the SSH service is supported.

**Disclaimer**: Note that the target server may have defensive mechanisms against this type of attack and block the attacker's attempts on guessing the password.
Please only use this for testing purposes and target your own machines.

### Automated reconnaissance

This command will automate some of the reconnaissance techniques available on this script.
To do this, type:

`-autoscan <HOST(s) IP/FQDN>`

### Turn on monitor or managed mode on an interface

Most wireless users only use their wireless cards as a station to an AP. In managed mode, the wireless card and driver software rely on a local AP in managed mode to provide connectivity to the wireless network. 

Some wireless cards also support monitor mode functionality. When configured in monitor mode, the wireless card stops transmitting data and sniffs the currently configured channel, reporting the contents of any observed packets to the host operating system. 

To turn an interface to monitor mode, use the following command:

`-mode monitor -iface <INTERFACE>`

You can also set your interface to the default wireless interface (configured in `files/conf.py`):

`-mode monitor -iface d`



As you can see in the screenshot below, the interface mode was succesfully changed.



However, if you wish to turn your interface back to managed mode, type:

`-mode managed -iface <INTERFACE>`

You can also set your interface to the default wireless interface (configured in `files/conf.py`):

`-mode managed -iface d`



As you can see in the screenshot below, the interface mode was succesfully changed.



## Contribution

Create a issue or pull request, or send me an email at [faltosploiter@gmail.com](mailto:faltosploiter@gmail.com).
## License

This repository is under the [**MIT License**](https://opensource.org/licenses/MIT).
