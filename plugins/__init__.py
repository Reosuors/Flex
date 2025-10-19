# Plugins package. Import plugin modules here to register their handlers.
# We progressively split features out of `modified.py`.
import importlib


def load_all():
    # Load split plugins first
    importlib.import_module("plugins.stats")

    # Then load the legacy monolith
    importlib.import_module("modified")