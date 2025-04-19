#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

# Update package lists
apt-get update

# Install required system packages
apt-get install -y \
    python3 \
    python3-pip \
    nmap \
    tcpdump \
    net-tools \
    python3-colorama \
    python3-scapy \
    python3-nmap \
    python3-requests \
    python3-dnspython \
    python3-whois \
    python3-bs4 \
    python3-paramiko \
    python3-cryptography \
    python3-ipinfo

# Make the main script executable
chmod +x Rafo.py

echo "Installation complete! You can now run Rafo with: sudo python3 Rafo.py" 
