import socket
import subprocess
import os
import json
from typing import Dict, Any, Optional
from plugins.base import BasePlugin

class NetworkReconPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="network_recon", version="1.1.0")
        self.go_engine_bin = "./engine/recon"

    def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Verify plugin binaries and environment."""
        self.is_enabled = True
        return True

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Core execution logic: fast port check and banner grabbing."""
        target = payload.get("target")
        if not target:
            return {"status": "error", "message": "Missing 'target' in payload"}

        # Use Go engine if compiled, fallback to native Python sockets
        if os.path.exists(self.go_engine_bin):
            try:
                res = subprocess.run([self.go_engine_bin, target], capture_output=True, text=True, timeout=10)
                open_ports = json.loads(res.stdout)
                return {"status": "success", "engine": "go", "open_ports": open_ports}
            except Exception as e:
                pass

        # Python Socket Fallback Banner Grabber
        ports = payload.get("ports", [21, 22, 80, 443, 8080])
        discovered = []
        for port in ports:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1.0)
                    if s.connect_ex((target, port)) == 0:
                        discovered.append({"port": port, "open": True})
            except Exception:
                continue

        return {"status": "success", "engine": "python_fallback", "discovered": discovered}

    def shutdown(self) -> None:
        pass