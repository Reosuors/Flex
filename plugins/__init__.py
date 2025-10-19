# Plugins package. Import plugin modules here to register their handlers.
# For now, we reuse the existing large handler module (modified.py) after
# it is adapted to use the shared client from core.client.
# If you create new plugin files, import them here.
import importlib

def load_all():
    # Importing modified registers all handlers on the shared client
    importlib.import_module("modified")