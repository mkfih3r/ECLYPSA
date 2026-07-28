import unittest
import os
from core.config import ConfigManager

class TestConfigManager(unittest.TestCase):
    def test_default_config_loading(self):
        config_mgr = ConfigManager()
        self.assertEqual(config_mgr.get("version"), "v0.0.1-alpha")
        self.assertEqual(config_mgr.get("engine.port"), 8080)

    def test_env_override(self):
        os.environ["ECLYPSA_PORT"] = "9090"
        config_mgr = ConfigManager()
        self.assertEqual(config_mgr.get("engine.port"), 9090)
        del os.environ["ECLYPSA_PORT"]

if __name__ == "__main__":
    unittest.main()