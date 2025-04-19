import os
import subprocess
import sys
import readline
from colorama import Fore, Back, Style

# Check and activate virtual environment
venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv')
if os.path.exists(venv_path):
    if sys.platform == 'win32':
        activate_script = os.path.join(venv_path, 'Scripts', 'activate')
    else:
        activate_script = os.path.join(venv_path, 'bin', 'activate')
    
    if os.path.exists(activate_script):
        # Activate virtual environment
        if sys.platform == 'win32':
            os.system(f'call {activate_script}')
        else:
            os.system(f'source {activate_script}')
    else:
        print(f'{Fore.RED}Error: Virtual environment activation script not found.{Style.RESET_ALL}')
        sys.exit(1)
else:
    print(f'{Fore.RED}Error: Virtual environment not found. Please run install.sh first.{Style.RESET_ALL}')
    sys.exit(1)

# Now import other modules after virtual environment is activated
from run import *
from welcome import welcome

hist_list = []
comm = ''

def check_root():
    if os.geteuid() != 0:
        print(f'\n{Fore.RED}Error: This script requires root privileges to run properly.{Style.RESET_ALL}')
        print(f'Please run with sudo: {Fore.YELLOW}sudo python3 Rafo.py{Style.RESET_ALL}')
        sys.exit(1)

# Loop function to read commands and act accordingly
def handleCommands():
    global hist_list
    global comm
    while True:
        try:
            comm = input(f'\nRafo > ')
            if comm.strip() == 'clear':
                subprocess.call("clear", shell=True)
            elif comm.strip() == 'history':
                if len(hist_list) > 0:
                    print('Last commands:')
                    for i in range(0, len(hist_list)):
                        print(hist_list[i])
                else:
                    print('No commands history.')
            else:
                hist_list.append(comm.strip())
                # Use subprocess.run instead of os.system for better security
                subprocess.run(['python3', 'run.py'] + comm.strip().split(), check=True)
        except KeyboardInterrupt:
            sys.exit('\n^C\n')
        except subprocess.CalledProcessError:
            print(f'{Fore.RED}Error executing command. Please check your input.{Style.RESET_ALL}')

def main():
    # Check for root privileges first
    check_root()
    
    # if no arguments are present, run the welcome() function
    if len(sys.argv) == 1:
        welcome()

    handleCommands()

if __name__ == '__main__':
    main()
