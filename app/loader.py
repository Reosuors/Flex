import importlib
import os
import glob
import logging

def load_plugins():
    """
    Dynamically load all Python files in the plugins/ directory as modules.
    """
    plugins_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "plugins")
    plugin_files = glob.glob(os.path.join(plugins_dir, "*.py"))
    
    for file_path in plugin_files:
        module_name = os.path.basename(file_path)[:-3]
        if module_name == "__init__":
            continue
            
        try:
            importlib.import_module(f"plugins.{module_name}")
            print(f"[loader] ✅ Loaded plugin: {module_name}")
        except Exception as e:
            print(f"[loader] ❌ Failed to load plugin {module_name}: {e}")
