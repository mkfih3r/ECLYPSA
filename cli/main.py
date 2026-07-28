import argparse
import sys
import json
import logging
from core.engine import EclypsaEngine
from plugins.loader import PluginLoader
from agent.llm import OllamaProvider, OpenAIProvider
from agent.react import ReActAgent
from agent.bridge import AgentPluginBridge

def main():
    parser = argparse.ArgumentParser(description="ECLYPSA AI CLI - Autonomous Intelligence Core")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Health & Status Command
    subparsers.add_parser("status", help="Check system health and core status")

    # Agent Execution Command
    agent_parser = subparsers.add_parser("agent", help="Run autonomous agent tasks")
    agent_parser.add_argument("--task", type=str, required=True, help="Task description for the agent")
    agent_parser.add_argument("--provider", type=str, choices=["ollama", "openai"], default="ollama", help="LLM Provider")
    agent_parser.add_argument("--model", type=str, default="llama3", help="Model name")
    agent_parser.add_argument("--api-key", type=str, default="", help="API key for cloud provider")

    args = parser.parse_args()

    engine = EclypsaEngine()
    engine.initialize()

    if args.command == "status":
        print(json.dumps(engine.health_check(), indent=2))

    elif args.command == "agent":
        print(f"[*] Initializing ECLYPSA AI Agent [Provider: {args.provider}]...")

        # Setup Provider
        if args.provider == "openai":
            if not args.api_key:
                print("[X] Error: --api-key is required for OpenAI provider.")
                sys.exit(1)
            provider = OpenAIProvider(api_key=args.api_key, model=args.model)
        else:
            provider = OllamaProvider(model=args.model)

        # Setup ReAct Agent & Plugin Bridge
        react_agent = ReActAgent(llm_provider=provider)
        plugin_loader = PluginLoader()
        bridge = AgentPluginBridge(plugin_loader, react_agent)

        registered_tools = bridge.sync_plugins_to_tools()
        print(f"[+] Loaded {registered_tools} plugin tool(s) into agent arsenal.")

        print(f"[*] Executing task: {args.task}\n" + "-"*50)
        result = react_agent.run(task=args.task)
        print("-" * 50)
        print(f"[+] Agent Final Output:\n{result}")

    else:
        parser.print_help()

    engine.shutdown()

if __name__ == "__main__":
    main()