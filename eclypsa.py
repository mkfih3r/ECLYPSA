import os
import sys
import subprocess
import argparse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GO_ENGINE_SRC = os.path.join(BASE_DIR, "engine", "recon.go")
BIN_DIR = os.path.join(BASE_DIR, "bin")
RECON_BINARY = os.path.join(BIN_DIR, "recon")

from modules.analyzer import execute_recon, parse_recon_output, analyze_findings, generate_cli_report
from modules.reporter import export_json, export_html

def build_go_engine():
    """Checks if the Go recon binary exists; if not, builds it automatically."""
    if os.path.exists(RECON_BINARY):
        return True

    print("[*] Go engine binary not found. Building engine/recon.go...")
    os.makedirs(BIN_DIR, exist_ok=True)

    try:
        cmd = ["go", "build", "-o", RECON_BINARY, GO_ENGINE_SRC]
        subprocess.run(cmd, check=True)
        print("[+] Go engine compiled successfully!")
        return True
    except subprocess.CalledProcessError:
        print("[-] Build Error: Failed to compile 'engine/recon.go'. Ensure Go is installed.")
        return False
    except FileNotFoundError:
        print("[-] Environment Error: 'go' command not found. Please install Go compiler.")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="ECLYPSA AI — Hybrid Recon & Threat Analysis Framework"
    )
    parser.add_argument(
        "-t", "--target", 
        required=True, 
        help="Target IP address or domain name to scan"
    )
    parser.add_argument(
        "--json", 
        help="Path to save output as JSON report (e.g. output.json)"
    )
    parser.add_argument(
        "--html", 
        help="Path to save output as HTML report (e.g. output.html)"
    )

    args = parser.parse_args()
    target = args.target

    print(f"[+] Initializing ECLYPSA AI Framework...")

    if not build_go_engine():
        sys.exit(1)

    raw_output = execute_recon(target)
    if not raw_output:
        print("[-] Recon scan failed or returned no data.")
        sys.exit(1)

    parsed_data = parse_recon_output(raw_output)
    if parsed_data is None:
        print("[-] Failed to process scan results.")
        sys.exit(1)

    analysis = analyze_findings(parsed_data)

    # Console Report
    generate_cli_report(target, analysis)

    # Optional File Exports
    if args.json:
        export_json(analysis, args.json)
    if args.html:
        export_html(target, analysis, args.html)

if __name__ == "__main__":
    main()
