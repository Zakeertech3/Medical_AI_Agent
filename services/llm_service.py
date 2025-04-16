# services/llm_service.py
import os
import logging
from groq import Groq
from typing import Dict, Any, Optional

from config.settings import GROQ_API_KEY, GROQ_MODEL

logger = logging.getLogger(__name__)

class LLMService:
    """Service for interacting with the Groq LLM API."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the LLM service.
        
        Args:
            api_key: Groq API key (defaults to environment variable)
            model: Model identifier (defaults to environment variable)
        """
        self.api_key = api_key or GROQ_API_KEY
        self.model = model or GROQ_MODEL
        
        if not self.api_key:
            raise ValueError("Groq API key is required. Set GROQ_API_KEY environment variable or pass it explicitly.")
        
        self.client = Groq(api_key=self.api_key)
        logger.info(f"LLM Service initialized with model: {self.model}")
    
    def generate_response(self, prompt: str, temperature: float = 0.2, max_tokens: int = 1024) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The input prompt text
            temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
            max_tokens: Maximum tokens in the response
            
        Returns:
            Generated text response
        """
        try:
            logger.debug(f"Sending prompt to LLM (length: {len(prompt)})")
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful medical assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            response = completion.choices[0].message.content
            logger.debug(f"Received response from LLM (length: {len(response)})")
            return response
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            raise