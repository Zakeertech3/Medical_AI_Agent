from core.agent_base import BaseAgent

class CustomAgent(BaseAgent):
    """
    Template for creating custom medical specialist agents.
    
    To create a new specialist agent, inherit from this class and implement the _get_role method.
    The agent will automatically load the corresponding prompt template from the templates directory.
    
    Example usage:
    
    class Neurologist(CustomAgent):
        def _get_role(self) -> str:
            return "Neurologist"
            
    class Oncologist(CustomAgent):
        def _get_role(self) -> str:
            return "Oncologist"
    """
    
    def _get_role(self) -> str:
        """
        Override this method to define the role of your custom agent.
        
        Returns:
            str: The name of the medical specialty (e.g., "Neurologist", "Oncologist")
        """
        return "CustomSpecialist"
