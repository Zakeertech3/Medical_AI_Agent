# core/agent_factory.py
import logging
from typing import Dict, Type, Optional

from core.agent_base import BaseAgent
from agents.cardiologist import Cardiologist
from agents.psychologist import Psychologist
from agents.pulmonologist import Pulmonologist
from services.llm_service import LLMService

logger = logging.getLogger(__name__)

class AgentFactory:
    """Factory for creating different types of medical specialist agents."""
    
    # Registry of available agent types
    AGENT_REGISTRY: Dict[str, Type[BaseAgent]] = {
        "cardiologist": Cardiologist,
        "psychologist": Psychologist,
        "pulmonologist": Pulmonologist,
    }
    
    @classmethod
    def register_agent(cls, agent_type: str, agent_class: Type[BaseAgent]) -> None:
        """
        Register a new agent type.
        
        Args:
            agent_type: Lowercase string identifier for the agent type
            agent_class: The agent class to register
        """
        cls.AGENT_REGISTRY[agent_type.lower()] = agent_class
        logger.info(f"Registered new agent type: {agent_type}")
    
    @classmethod
    def create_agent(cls, 
                    agent_type: str, 
                    llm_service: Optional[LLMService] = None,
                    temperature: float = 0.2,
                    max_tokens: int = 1024) -> BaseAgent:
        """
        Create an agent of the specified type.
        
        Args:
            agent_type: Type of agent to create (must be in AGENT_REGISTRY)
            llm_service: LLM service to use (will create one if None)
            temperature: LLM temperature setting
            max_tokens: LLM max tokens setting
            
        Returns:
            Initialized agent instance
            
        Raises:
            ValueError: If agent_type is not registered
        """
        agent_type = agent_type.lower()
        if agent_type not in cls.AGENT_REGISTRY:
            raise ValueError(f"Unknown agent type: {agent_type}. Available types: {', '.join(cls.AGENT_REGISTRY.keys())}")
        
        agent_class = cls.AGENT_REGISTRY[agent_type]
        
        # Create a shared LLM service if one wasn't provided
        if llm_service is None:
            llm_service = LLMService()
            
        return agent_class(
            llm_service=llm_service,
            temperature=temperature,
            max_tokens=max_tokens
        )