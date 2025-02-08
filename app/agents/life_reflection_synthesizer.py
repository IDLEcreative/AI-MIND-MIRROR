"""
Life Reflection Synthesizer: Creates a cohesive narrative from journal entries, highlighting growth and milestones.
"""
from typing import Dict, List, Any
from pydantic import Field
import os
from openai import OpenAI
from datetime import datetime
from .base_agent import BaseAgent

class LifeReflectionSynthesizer(BaseAgent):
    """Agent that synthesizes journal entries into a meaningful life narrative."""
    
    journal_archive: List[Dict] = Field(
        ..., 
        description="Archive of journal entries to synthesize into a narrative."
    )
    
    def _identify_key_moments(self) -> Dict:
        """
        Identifies significant moments, milestones, and turning points from journal entries.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Prepare archive for analysis
        archive_text = "\n".join([
            f"Date: {entry.get('date', 'Unknown')}\nContent: {entry.get('content', '')}"
            for entry in self.journal_archive
        ])
        
        prompt = f"""
        Analyze these journal entries to identify key life moments and patterns:
        
        {archive_text}
        
        Identify:
        1. Major milestones and achievements
        2. Significant turning points
        3. Important lessons learned
        4. Recurring themes or values
        
        Format as JSON with these keys: milestones, turning_points, lessons, themes
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are a life reflection synthesizer that identifies meaningful patterns and moments in personal narratives."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="high"  # Deep analysis for life patterns
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": f"Error identifying key moments: {str(e)}"}

    def _create_narrative(self, key_moments: Dict) -> Dict:
        """
        Creates a cohesive narrative based on identified key moments and patterns.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Based on these key moments and patterns:
        {key_moments}
        
        Create a meaningful narrative that:
        1. Connects major life events and turning points
        2. Highlights personal growth and development
        3. Identifies recurring themes and values
        4. Suggests future directions based on past patterns
        
        Format as JSON with keys: narrative_summary, growth_journey, core_themes, future_directions
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are a life reflection synthesizer that creates meaningful narratives from personal experiences."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="high"
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": f"Error creating narrative: {str(e)}"}

    def run(self) -> Dict[str, Any]:
        """
        Main execution method that synthesizes journal entries into a cohesive narrative.
        """
        try:
            # Step 1: Identify key moments and patterns
            key_moments = self._identify_key_moments()
            
            # Step 2: Create narrative synthesis
            narrative = self._create_narrative(key_moments)
            
            # Step 3: Compile results
            return {
                "timestamp": datetime.now().isoformat(),
                "key_moments": key_moments,
                "narrative_synthesis": narrative
            }
            
        except Exception as e:
            return {
                "error": f"Error in LifeReflectionSynthesizer: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

if __name__ == "__main__":
    # Example usage
    test_archive = [
        {
            "date": "2025-02-08",
            "content": "Reflecting on my journey this year - from career change to personal growth."
        },
        {
            "date": "2025-01-15",
            "content": "Made the difficult decision to switch careers. Feeling both scared and excited."
        }
    ]
    
    agent = LifeReflectionSynthesizer(journal_archive=test_archive)
    results = agent.run()
    print(results)
