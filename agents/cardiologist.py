# agents/cardiologist.py
from core.agent_base import BaseAgent

class Cardiologist(BaseAgent):
    """Cardiologist specialist agent."""
    
    def _get_role(self) -> str:
        return "Cardiologist"

# agents/psychologist.py
from core.agent_base import BaseAgent

class Psychologist(BaseAgent):
    """Psychologist specialist agent."""
    
    def _get_role(self) -> str:
        return "Psychologist"

# agents/pulmonologist.py
from core.agent_base import BaseAgent

class Pulmonologist(BaseAgent):
    """Pulmonologist specialist agent."""
    
    def _get_role(self) -> str:
        return "Pulmonologist"

# agents/custom_agent.py
from core.agent_base import BaseAgent

class CustomAgent(BaseAgent):
    """
    Template for creating custom medical specialist agents.
    
    Example usage:
    
    class Neurologist(CustomAgent):
        def _get_role(self) -> str:
            return "Neurologist"
    """
    
    def _get_role(self) -> str:
        """Override this method to define the role."""
        return "CustomSpecialist"