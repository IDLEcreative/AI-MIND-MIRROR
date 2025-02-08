"""
Behavior Change Agent: Identifies behavioral patterns and suggests subtle modifications for positive change.
"""
from typing import Dict, List, Any
from pydantic import Field
import os
from openai import OpenAI
from datetime import datetime
from .base_agent import BaseAgent

class BehaviorChangeAgent(BaseAgent):
    """Agent that detects behavioral patterns and recommends subtle modifications."""
    
    journal_entries: List[Dict] = Field(
        ..., 
        description="Journal entries to analyze for behavioral patterns."
    )
    
    def _analyze_behavior_patterns(self) -> Dict:
        """
        Analyzes journal entries to identify recurring behavioral patterns and self-talk.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Prepare entries for analysis
        entries_text = "\n".join([
            f"Date: {entry.get('date', 'Unknown')}\nContent: {entry.get('content', '')}"
            for entry in self.journal_entries[-15:]  # Focus on recent entries
        ])
        
        prompt = f"""
        Analyze these journal entries for behavioral patterns and self-talk:
        
        {entries_text}
        
        Identify:
        1. Recurring behavioral patterns (both positive and negative)
        2. Self-limiting beliefs or self-sabotaging language
        3. Triggers for specific behaviors
        4. Current coping mechanisms
        
        Format as JSON with these keys: patterns, beliefs, triggers, coping_mechanisms
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are a behavior change agent that identifies patterns and suggests modifications."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="high"  # Deep analysis for behavioral patterns
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": f"Error analyzing patterns: {str(e)}"}

    def _generate_behavior_modifications(self, pattern_analysis: Dict) -> Dict:
        """
        Generates subtle behavior modification suggestions based on identified patterns.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Based on this behavioral pattern analysis:
        {pattern_analysis}
        
        Suggest subtle modifications that:
        1. Address identified negative patterns
        2. Reinforce positive behaviors
        3. Help reframe limiting beliefs
        4. Enhance existing coping mechanisms
        
        Format as JSON with keys: modifications, rationale, implementation_steps
        Keep suggestions subtle and easily implementable.
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are a behavior change agent specializing in subtle, effective modifications."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="high"
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": f"Error generating modifications: {str(e)}"}

    def run(self) -> Dict[str, Any]:
        """
        Main execution method that analyzes patterns and suggests behavioral modifications.
        """
        try:
            # Step 1: Analyze behavioral patterns
            pattern_analysis = self._analyze_behavior_patterns()
            
            # Step 2: Generate modification suggestions
            modifications = self._generate_behavior_modifications(pattern_analysis)
            
            # Step 3: Compile results
            return {
                "timestamp": datetime.now().isoformat(),
                "pattern_analysis": pattern_analysis,
                "suggested_modifications": modifications
            }
            
        except Exception as e:
            return {
                "error": f"Error in BehaviorChangeAgent: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

if __name__ == "__main__":
    # Example usage
    test_entries = [
        {
            "date": "2025-02-08",
            "content": "Procrastinated again on the important task, but managed to complete it last minute."
        },
        {
            "date": "2025-02-07",
            "content": "Found myself doubting my abilities during the team meeting."
        }
    ]
    
    agent = BehaviorChangeAgent(journal_entries=test_entries)
    results = agent.run()
    print(results)
