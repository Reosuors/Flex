from plugins import load_all

def load_plugins():
    """
    Import and register all plugins/handlers.
    Separated so it can be extended later (e.g., conditional loading).
    """
    load_all()