"""
Rafo Results Database (SQLite)
================================
Stores all task results persistently at ~/.rafo/results.db.

Tables:
  targets       – unique hosts/domains scanned
  scan_results  – port scan findings
  recon_results – generic key/value recon output (whois, ns, etc.)
  sessions      – high-level session records

Usage (from any task module):
    from files.db import RafoDB
    db = RafoDB()
    db.add_target('example.com')
    db.add_scan_result('example.com', 80, 'tcp', 'open', 'http')
    db.close()
"""

import sqlite3
import os
import datetime


_DB_PATH = os.path.join(os.path.expanduser('~'), '.rafo', 'results.db')


class RafoDB:

    def __init__(self, path=_DB_PATH):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path)
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        c.executescript('''
            CREATE TABLE IF NOT EXISTS targets (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                host      TEXT UNIQUE NOT NULL,
                first_seen TEXT,
                last_seen  TEXT
            );

            CREATE TABLE IF NOT EXISTS scan_results (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                host      TEXT NOT NULL,
                port      INTEGER,
                protocol  TEXT,
                state     TEXT,
                service   TEXT,
                scanned_at TEXT
            );

            CREATE TABLE IF NOT EXISTS recon_results (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                host      TEXT NOT NULL,
                task      TEXT NOT NULL,
                key       TEXT,
                value     TEXT,
                recorded_at TEXT
            );

            CREATE TABLE IF NOT EXISTS sessions (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                target     TEXT,
                started_at TEXT,
                ended_at   TEXT
            );
        ''')
        self.conn.commit()

    # --- Target helpers ---

    def add_target(self, host):
        now = datetime.datetime.utcnow().isoformat()
        c = self.conn.cursor()
        c.execute(
            'INSERT OR IGNORE INTO targets (host, first_seen, last_seen) VALUES (?, ?, ?)',
            (host, now, now)
        )
        c.execute('UPDATE targets SET last_seen = ? WHERE host = ?', (now, host))
        self.conn.commit()

    # --- Scan result helpers ---

    def add_scan_result(self, host, port, protocol, state, service=''):
        now = datetime.datetime.utcnow().isoformat()
        self.add_target(host)
        c = self.conn.cursor()
        c.execute(
            'INSERT INTO scan_results (host, port, protocol, state, service, scanned_at) VALUES (?, ?, ?, ?, ?, ?)',
            (host, port, protocol, state, service, now)
        )
        self.conn.commit()

    # --- Recon result helpers ---

    def add_recon_result(self, host, task, key, value):
        now = datetime.datetime.utcnow().isoformat()
        self.add_target(host)
        c = self.conn.cursor()
        c.execute(
            'INSERT INTO recon_results (host, task, key, value, recorded_at) VALUES (?, ?, ?, ?, ?)',
            (host, task, key, str(value), now)
        )
        self.conn.commit()

    # --- Session helpers ---

    def start_session(self, session_id, target=''):
        now = datetime.datetime.utcnow().isoformat()
        c = self.conn.cursor()
        c.execute(
            'INSERT OR IGNORE INTO sessions (session_id, target, started_at) VALUES (?, ?, ?)',
            (session_id, target, now)
        )
        self.conn.commit()

    def end_session(self, session_id):
        now = datetime.datetime.utcnow().isoformat()
        c = self.conn.cursor()
        c.execute('UPDATE sessions SET ended_at = ? WHERE session_id = ?', (now, session_id))
        self.conn.commit()

    # --- Query helpers ---

    def get_targets(self):
        c = self.conn.cursor()
        return c.execute('SELECT host, first_seen, last_seen FROM targets ORDER BY last_seen DESC').fetchall()

    def get_scan_results(self, host):
        c = self.conn.cursor()
        return c.execute(
            'SELECT port, protocol, state, service, scanned_at FROM scan_results WHERE host = ? ORDER BY port',
            (host,)
        ).fetchall()

    def get_recon(self, host, task=None):
        c = self.conn.cursor()
        if task:
            return c.execute(
                'SELECT key, value, recorded_at FROM recon_results WHERE host = ? AND task = ?',
                (host, task)
            ).fetchall()
        return c.execute(
            'SELECT task, key, value, recorded_at FROM recon_results WHERE host = ? ORDER BY recorded_at',
            (host,)
        ).fetchall()

    def close(self):
        self.conn.close()
