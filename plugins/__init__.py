# Plugins package. Import plugin modules here to register their handlers.
# We progressively split features out of `modified.py`.
import importlib

def load_all():
    # Load split plugins
    base = [
        "plugins.stats",
        "plugins.storage",
        "plugins.auto_reply",
        "plugins.afk",
        "plugins.profile",
        "plugins.timers_publish",
        "plugins.protection",
        "plugins.games",
        "plugins.shortcuts_memes",
        "plugins.user_tools",
        "plugins.media_tools",
        "plugins.hunter",
        "plugins.monitor",
        "plugins.admin_tools",
        "plugins.help",
        "plugins.inline_help",
        "plugins.ai_tools",
        "plugins.temp_mail",
        "plugins.fake_interactions",
        "plugins.command_aliases",
        "plugins.check",
        "plugins.onboarding",
        # Removed limits by request:
        # "plugins.member_limit",
        # "plugins.command_limit",
    ]
    for module in base:
        importlib.import_module(module)

async def run_startup():
    """
    Run any startup tasks provided by plugins after client.start().
    """
    try:
        mod = importlib.import_module("plugins.onboarding")
        if hasattr(mod, "run_startup"):
            await mod.run_startup()
    except Exception:
        # Ignore startup errors to not block the client
        pass