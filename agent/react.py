import json
import logging
from typing import Dict, Any, Callable
from agent.llm import BaseLLMProvider

SYSTEM_PROMPT = """You are ECLYPSA AI, an autonomous cybersecurity intelligence and security automation agent.
You operate using the ReAct (Reasoning and Acting) loop.

When presented with a task, respond ONLY in valid JSON with the following schema:
{
    "thought": "Your step-by-step reasoning about what to do next",
    "action": "tool_name OR 'finish'",
    "action_input": {"param_key": "param_value"} or "Final summary answer when action is finish"
}
"""

class ReActAgent:
    def __init__(self, llm_provider: BaseLLMProvider):
        self.llm = llm_provider
        self.tools: Dict[str, Callable] = {}
        self.logger = logging.getLogger("ReActAgent")

    def register_tool(self, name: str, func: Callable):
        """Register executable tool into the agent's arsenal."""
        self.tools[name] = func

    def run(self, task: str, max_iterations: int = 5) -> str:
        self.logger.info(f"Executing task via ReAct Loop: '{task}'")
        context_history = f"Task: {task}\n"

        for iteration in range(1, max_iterations + 1):
            prompt = f"{context_history}\nIteration {iteration}/{max_iterations}. Determine next step in JSON:"
            raw_response = self.llm.generate(prompt, system_prompt=SYSTEM_PROMPT)

            try:
                # Find JSON block
                start_idx = raw_response.find("{")
                end_idx = raw_response.rfind("}") + 1
                clean_json = raw_response[start_idx:end_idx]
                decision = json.loads(clean_json)

                thought = decision.get("thought", "")
                action = decision.get("action", "finish")
                action_input = decision.get("action_input", {})

                self.logger.info(f"[Thought]: {thought}")

                if action == "finish":
                    return str(action_input)

                if action in self.tools:
                    self.logger.info(f"[Action]: Executing '{action}' with inputs {action_input}")
                    observation = self.tools[action](**action_input) if isinstance(action_input, dict) else self.tools[action](action_input)
                    self.logger.info(f"[Observation]: {observation}")
                    context_history += f"\nAction: {action}\nObservation: {observation}\n"
                else:
                    context_history += f"\nAction Failure: Tool '{action}' is not registered.\n"

            except Exception as e:
                self.logger.warning(f"Failed to parse LLM reasoning output: {e}. Raw response: {raw_response}")
                context_history += f"\nSystem Error: Response format was invalid JSON. Retrying.\n"

        return "Task stopped: Reached maximum allowed iterations."