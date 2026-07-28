import os
import importlib.util
import logging
from typing import Dict, Any, Type
from plugins.base import BasePlugin

class PluginLoader:
    def __init__(self, plugin_dir: str = "./plugins"):
        self.plugin_dir = plugin_dir
        self.loaded_plugins: Dict[str, BasePlugin] = {}
        self.logger = logging.getLogger("PluginLoader")

    def discover_and_load(self) -> Dict[str, BasePlugin]:
        """Scans the plugin directory and dynamically loads BasePlugin classes."""
        if not os.path.exists(self.plugin_dir):
            self.logger.warning(f"Plugin directory does not exist: {self.plugin_dir}")
            return self.loaded_plugins

        for file_name in os.listdir(self.plugin_dir):
            if file_name.endswith(".py") and not file_name.startswith("__") and file_name != "base.py" and file_name != "loader.py":
                plugin_path = os.path.join(self.plugin_dir, file_name)
                module_name = file_name[:-3]
                
                try:
                    spec = importlib.util.spec_from_file_location(module_name, plugin_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        # Find class extending BasePlugin
                        for attribute_name in dir(module):
                            attribute = getattr(module, attribute_name)
                            if (isinstance(attribute, type) and 
                                issubclass(attribute, BasePlugin) and 
                                attribute is not BasePlugin):
                                
                                plugin_instance: BasePlugin = attribute()
                                if plugin_instance.initialize():
                                    plugin_instance.is_enabled = True
                                    self.loaded_plugins[plugin_instance.name] = plugin_instance
                                    self.logger.info(f"[+] Dynamic plugin loaded: {plugin_instance.name} (v{plugin_instance.version})")
                except Exception as e:
                    self.logger.error(f"[X] Failed to load plugin from {file_name}: {e}")

        return self.loaded_plugins

    def get_plugin(self, name: str) -> Optional[BasePlugin]:
        """Retrieve a loaded plugin by name."""
        return self.loaded_plugins.get(name)