"""
Catalyst Agent: Identifies breakthrough moments and opportunities for growth in journal entries.
"""
from typing import Dict, List, Any
from pydantic import Field
import os
from openai import OpenAI
from datetime import datetime
from .base_agent import BaseAgent

class CatalystAgent(BaseAgent):
    """Catalyst Agent that automatically identifies breakthrough moments and suggests growth opportunities."""
    
    journal_entries: List[Dict] = Field(
        ..., 
        description="List of journal entries to analyze for breakthroughs and opportunities."
    )

    def _identify_breakthrough_moments(self) -> List[Dict]:
        """
        Analyzes journal entries to identify potential breakthrough moments or challenges
        that could catalyze personal growth.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Prepare entries for analysis
        entries_text = "\n".join([
            f"Date: {entry.get('date', 'Unknown')}\nContent: {entry.get('content', '')}"
            for entry in self.journal_entries[-10:]  # Focus on recent entries
        ])
        
        prompt = f"""
        Analyze these journal entries for breakthrough moments, challenges, or opportunities:
        
        {entries_text}
        
        Identify:
        1. Key breakthrough moments
        2. Significant challenges that could lead to growth
        3. Emerging patterns or themes
        4. Potential opportunities for development
        
        Format as JSON with these keys: breakthroughs, challenges, themes, opportunities
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are a catalyst agent that identifies breakthrough moments and growth opportunities in journal entries."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="high"  # Deep analysis for meaningful insights
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": f"Error analyzing breakthroughs: {str(e)}"}

    def _generate_growth_suggestions(self, analysis: Dict) -> List[Dict]:
        """
        Generates personalized growth suggestions based on identified breakthroughs and patterns.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Based on this analysis of journal entries:
        {analysis}
        
        Generate 3 specific, actionable suggestions for personal growth that:
        1. Build on identified breakthrough moments
        2. Transform challenges into opportunities
        3. Align with emerging themes
        
        Format as JSON with keys: suggestion, rationale, action_steps
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are a catalyst agent specializing in transforming insights into growth opportunities."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="high"
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": f"Error generating suggestions: {str(e)}"}

    def run(self) -> Dict[str, Any]:
        """
        Main execution method that processes journal entries and returns insights and suggestions.
        """
        try:
            # Step 1: Identify breakthrough moments and patterns
            breakthrough_analysis = self._identify_breakthrough_moments()
            
            # Step 2: Generate growth suggestions
            growth_suggestions = self._generate_growth_suggestions(breakthrough_analysis)
            
            # Step 3: Compile results
            return {
                "timestamp": datetime.now().isoformat(),
                "analysis": breakthrough_analysis,
                "suggestions": growth_suggestions
            }
            
        except Exception as e:
            return {
                "error": f"Error in CatalystAgent: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

if __name__ == "__main__":
    # Example usage
    test_entries = [
        {
            "date": "2025-02-08",
            "content": "Today I finally overcame my fear of public speaking and gave a presentation. It went better than expected!"
        },
        {
            "date": "2025-02-07",
            "content": "Struggling with time management, but I'm starting to see patterns in my productivity."
        }
    ]
    
    agent = CatalystAgent(journal_entries=test_entries)
    results = agent.run()
    print(results)
