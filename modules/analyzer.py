import os
import sys
import json
import subprocess

RECON_BINARY = "./bin/recon"

RISK_MAP = {
    21: {"service": "FTP", "risk": "MEDIUM", "note": "Unencrypted file transfer. Check for anonymous login."},
    22: {"service": "SSH", "risk": "LOW", "note": "Ensure strong key-based authentication is enforced."},
    23: {"service": "Telnet", "risk": "CRITICAL", "note": "Cleartext management interface. Should be disabled immediately."},
    25: {"service": "SMTP", "risk": "MEDIUM", "note": "Verify open relay configuration."},
    53: {"service": "DNS", "risk": "LOW", "note": "Check for domain zone transfer exposure."},
    80: {"service": "HTTP", "risk": "LOW", "note": "Unencrypted web server. Ensure HTTPS redirect."},
    445: {"service": "SMB", "risk": "HIGH", "note": "High risk port. Vector for EternalBlue/WannaCry if unpatched."},
    3306: {"service": "MySQL", "risk": "HIGH", "note": "Database exposed directly to network. Restrict access via firewall."},
    8080: {"service": "HTTP-Alt", "risk": "MEDIUM", "note": "Commonly used for dev web servers or admin panels."}
}

WEIGHTS = {
    "CRITICAL": 10,
    "HIGH": 7,
    "MEDIUM": 4,
    "LOW": 1,
    "INFO": 0
}

def check_environment():
    """Checks if the compiled Go binary is present before running analysis."""
    if not os.path.exists(RECON_BINARY):
        print(f"[-] Error: Go recon binary not found at '{RECON_BINARY}'.")
        print("    Run: 'go build -o bin/recon engine/recon.go' first.")
        return False
    return True

def execute_recon(target):
    """Executes the Go recon binary against the target and captures STDOUT."""
    print(f"[+] Launching recon scan against {target}...")
    try:
        result = subprocess.run(
            [RECON_BINARY, target],
            capture_output=True,
            text=True,
            check=True
        )
        print("[+] Scan execution completed successfully!")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[-] Recon execution failed with code {e.returncode}")
        print(f"[-] Error output: {e.stderr}")
        return None
    except Exception as e:
        print(f"[-] Unexpected execution error: {e}")
        return None

def parse_recon_output(raw_output):
    """Parses raw JSON string into Python list/dict with validation."""
    if not raw_output or not raw_output.strip():
        print("[-] Validation Error: Received empty output from Go binary.")
        return None

    try:
        data = json.loads(raw_output)
        if not isinstance(data, list):
            print(f"[-] Validation Error: Expected JSON list, got {type(data).__name__}.")
            return None

        print(f"[+] JSON successfully parsed! Found {len(data)} open port entries.")
        return data
    except json.JSONDecodeError as e:
        print(f"[-] JSON Parse Error: {e.msg}")
        return None

def analyze_findings(parsed_data):
    """Analyzes open ports and calculates security threat score."""
    findings = []
    total_threat_score = 0

    for entry in parsed_data:
        port = entry.get("port")
        banner = entry.get("banner", "").strip()

        rule = RISK_MAP.get(port, {
            "service": "Unknown",
            "risk": "INFO",
            "note": "Standard service or unrecognized port."
        })

        risk_level = rule["risk"]
        score = WEIGHTS.get(risk_level, 0)
        total_threat_score += score

        findings.append({
            "port": port,
            "service": rule["service"],
            "risk": risk_level,
            "score_weight": score,
            "banner": banner if banner else "N/A",
            "recommendation": rule["note"]
        })

    return {
        "total_open_ports": len(parsed_data),
        "overall_threat_score": total_threat_score,
        "findings": findings
    }

def generate_cli_report(target, analysis):
    """Formats and prints a detailed security report to the console."""
    divider = "=" * 60
    sub_divider = "-" * 60

    print("\n" + divider)
    print(f"       ECLYPSA AI — SECURITY ASSESSMENT REPORT")
    print(divider)
    print(f" Target Host          : {target}")
    print(f" Open Ports Detected  : {analysis['total_open_ports']}")
    print(f" Overall Threat Score : {analysis['overall_threat_score']}")
    print(sub_divider)

    if not analysis["findings"]:
        print(" [!] No open ports or actionable risks detected.")
    else:
        print(" FINDINGS BREAKDOWN:\n")
        for item in analysis["findings"]:
            print(f" [{item['risk']}] Port {item['port']} / {item['service']}")
            if item['banner'] != "N/A":
                print(f"   ├─ Service Banner : {item['banner']}")
            print(f"   └─ Action Item    : {item['recommendation']}\n")

    print(divider)
    print(" [i] Report generated automatically by ECLYPSA Analysis Engine.")
    print(divider + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python modules/analyzer.py <target_host>")
        sys.exit(1)

    target_host = sys.argv[1]
    print(f"[+] Initializing ECLYPSA Analysis Module for target: {target_host}")

    if check_environment():
        raw_output = execute_recon(target_host)
        if raw_output:
            parsed_data = parse_recon_output(raw_output)
            if parsed_data is not None:
                analysis = analyze_findings(parsed_data)
                generate_cli_report(target_host, analysis)
                print("[+] Step 5 completed successfully!")
