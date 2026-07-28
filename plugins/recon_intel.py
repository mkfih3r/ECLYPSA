import socket
import ssl
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional, List
from plugins.base import BasePlugin

class IntelScannerPlugin(BasePlugin):
    """
    ECLYPSA AI Skill Plugin: Subdomain Enumerator (crt.sh OSINT) & Service Banner Grabber.
    Designed for asset discovery and defensive attack surface mapping.
    """
    def __init__(self):
        super().__init__(name="recon_intel", version="1.0.0")

    def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
        self.is_enabled = True
        return True

    def _enumerate_subdomains(self, domain: str) -> List[str]:
        """Fetch passive subdomains from Certificate Transparency logs (crt.sh)."""
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        subdomains = set()
        
        try:
            req = urllib.request.Request(
                url, 
                headers={"User-Agent": "ECLYPSA-AI-Scanner/1.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    for entry in data:
                        name_value = entry.get("name_value", "")
                        for name in name_value.split("\n"):
                            name = name.strip().lower()
                            if name.endswith(domain) and not name.startswith("*"):
                                subdomains.add(name)
        except Exception:
            pass
            
        return sorted(list(subdomains))

    def _grab_banner(self, target: str, port: int) -> Dict[str, Any]:
        """Grab raw service banner or HTTP server headers."""
        banner_info = {"port": port, "banner": None, "service": "unknown"}
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0)
                s.connect((target, port))
                
                # HTTP/HTTPS Web Server Header Grabber
                if port in [80, 443, 8080, 8443]:
                    request = f"HEAD / HTTP/1.1\r\nHost: {target}\r\nUser-Agent: ECLYPSA-AI/1.0\r\nConnection: close\r\n\r\n"
                    
                    if port in [443, 8443]:
                        context = ssl.create_default_context()
                        context.check_hostname = False
                        context.verify_mode = ssl.CERT_NONE
                        with context.wrap_socket(s, server_hostname=target) as ss:
                            ss.sendall(request.encode())
                            response = ss.recv(1024).decode("utf-8", errors="ignore")
                    else:
                        s.sendall(request.encode())
                        response = s.recv(1024).decode("utf-8", errors="ignore")
                    
                    # Parse 'Server' or 'X-Powered-By' Header
                    for line in response.split("\r\n"):
                        if line.lower().startswith("server:"):
                            banner_info["banner"] = line.split(":", 1)[1].strip()
                            banner_info["service"] = "http/web"
                            break
                    if not banner_info["banner"] and response:
                        banner_info["banner"] = response.split("\r\n")[0]
                else:
                    # Raw TCP banner (SSH, FTP, SMTP, etc.)
                    banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
                    if banner:
                        banner_info["banner"] = banner
                        banner_info["service"] = "raw_tcp"
                        
        except Exception as e:
            banner_info["error"] = str(e)
            
        return banner_info

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execution entrypoint for ReAct Agent and Plugin Manager.
        Payload options:
        - target / domain: Domain or IP address
        - action: 'subdomains' | 'banner' | 'full' (default: 'full')
        - ports: List of ports (default: [21, 22, 80, 443, 8080])
        """
        action = payload.get("action", "full")
        target = payload.get("domain") or payload.get("target")
        ports = payload.get("ports", [21, 22, 80, 443, 8080])

        if not target:
            return {"status": "error", "message": "Missing 'target' or 'domain' parameter in payload"}

        results = {"target": target, "subdomains": [], "banners": []}

        if action in ["subdomains", "full"]:
            results["subdomains"] = self._enumerate_subdomains(target)

        if action in ["banner", "full"]:
            for port in ports:
                banner_data = self._grab_banner(target, port)
                if banner_data.get("banner"):
                    results["banners"].append(banner_data)

        return {"status": "success", "action": action, "results": results}

    def shutdown(self) -> None:
        pass
