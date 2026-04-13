"""Unit tests for files/db.py"""

import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestRafoDB:
    @pytest.fixture
    def db(self, tmp_path):
        from files.db import RafoDB

        d = RafoDB(path=str(tmp_path / 'test.db'))
        yield d
        d.close()

    def test_add_and_get_target(self, db):
        db.add_target('example.com')
        targets = db.get_targets()
        hosts = [t[0] for t in targets]
        assert 'example.com' in hosts

    def test_add_target_idempotent(self, db):
        db.add_target('example.com')
        db.add_target('example.com')
        assert len([t for t in db.get_targets() if t[0] == 'example.com']) == 1

    def test_add_scan_result(self, db):
        db.add_scan_result('10.0.0.1', 80, 'tcp', 'open', 'http')
        results = db.get_scan_results('10.0.0.1')
        assert len(results) == 1
        assert results[0][0] == 80

    def test_add_recon_result(self, db):
        db.add_recon_result('example.com', 'whois', 'registrar', 'IANA')
        recon = db.get_recon('example.com', task='whois')
        assert len(recon) == 1
        assert recon[0][0] == 'registrar'

    def test_session_lifecycle(self, db):
        db.start_session('sess-001', target='example.com')
        db.end_session('sess-001')
        c = db.conn.cursor()
        row = c.execute("SELECT ended_at FROM sessions WHERE session_id='sess-001'").fetchone()
        assert row and row[0] is not None
