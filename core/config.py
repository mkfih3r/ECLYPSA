import os
import yaml
from typing import Dict, Any, Optional

DEFAULT_CONFIG: Dict[str, Any] = {
    "version": "v0.0.1-alpha",
    "engine": {
        "environment": "development",
        "log_level": "info",
        "host": "127.0.0.1",
        "port": 8080
    },
    "telemetry": {
        "enabled": False
    },
    "plugins": {
        "directory": "./plugins",
        "auto_load": False
    },
    "agent": {
        "max_iterations": 10,
        "timeout_seconds": 120
    }
}

class ConfigManager:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.getenv(
            "ECLYPSA_CONFIG_PATH", 
            os.path.expanduser("~/.eclypsa/config.yaml")
        )
        self.config = DEFAULT_CONFIG.copy()
        self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file if exists, then apply env overrides."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    file_config = yaml.safe_load(f) or {}
                    self._deep_update(self.config, file_config)
            except Exception as e:
                print(f"[!] Warning: Failed to parse config file at {self.config_path}: {e}")

        self._apply_env_overrides()
        return self.config

    def _apply_env_overrides(self):
        """Override configuration with ECLYPSA_ environment variables."""
        if env_val := os.getenv("ECLYPSA_ENV"):
            self.config["engine"]["environment"] = env_val
        if env_val := os.getenv("ECLYPSA_LOG_LEVEL"):
            self.config["engine"]["log_level"] = env_val
        if env_val := os.getenv("ECLYPSA_HOST"):
            self.config["engine"]["host"] = env_val
        if env_val := os.getenv("ECLYPSA_PORT"):
            try:
                self.config["engine"]["port"] = int(env_val)
            except ValueError:
                pass

    def _deep_update(self, original: Dict[str, Any], update: Dict[str, Any]):
        """Recursively update a nested dictionary."""
        for key, value in update.items():
            if isinstance(value, dict) and key in original and isinstance(original[key], dict):
                self._deep_update(original[key], value)
            else:
                original[key] = value

    def get(self, key_path: str, default: Any = None) -> Any:
        """Access nested keys using dot-notation (e.g., 'engine.port')."""
        keys = key_path.split(".")
        curr = self.config
        for k in keys:
            if isinstance(curr, dict) and k in curr:
                curr = curr[k]
            else:
                return default
        return curr