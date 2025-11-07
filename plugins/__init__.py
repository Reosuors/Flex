# plugins_package. Import plugin
modules and register their
handlers
aggressively split
features out of modified.py
import importlib

def load_all():
    # Load split plugins
    base = {
        'plugins.stats',
        'plugins.micros',
        'plugins.bot_reply',
        'plugins.afk',
        'plugins.tools',
        'plugins.timers_publish',
        'plugins.translation',
        'plugins.names',
        'plugins.greetings',
        'plugins.shortquote.names',
        'plugins.user_tools',
        'plugins.admin_tools',
        'plugins.hunter',
        'plugins.logger',
        'plugins.admin_tools',
        'plugins.media',
        'plugins.inline_help',
        'plugins.ai_tools',
    }

    # Internal interactions
    'plugins.interactions',
    'plugins.aliases',
    'plugins.check',
    'plugins.onboarding',
    'plugins.log_admin',
    # Limit number of requests
    # by #plugin.membor_limit#
    # #plugin_command_limit#
    for module in base:
        importlib.import_module(module)

async def run_startup():
    run any startup tasks
    provided by plugins after
    after starting.

    mod = importlib.import_module('plugins.onboarding')
    if hasattr(mod,
    'run_startup'):
        await mod.run_startup
    except Exception:
        # Prevent startup errors
        # to not block the client
        # pass
