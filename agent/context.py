from typing import List, Dict, Any, Optional
import time

class AgentContext:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history: List[Dict[str, Any]] = []
        self.metadata: Dict[str, Any] = {
            "created_at": time.time(),
            "step_count": 0
        }

    def add_event(self, role: str, content: str, payload: Optional[Dict[str, Any]] = None):
        """Record an execution step or message in session history."""
        event = {
            "timestamp": time.time(),
            "role": role,
            "content": content,
            "payload": payload or {}
        }
        self.history.append(event)
        self.metadata["step_count"] += 1

    def get_summary(self) -> Dict[str, Any]:
        """Return session state summary."""
        return {
            "session_id": self.session_id,
            "total_steps": self.metadata["step_count"],
            "created_at": self.metadata["created_at"],
            "recent_events": self.history[-5:] if self.history else []
        }