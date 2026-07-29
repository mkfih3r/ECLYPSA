import json
import subprocess
import sys

# High-risk ports and basic threat assessment mapping
RISK_MAP = {
    21: {"service": "FTP", "risk": "MEDIUM", "note": "Unencrypted file transfer. Check for anonymous login."},
    22: {"service": "SSH", "risk": "LOW", "note": "Ensure key-based authentication is enforced."},
    23: {"service": "Telnet", "risk": "CRITICAL", "note": "Cleartext management interface. Should be disabled."},
    25: {"service": "SMTP", "risk": "MEDIUM", "note": "Check for open relay configuration."},
    53: {"service": "DNS", "risk": "LOW", "note": "Check for zone transfer vulnerabilities."},
    80: {"service": "HTTP", "risk": "LOW", "note": "Plaintext web traffic. Verify HTTPS redirection."},
    445: {"service": "SMB", "risk": "HIGH", "note": "Potential vector for WannaCry/EternalBlue attacks if outdated."},
    3306: {"service": "MySQL", "risk": "HIGH", "note": "Database exposed publicly. Restrict access via firewall."},
    8080: {"service": "HTTP-Alt", "risk": "MEDIUM", "note": "Often hosts unpatched admin panels or dev environments."}
}

def run_recon(target):
    """Executes the Go recon binary and captures JSON output."""
    try:
        result = subprocess.run(
            ["./bin/recon", target],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except FileNotFoundError:
        print("[-] Error: Compiled './bin/recon' binary not found. Build it first using Go.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("[-] Error: Failed to parse JSON output from recon binary.")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Execution error: {e}")
        sys.exit(1)

def analyze_target(scan_results):
    """Analyzes open ports and generates threat assessment summary."""
    findings = []
    total_risk_score = 0

    for item in scan_results:
        port = item.get("port")
        banner = item.get("banner", "").strip()

        info = RISK_MAP.get(port, {"service": "Unknown", "risk": "INFO", "note": "Standard network service."})
        
        # Calculate arbitrary risk rating weight
        weight = {"CRITICAL": 10, "HIGH": 7, "MEDIUM": 4, "LOW": 1, "INFO": 0}.get(info["risk"], 0)
        total_risk_score += weight

        findings.append({
            "port": port,
            "service": info["service"],
            "risk_level": info["risk"],
            "banner": banner if banner else "N/A",
            "recommendation": info["note"]
        })

    return {
        "total_open_ports": len(scan_results),
        "threat_score": total_risk_score,
        "findings": findings
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python modules/analyzer.py <target_host>")
        sys.exit(1)

    target_host = sys.argv[1]
    print(f"[+] ECLYPSA AI: Analyzing target {target_host}...")

    raw_data = run_recon(target_host)
    analysis = analyze_target(raw_data)

    print("\n" + "="*50)
    print(f" SECURITY ANALYSIS REPORT: {target_host}")
    print("="*50)
    print(f"Open Ports Detected : {analysis['total_open_ports']}")
    print(f"Calculated Threat Score : {analysis['threat_score']}")
    print("-" * 50)

    for issue in analysis["findings"]:
        print(f"[{issue['risk_level']}] Port {issue['port']} ({issue['service']})")
        if issue['banner'] != "N/A":
            print(f"  └─ Banner: {issue['banner']}")
        print(f"  └─ Action: {issue['recommendation']}\n")
