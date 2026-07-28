import ssl
import socket
import urllib.request
from typing import Dict, Any, Optional
from plugins.base import BasePlugin

class WebAnalyzerPlugin(BasePlugin):
    """
    ECLYPSA AI Skill Plugin: Web Security Headers & SSL/TLS Configuration Audit.
    Assesses basic security posture for target web applications.
    """
    def __init__(self):
        super().__init__(name="web_analyzer", version="1.0.0")

    def initialize(self, config: Optional[Dict[str, Any]] = None) -> bool:
        self.is_enabled = True
        return True

    def _check_security_headers(self, url: str) -> Dict[str, Any]:
        """Audit HTTP security headers on target."""
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        recommended_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy",
            "Access-Control-Allow-Origin"
        ]

        result = {"url": url, "present_headers": {}, "missing_headers": [], "cors_misconfig": False}

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ECLYPSA-AI-Audit/1.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                headers = dict(response.headers)
                
                for head in recommended_headers:
                    found = False
                    for h_key, h_val in headers.items():
                        if h_key.lower() == head.lower():
                            result["present_headers"][head] = h_val
                            found = True
                            # Check CORS wildcard misconfiguration
                            if head.lower() == "access-control-allow-origin" and h_val == "*":
                                result["cors_misconfig"] = True
                            break
                    if not found:
                        result["missing_headers"].append(head)

        except Exception as e:
            result["error"] = str(e)

        return result

    def _check_ssl_info(self, hostname: str) -> Dict[str, Any]:
        """Fetch basic SSL certificate metadata."""
        ssl_info = {}
        try:
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    ssl_info["subject"] = dict(x[0] for x in cert.get("subject", []))
                    ssl_info["issuer"] = dict(x[0] for x in cert.get("issuer", []))
                    ssl_info["version"] = cert.get("version")
                    ssl_info["notAfter"] = cert.get("notAfter")
        except Exception as e:
            ssl_info["error"] = str(e)

        return ssl_info

    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execution payload:
        - target: Domain or hostname
        """
        target = payload.get("target") or payload.get("domain")
        if not target:
            return {"status": "error", "message": "Missing 'target' parameter"}

        # Clean hostname for SSL check
        hostname = target.replace("https://", "").replace("http://", "").split("/")[0]

        headers_audit = self._check_security_headers(target)
        ssl_audit = self._check_ssl_info(hostname)

        return {
            "status": "success",
            "target": target,
            "security_headers": headers_audit,
            "ssl_certificate": ssl_audit
        }

    def shutdown(self) -> None:
        pass
