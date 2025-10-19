# Plugins package. Import plugin modules here to register their handlers.
# We progressively split features out of `modified.py`.
import importlib


def load_all():
    # Load split plugins first
    importlib.import_module("plugins.stats")
    importlib.import_module("plugins.storage")
    importlib.import_module("plugins.auto_reply")

    # Then load the legacy monolith (until full split is complete)
    importlib.import_module("modified")