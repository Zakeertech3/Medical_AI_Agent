from core.agent_base import BaseAgent

class Psychologist(BaseAgent):
    """Psychologist specialist agent for analyzing mental health conditions."""
    
    def _get_role(self) -> str:
        """Return the role of this agent as a psychologist."""
        return "Psychologist"
