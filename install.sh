#!/bin/bash

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root"
    exit 1
fi

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Update package lists
echo "Updating package lists..."
apt-get update

# Install required system packages
echo "Installing system packages..."
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
    python3-cryptography

# Install ipinfo package using pip in a virtual environment
echo "Setting up virtual environment for additional packages..."
if ! command_exists python3-venv; then
    apt-get install -y python3-venv
fi

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install ipinfo package
echo "Installing ipinfo package..."
pip install ipinfo

# Make the main script executable
chmod +x Rafo.py

echo "Installation complete! You can now run Rafo with: sudo python3 Rafo.py"
echo "Note: Make sure to activate the virtual environment before running: source venv/bin/activate" 
