import csv
import json
import subprocess
import sys

from colorama import Fore, Style


def save(cmd, filename, fmt='txt'):
    """
    Re-run a Rafo command and save its output to a file.

    Args:
        cmd      : the raw command string (e.g. '-ns example.com')
        filename : destination file path
        fmt      : 'txt' | 'json' | 'csv'
    """
    try:
        result = subprocess.run(
            [sys.executable, 'run.py'] + cmd.strip().split(),
            capture_output=True, text=True
        )
        output = result.stdout

        if fmt == 'json':
            lines = [ln for ln in output.splitlines() if ln.strip()]
            data = {'command': cmd, 'output': lines}
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)

        elif fmt == 'csv':
            lines = [ln for ln in output.splitlines() if ln.strip()]
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['line', 'output'])
                for i, line in enumerate(lines, 1):
                    writer.writerow([i, line])

        else:
            with open(filename, 'w') as f:
                f.write(output)

    except Exception as e:
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Error: {Fore.RED}{e}{Style.RESET_ALL}')
    else:
        print(f'[{Fore.GREEN}+{Style.RESET_ALL}] Successfully saved {Fore.GREEN}{filename}{Style.RESET_ALL} ({fmt.upper()} format).')
