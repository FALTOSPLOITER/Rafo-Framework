"""
Rafo Session Manager
=====================
Sessions let you group related recon commands under one target and export results.

Session data is stored as JSON in ~/.rafo/sessions/<uuid>.json.
The SQLite DB (files/db.py) tracks session metadata.

CLI commands (used from the Rafo interactive shell):
    session list
    session start <target>
    session end
    session export <session-id>
"""

import os
import sys
import json
import uuid
import datetime
from colorama import Fore, Style

_SESSIONS_DIR = os.path.join(os.path.expanduser('~'), '.rafo', 'sessions')
_CURRENT_SESSION_FILE = os.path.join(os.path.expanduser('~'), '.rafo', 'current_session.json')


def _sessions_dir():
    os.makedirs(_SESSIONS_DIR, exist_ok=True)
    return _SESSIONS_DIR


def start_session(target=''):
    """Create a new session and set it as current."""
    session_id = str(uuid.uuid4())[:8]
    now = datetime.datetime.utcnow().isoformat()
    data = {
        'session_id': session_id,
        'target': target,
        'started_at': now,
        'ended_at': None,
        'commands': []
    }
    path = os.path.join(_sessions_dir(), f'{session_id}.json')
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

    # Write current session pointer
    with open(_CURRENT_SESSION_FILE, 'w') as f:
        json.dump({'session_id': session_id, 'path': path}, f)

    print(f'[{Fore.GREEN}+{Style.RESET_ALL}] Session {Fore.GREEN}{session_id}{Style.RESET_ALL} started for target {Fore.YELLOW}{target or "(none)"}{Style.RESET_ALL}.')
    return session_id


def get_current_session():
    """Return current session data dict, or None."""
    if not os.path.exists(_CURRENT_SESSION_FILE):
        return None
    try:
        with open(_CURRENT_SESSION_FILE) as f:
            ptr = json.load(f)
        with open(ptr['path']) as f:
            return json.load(f)
    except Exception:
        return None


def log_command(command, output=''):
    """Append a command entry to the current session."""
    session = get_current_session()
    if not session:
        return
    session['commands'].append({
        'command': command,
        'output': output,
        'timestamp': datetime.datetime.utcnow().isoformat()
    })
    path = os.path.join(_sessions_dir(), f"{session['session_id']}.json")
    with open(path, 'w') as f:
        json.dump(session, f, indent=2)


def end_session():
    """Mark the current session as ended."""
    session = get_current_session()
    if not session:
        print(f'[{Fore.YELLOW}?{Style.RESET_ALL}] No active session.')
        return
    session['ended_at'] = datetime.datetime.utcnow().isoformat()
    path = os.path.join(_sessions_dir(), f"{session['session_id']}.json")
    with open(path, 'w') as f:
        json.dump(session, f, indent=2)
    if os.path.exists(_CURRENT_SESSION_FILE):
        os.remove(_CURRENT_SESSION_FILE)
    print(f'[{Fore.GREEN}+{Style.RESET_ALL}] Session {Fore.GREEN}{session["session_id"]}{Style.RESET_ALL} ended.')


def list_sessions():
    """Print all saved sessions."""
    sdir = _sessions_dir()
    files = sorted([f for f in os.listdir(sdir) if f.endswith('.json')])
    if not files:
        print('No sessions found.')
        return
    print(f'\n{"ID":<12} {"Target":<30} {"Started":<22} {"Ended":<22}')
    print('-' * 90)
    for fname in files:
        try:
            with open(os.path.join(sdir, fname)) as f:
                s = json.load(f)
            print(f'{s["session_id"]:<12} {(s.get("target") or ""):<30} {s["started_at"][:19]:<22} {(s.get("ended_at") or "active")[:19]:<22}')
        except Exception:
            pass
    print()


def export_session(session_id, fmt='json'):
    """Export a session to a file in ~/.rafo/sessions/<id>_export.<fmt>."""
    path = os.path.join(_sessions_dir(), f'{session_id}.json')
    if not os.path.exists(path):
        print(f'[{Fore.RED}!{Style.RESET_ALL}] Session {session_id} not found.')
        return
    with open(path) as f:
        data = json.load(f)

    out_path = os.path.join(_sessions_dir(), f'{session_id}_export.{fmt}')
    with open(out_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f'[{Fore.GREEN}+{Style.RESET_ALL}] Exported to {Fore.GREEN}{out_path}{Style.RESET_ALL}.')
