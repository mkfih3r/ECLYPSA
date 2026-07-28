import argparse
import sys
import json
from core.engine import EclypsaEngine

def main():
    parser = argparse.ArgumentParser(
        description="ECLYPSA AI Core Command Line Interface"
    )
    
    parser.add_argument(
        "-v", "--version", 
        action="store_true", 
        help="Display version information"
    )
    
    parser.add_argument(
        "-c", "--config", 
        type=str, 
        help="Path to custom YAML configuration file"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    # Command: init
    subparsers.add_parser("init", help="Initialize local environment and configuration")

    # Command: start
    start_parser = subparsers.add_parser("start", help="Start the ECLYPSA core runtime engine")
    start_parser.add_argument("--dry-run", action="store_true", help="Initialize and exit cleanly for health validation")

    # Command: status
    subparsers.add_parser("status", help="Display core engine health and subsystem status")

    args = parser.parse_args()

    # Create Engine Instance
    engine = EclypsaEngine(config_path=args.config)

    if args.version:
        print(f"ECLYPSA AI Engine Version: {engine.config['version']}")
        sys.exit(0)

    if args.command == "init":
        print("[+] Initializing ECLYPSA AI local configuration...")
        print(f"[✓] Default configuration structure validated at: {engine.config_manager.config_path}")
        sys.exit(0)

    elif args.command == "start":
        engine.initialize()
        if args.dry_run:
            print("[✓] Dry run execution completed successfully.")
            engine.shutdown()
        else:
            print("[+] Engine is running. Press CTRL+C to terminate.")
            try:
                # Keep process active
                import time
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                engine.shutdown()

    elif args.command == "status":
        engine.initialize()
        status_info = engine.health_check()
        print(json.dumps(status_info, indent=2))
        engine.shutdown()

    else:
        parser.print_help()

if __name__ == "__main__":
    main()