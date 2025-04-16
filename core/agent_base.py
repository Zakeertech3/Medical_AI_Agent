# core/agent_base.py
import os
import logging
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

from services.llm_service import LLMService
from config.settings import TEMPLATES_DIR

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """Abstract base class for medical specialty agents."""
    
    def __init__(self, 
                 llm_service: Optional[LLMService] = None,
                 temperature: float = 0.2,
                 max_tokens: int = 1024):
        """
        Initialize the base agent.
        
        Args:
            llm_service: LLM service for generating responses
            temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
            max_tokens: Maximum tokens in the response
        """
        self.llm_service = llm_service or LLMService()
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.role = self._get_role()
        self.prompt_template = self._load_prompt_template()
        
        logger.info(f"Initialized {self.role} agent")
    
    @abstractmethod
    def _get_role(self) -> str:
        """Return the role/specialty of this agent."""
        pass
    
    def _load_prompt_template(self) -> str:
        """Load the prompt template for this agent."""
        template_path = os.path.join(TEMPLATES_DIR, f"{self._get_role().lower()}_prompt.txt")
        try:
            with open(template_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            logger.warning(f"Prompt template not found for {self.role} at {template_path}")
            return self._get_default_prompt_template()
    
    def _get_default_prompt_template(self) -> str:
        """Return a default prompt template if no file is found."""
        return f"""
        Act like a {self.role}. You will receive a medical report of a patient.
        Task: Review the patient's report and provide a medical assessment based on your expertise.
        Focus: Identify potential issues related to your specialty that may explain the patient's symptoms.
        Recommendation: Suggest appropriate next steps, including additional tests or treatments.
        
        Patient Report: {{medical_report}}
        """
    
    def format_prompt(self, medical_report: str, **kwargs) -> str:
        """
        Format the prompt template with the medical report and other arguments.
        
        Args:
            medical_report: The patient's medical report
            **kwargs: Additional arguments to format into the prompt
            
        Returns:
            Formatted prompt string
        """
        context = {"medical_report": medical_report, **kwargs}
        return self.prompt_template.format(**context)
    
    def analyze(self, medical_report: str, **kwargs) -> str:
        """
        Analyze the medical report and generate recommendations.
        
        Args:
            medical_report: The patient's medical report
            **kwargs: Additional arguments to pass to the formatter
            
        Returns:
            Analysis results
        """
        logger.info(f"{self.role} agent analyzing report")
        prompt = self.format_prompt(medical_report, **kwargs)
        
        try:
            response = self.llm_service.generate_response(
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            logger.info(f"{self.role} agent completed analysis")
            return response
        except Exception as e:
            logger.error(f"Error in {self.role} agent analysis: {str(e)}")
            return f"Error during {self.role} analysis: {str(e)}"