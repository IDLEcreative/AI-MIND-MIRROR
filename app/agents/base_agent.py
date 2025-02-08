"""
Base agent class for Mind Mirror agents.
"""
from pydantic import BaseModel, Field
from typing import Dict, Any

class BaseAgent(BaseModel):
    """Base class for all Mind Mirror agents."""
    
    def run(self) -> Dict[str, Any]:
        """
        Main execution method that must be implemented by all agents.
        Returns a dictionary containing the agent's insights and analysis.
        """
        raise NotImplementedError("Each agent must implement its own run method.")
