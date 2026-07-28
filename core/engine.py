import logging
from typing import Dict, Any
from core.config import ConfigManager

class EclypsaEngine:
    def __init__(self, config_path: str = None):
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.config
        self.is_running = False
        self._setup_logger()

    def _setup_logger(self):
        log_level = self.config["engine"]["log_level"].upper()
        logging.basicConfig(
            level=getattr(logging, log_level, logging.INFO),
            format="[%(asctime)s] [%(levelname)s] [ECLYPSA-CORE] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logger = logging.getLogger("EclypsaEngine")

    def initialize(self) -> bool:
        """Initialize pipeline registries, drivers, and background tasks."""
        self.logger.info(f"Initializing ECLYPSA AI Core Engine ({self.config['version']})...")
        self.logger.info(f"Environment: {self.config['engine']['environment']}")
        self.logger.info(f"Target Binding: {self.config['engine']['host']}:{self.config['engine']['port']}")
        
        # Foundation checks
        self.is_running = True
        return True

    def health_check(self) -> Dict[str, Any]:
        """Return engine operational status."""
        return {
            "status": "active" if self.is_running else "inactive",
            "version": self.config["version"],
            "environment": self.config["engine"]["environment"],
            "subsystems": {
                "core": "healthy",
                "config": "loaded"
            }
        }

    def shutdown(self):
        """Safely terminate core threads and unload active plugins."""
        if self.is_running:
            self.logger.info("Initiating graceful core engine shutdown...")
            self.is_running = False
            self.logger.info("Core engine stopped cleanly.")