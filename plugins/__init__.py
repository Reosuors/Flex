import importlib

async def run_startup():
    # قائمة الموديولات اللي ممكن تحتوي على run_startup
    plugins_with_startup = {
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
        'plugins.media',
        'plugins.inline_help',
        'plugins.ai_tools',
        'plugins.interactions',
        'plugins.aliases',
        'plugins.check',
        'plugins.onboarding',
        'plugins.log_admin',
    }

    for module_name in plugins_with_startup:
        try:
            mod = importlib.import_module(module_name)
            if hasattr(mod, 'run_startup'):
                await mod.run_startup()
        except Exception as e:
            # سجل الخطأ لو حابب، أو تجاهله عشان ما يوقف التشغيل
            print(f"⚠️ Error in {module_name}.run_startup: {e}")
