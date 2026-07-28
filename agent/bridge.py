import json
import logging
from typing import Dict, Any
from plugins.loader import PluginLoader
from agent.react import ReActAgent

class AgentPluginBridge:
    """Bridge layer that converts loaded plugins into executable agent tools."""

    def __init__(self, plugin_loader: PluginLoader, agent: ReActAgent):
        self.plugin_loader = plugin_loader
        self.agent = agent
        self.logger = logging.getLogger("AgentPluginBridge")

    def sync_plugins_to_tools(self) -> int:
        """Scan loaded plugins and register their execute methods as agent tools."""
        plugins = self.plugin_loader.discover_and_load()
        count = 0

        for plugin_name, plugin_instance in plugins.items():
            if plugin_instance.is_enabled:
                def make_tool_wrapper(inst):
                    def tool_wrapper(payload: Any) -> Dict[str, Any]:
                        if isinstance(payload, str):
                            try:
                                payload = json.loads(payload)
                            except Exception:
                                payload = {"target": payload}
                        return inst.execute(payload)
                    return tool_wrapper

                self.agent.register_tool(plugin_name, make_tool_wrapper(plugin_instance))
                self.logger.info(f"[Bridge] Registered plugin '{plugin_name}' as agent tool")
                count += 1

        return count