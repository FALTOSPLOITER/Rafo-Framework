import os
import subprocess
import sys
import readline
from colorama import Fore, Back, Style

# --- Virtual environment bootstrap ---
# If not already inside the venv, re-exec this script using the venv Python.
_project_root = os.path.dirname(os.path.abspath(__file__))
_venv_python = os.path.join(_project_root, 'venv', 'bin', 'python3')

if os.path.exists(_venv_python) and sys.executable != _venv_python:
    os.execv(_venv_python, [_venv_python] + sys.argv)

# --- History file setup ---
_rafo_dir = os.path.join(os.path.expanduser('~'), '.rafo')
os.makedirs(_rafo_dir, exist_ok=True)
_history_file = os.path.join(_rafo_dir, 'history')

try:
    readline.read_history_file(_history_file)
except FileNotFoundError:
    pass

readline.set_history_length(1000)

# --- Imports (after venv is active) ---
from welcome import welcome


def check_root():
    if os.geteuid() != 0:
        print(f'\n{Fore.RED}Error: This script requires root privileges to run properly.{Style.RESET_ALL}')
        print(f'Please run with sudo: {Fore.YELLOW}sudo python3 Rafo.py{Style.RESET_ALL}')
        sys.exit(1)


def handleCommands():
    while True:
        try:
            comm = input(f'\nRafo > ')
            stripped = comm.strip()

            if not stripped:
                continue

            if stripped == 'clear':
                subprocess.run(['clear'])
            elif stripped == 'history':
                for i in range(1, readline.get_current_history_length() + 1):
                    print(f'  {i}  {readline.get_history_item(i)}')
            else:
                subprocess.run(
                    [sys.executable, os.path.join(_project_root, 'run.py')] + stripped.split(),
                    check=True
                )

        except KeyboardInterrupt:
            readline.write_history_file(_history_file)
            sys.exit('\n^C\n')
        except subprocess.CalledProcessError:
            print(f'{Fore.RED}Error executing command. Please check your input.{Style.RESET_ALL}')
        except EOFError:
            readline.write_history_file(_history_file)
            sys.exit('\n')


def main():
    check_root()

    if len(sys.argv) == 1:
        welcome()

    try:
        handleCommands()
    finally:
        readline.write_history_file(_history_file)


if __name__ == '__main__':
    main()
