#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

# Update package lists
apt-get update

# Install Python3 and pip if not already installed
apt-get install -y python3 python3-pip

# Install required system packages
apt-get install -y nmap tcpdump net-tools

# Install Python dependencies
pip3 install -r requirements.txt

# Make the main script executable
chmod +x Rafo.py

echo "Installation complete! You can now run Rafo with: sudo python3 Rafo.py" 
