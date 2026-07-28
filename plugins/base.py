from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BasePlugin(ABC):
    """Abstract Base Class that all ECLYPSA AI plugins must inherit from."""

    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.is_enabled = False

    @abstractmethod
    def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Initialize plugin resources and configurations."""
        pass

    @abstractmethod
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Core execution logic of the plugin."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Cleanup resources on plugin unload."""
        pass

    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the plugin."""
        return {
            "name": self.name,
            "version": self.version,
            "status": "enabled" if self.is_enabled else "disabled"
        }