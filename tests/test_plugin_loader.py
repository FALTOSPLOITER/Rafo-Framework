"""Unit tests for files/plugin_loader.py"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class TestDiscoverPlugins:
    def test_discover_returns_list(self, tmp_path, monkeypatch):
        """discover_plugins() returns a list (empty or populated)."""
        import files.plugin_loader as pl

        monkeypatch.setattr(pl, '_PLUGINS_DIR', str(tmp_path))
        result = pl.discover_plugins()
        assert isinstance(result, list)

    def test_valid_plugin_is_loaded(self, tmp_path, monkeypatch):
        """A correctly structured plugin file is discovered and loaded."""
        plugin_src = '''
COMMAND = "testcmd"
DESCRIPTION = "Test plugin"
ARGS = []
def run(args): pass
'''
        (tmp_path / 'myplugin.py').write_text(plugin_src)
        import files.plugin_loader as pl

        monkeypatch.setattr(pl, '_PLUGINS_DIR', str(tmp_path))
        plugins = pl.discover_plugins()
        assert len(plugins) == 1
        assert plugins[0].COMMAND == 'testcmd'

    def test_incomplete_plugin_is_skipped(self, tmp_path, monkeypatch):
        """A plugin missing required attributes is skipped without crashing."""
        (tmp_path / 'bad.py').write_text('COMMAND = "bad"\n')
        import files.plugin_loader as pl

        monkeypatch.setattr(pl, '_PLUGINS_DIR', str(tmp_path))
        plugins = pl.discover_plugins()
        assert plugins == []

    def test_underscore_files_ignored(self, tmp_path, monkeypatch):
        """Files starting with _ are not loaded as plugins."""
        (tmp_path / '__init__.py').write_text('')
        import files.plugin_loader as pl

        monkeypatch.setattr(pl, '_PLUGINS_DIR', str(tmp_path))
        assert pl.discover_plugins() == []
