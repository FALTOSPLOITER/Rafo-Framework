"""
Rafo Plugin Loader
==================
Plugins live in the top-level `plugins/` directory.
Each plugin is a .py file that exposes:

    COMMAND     = "tool-name"          # the CLI flag (without leading -)
    DESCRIPTION = "Short description"
    ARGS        = [                    # list of argparse kwargs dicts
        {"flags": ["-target"], "type": str, "nargs": 1, "required": True,
         "help": "target host"},
    ]
    def run(args): ...                 # called with the parsed Namespace

Example plugin file: plugins/mytools.py
"""

import os
import importlib.util
import sys
from colorama import Fore, Style

_PLUGINS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'plugins')


def _load_plugin(path):
    """Load a plugin module from an absolute file path."""
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def discover_plugins():
    """Return a list of valid plugin modules from the plugins/ directory."""
    plugins = []
    if not os.path.isdir(_PLUGINS_DIR):
        return plugins

    for fname in sorted(os.listdir(_PLUGINS_DIR)):
        if not fname.endswith('.py') or fname.startswith('_'):
            continue
        path = os.path.join(_PLUGINS_DIR, fname)
        try:
            mod = _load_plugin(path)
            # Validate required attributes
            for attr in ('COMMAND', 'DESCRIPTION', 'ARGS', 'run'):
                if not hasattr(mod, attr):
                    raise AttributeError(f'missing "{attr}"')
            plugins.append(mod)
        except Exception as e:
            print(f'[{Fore.YELLOW}?{Style.RESET_ALL}] Plugin {fname} skipped: {e}')

    return plugins


def register_plugins(parser, plugins):
    """Add each plugin's arguments to an argparse parser."""
    for plugin in plugins:
        parser.add_argument(
            f'-{plugin.COMMAND}',
            action='store_true',
            help=f'[plugin] {plugin.DESCRIPTION}'
        )
        for arg_spec in plugin.ARGS:
            flags = arg_spec.pop('flags')
            parser.add_argument(*flags, **arg_spec)


def dispatch_plugins(args, plugins):
    """
    Check parsed args against loaded plugins and call the matching one.
    Returns True if a plugin was dispatched, False otherwise.
    """
    for plugin in plugins:
        if getattr(args, plugin.COMMAND.replace('-', '_'), False):
            plugin.run(args)
            return True
    return False
