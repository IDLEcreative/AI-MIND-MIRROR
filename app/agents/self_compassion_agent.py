"""
Self-Compassion Agent: Identifies self-criticism and generates compassionate reframing suggestions.
"""
from typing import Dict, List, Any
from pydantic import Field
import os
from openai import OpenAI
from datetime import datetime
from .base_agent import BaseAgent

class SelfCompassionAgent(BaseAgent):
    """Agent that promotes self-compassion by identifying and reframing negative self-talk."""
    
    journal_entries: List[Dict] = Field(
        ..., 
        description="Journal entries to analyze for self-talk patterns."
    )
    
    def _analyze_self_talk(self) -> Dict:
        """
        Analyzes journal entries to identify patterns of self-criticism and negative self-talk.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Prepare entries for analysis
        entries_text = "\n".join([
            f"Date: {entry.get('date', 'Unknown')}\nContent: {entry.get('content', '')}"
            for entry in self.journal_entries[-10:]  # Focus on recent entries
        ])
        
        prompt = f"""
        Analyze these journal entries for patterns of self-talk:
        
        {entries_text}
        
        Identify:
        1. Instances of self-criticism or harsh self-judgment
        2. Recurring negative thought patterns
        3. Areas where self-compassion is needed
        4. Existing positive self-talk patterns
        
        Format as JSON with these keys: self_criticism, thought_patterns, compassion_needs, positive_patterns
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are a self-compassion agent that identifies and reframes negative self-talk patterns."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="high"  # Deep analysis for self-talk patterns
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": f"Error analyzing self-talk: {str(e)}"}

    def _generate_compassionate_responses(self, self_talk_analysis: Dict) -> Dict:
        """
        Generates compassionate reframing and self-supportive statements.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Based on this self-talk analysis:
        {self_talk_analysis}
        
        Generate:
        1. Compassionate reframing statements for identified self-criticism
        2. Gentle reminders for self-kindness
        3. Positive affirmations based on strengths
        4. Practical self-compassion exercises
        
        Format as JSON with keys: reframing, reminders, affirmations, exercises
        Ensure responses are gentle, supportive, and grounded in self-compassion.
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are a self-compassion agent specializing in gentle, supportive reframing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="high"
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": f"Error generating compassionate responses: {str(e)}"}

    def run(self) -> Dict[str, Any]:
        """
        Main execution method that analyzes self-talk and generates compassionate responses.
        """
        try:
            # Step 1: Analyze self-talk patterns
            self_talk_analysis = self._analyze_self_talk()
            
            # Step 2: Generate compassionate responses
            compassionate_responses = self._generate_compassionate_responses(self_talk_analysis)
            
            # Step 3: Compile results
            return {
                "timestamp": datetime.now().isoformat(),
                "self_talk_analysis": self_talk_analysis,
                "compassionate_responses": compassionate_responses
            }
            
        except Exception as e:
            return {
                "error": f"Error in SelfCompassionAgent: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

if __name__ == "__main__":
    # Example usage
    test_entries = [
        {
            "date": "2025-02-08",
            "content": "I keep making the same mistakes. Why can't I get better at this?"
        },
        {
            "date": "2025-02-07",
            "content": "Feeling like I'm not good enough for this project."
        }
    ]
    
    agent = SelfCompassionAgent(journal_entries=test_entries)
    results = agent.run()
    print(results)
