#!/bin/bash

# Show available options
echo "1. Debian-based (Debian, Ubuntu, Kali, ParrotOS, Pop OS, Linux Mint, Deepin, Elementary OS, Zorin OS, MX Linux, etc)"
echo "2. RHEL-based (Red Hat Enterprise Linux, Fedora, CentOS, Rocky Linux, AlmaLinux, Oracle Linux, ClearOS, etc)"
echo "3. Arch-based (Arch, Black Arch, Manjaro, etc)"

read -p "Enter your distro [1/2/3]: " choice

if [ "$choice" = "1" ]; then
    # Install necessary packages for Debian-based distros
    sudo apt-get update
    sudo apt-get install -y nmap python3-pip
elif [ "$choice" = "2" ]; then
    # Install necessary packages for RHEL-based distros
    sudo dnf install -y nmap python3-pip
elif [ "$choice" = "3" ]; then
    # Install necessary packages for Arch-based distros
    sudo pacman -Sy --noconfirm nmap python3-pip
else
    echo "Invalid choice. Operation cancelled."
    exit
fi

# Install all necessary pip packages
sudo pip3 install gnureadline colorama ipaddress python-nmap ipinfo scapy shodan python-whois paramiko netfilterqueue

# Add main .py file to the system path
sudo cp Rafo.py /usr/bin/Rafo
sudo chmod +x /usr/bin/Rafo

echo "Rafo has been installed successfully!"
