# Plugins package. Import plugin modules here to register their handlers.
# We progressively split features out of `modified.py`.
import importlib


def load_all():
    # Load split plugins first
    importlib.import_module("plugins.stats")
    importlib.import_module("plugins.storage")
    importlib_imports = [
        "plugins.auto_reply",
        "plugins.afk",
        "plugins.profile",
        "plugins.timers_publish",
        "plugins.protection",
        "plugins.games",
        "plugins.shortcuts_memes",
        "plugins.user_tools",
    ]
    for module in importlib_imports:
        importlib.import_module(module)

    # Then load the legacy monolith (until full split is complete)
    importlib.import_module("modified")