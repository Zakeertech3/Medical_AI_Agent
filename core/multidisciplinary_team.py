# core/multidisciplinary_team.py
import logging
from typing import Dict, Optional

from services.llm_service import LLMService
from core.agent_base import BaseAgent
from config.settings import TEMPLATES_DIR
import os

logger = logging.getLogger(__name__)

class MultidisciplinaryTeam(BaseAgent):
    """
    Agent that synthesizes assessments from multiple specialists.
    """
    
    def __init__(self, 
                 specialist_reports: Dict[str, str],
                 llm_service: Optional[LLMService] = None,
                 temperature: float = 0.2,
                 max_tokens: int = 1024):
        """
        Initialize the multidisciplinary team agent.
        
        Args:
            specialist_reports: Dictionary mapping specialist roles to their assessments
            llm_service: LLM service for generating responses
            temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
            max_tokens: Maximum tokens in the response
        """
        self.specialist_reports = specialist_reports
        super().__init__(llm_service, temperature, max_tokens)
    
    def _get_role(self) -> str:
        return "MultidisciplinaryTeam"
    
    def _get_default_prompt_template(self) -> str:
        """Return a default prompt template if no file is found."""
        return """
        Act like a multidisciplinary team of healthcare professionals.
        You will receive assessments from different medical specialists about a patient case.
        
        Task: Review the specialists' reports, analyze them together, and come up with a list of 3 possible health issues of the patient.
        
        Return only a list of bullet points of 3 possible health issues of the patient and for each issue provide the reason.
        
        Specialists' Reports:
        {specialist_reports}
        """
    
    def format_prompt(self, **kwargs) -> str:
        """
        Format the prompt with specialist reports.
        
        Returns:
            Formatted prompt string
        """
        # Format the specialist reports into a single string
        specialist_text = ""
        for role, report in self.specialist_reports.items():
            specialist_text += f"\n\n{role} Report:\n{report}"
        
        context = {"specialist_reports": specialist_text, **kwargs}
        return self.prompt_template.format(**context)
    
    def analyze(self, **kwargs) -> str:
        """
        Analyze the specialists' reports and generate a comprehensive assessment.
        
        Returns:
            Final assessment
        """
        logger.info("Multidisciplinary team analyzing specialist reports")
        prompt = self.format_prompt(**kwargs)
        
        try:
            response = self.llm_service.generate_response(
                prompt=prompt,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            logger.info("Multidisciplinary team completed analysis")
            return response
        except Exception as e:
            logger.error(f"Error in multidisciplinary team analysis: {str(e)}")
            return f"Error during multidisciplinary team analysis: {str(e)}"