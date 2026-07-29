import os
import sys
import subprocess

RECON_BINARY = "./bin/recon"

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
        # Runs the binary with target host as argument
        result = subprocess.run(
            [RECON_BINARY, target],
            capture_output=True,  # Captures stdout and stderr
            text=True,            # Converts byte output to Python string
            check=True            # Raises error if process exits with error code
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python modules/analyzer.py <target_host>")
        sys.exit(1)

    target_host = sys.argv[1]
    print(f"[+] Initializing ECLYPSA Analysis Module for target: {target_host}")

    if check_environment():
        raw_output = execute_recon(target_host)
        if raw_output:
            print("\n[+] Raw output received from Go engine:")
            print(raw_output)
            print("[+] Step 2 completed successfully!")
