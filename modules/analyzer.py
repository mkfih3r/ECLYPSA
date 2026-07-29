import os
import sys

# Path to our compiled Go recon binary
RECON_BINARY = "./bin/recon"

def check_environment():
    """Checks if the compiled Go binary is present before running analysis."""
    if not os.path.exists(RECON_BINARY):
        print(f"[-] Error: Go recon binary not found at '{RECON_BINARY}'.")
        print("    Run: 'go build -o bin/recon engine/recon.go' first.")
        return False
    
    print(f"[+] Verified: Native Go binary found at '{RECON_BINARY}'")
    return True

if __name__ == "__main__":
    # Check if target argument is provided
    if len(sys.argv) < 2:
        print("Usage: python modules/analyzer.py <target_host>")
        sys.exit(1)

    target_host = sys.argv[1]
    print(f"[+] Initializing ECLYPSA Analysis Module for target: {target_host}")

    if check_environment():
        print("[+] Step 1 completed successfully!")
