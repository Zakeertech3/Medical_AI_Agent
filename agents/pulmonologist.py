from core.agent_base import BaseAgent

class Pulmonologist(BaseAgent):
    """Pulmonologist specialist agent for analyzing respiratory conditions."""
    
    def _get_role(self) -> str:
        """Return the role of this agent as a pulmonologist."""
        return "Pulmonologist"
