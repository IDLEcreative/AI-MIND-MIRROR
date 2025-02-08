"""
Emotional Forecasting Agent: Predicts emotional trends and provides proactive guidance based on journal history.
"""
from typing import Dict, List, Any
from pydantic import Field
import os
from openai import OpenAI
from datetime import datetime, timedelta
from .base_agent import BaseAgent

class EmotionalForecastingAgent(BaseAgent):
    """Agent that analyzes emotional patterns and predicts future emotional states."""
    
    journal_history: List[Dict] = Field(
        ..., 
        description="Historical journal entries with emotional content and metadata."
    )
    
    def _analyze_emotional_patterns(self) -> Dict:
        """
        Analyzes historical emotional patterns and trends from journal entries.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Prepare historical data for analysis
        history_text = "\n".join([
            f"Date: {entry.get('date', 'Unknown')}\n"
            f"Emotion: {entry.get('emotion', 'Unknown')}\n"
            f"Content: {entry.get('content', '')}"
            for entry in self.journal_history[-20:]  # Focus on recent history
        ])
        
        prompt = f"""
        Analyze these journal entries for emotional patterns and trends:
        
        {history_text}
        
        Identify:
        1. Recurring emotional patterns
        2. Triggers or catalysts for emotional changes
        3. Time-based patterns (daily, weekly cycles)
        4. Current emotional trajectory
        
        Format as JSON with these keys: patterns, triggers, cycles, trajectory
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are an emotional forecasting agent that identifies patterns and predicts future states."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="high"  # Deep analysis for emotional patterns
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": f"Error analyzing patterns: {str(e)}"}

    def _generate_emotional_forecast(self, pattern_analysis: Dict) -> Dict:
        """
        Generates emotional forecasts and preventive suggestions based on pattern analysis.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Based on this emotional pattern analysis:
        {pattern_analysis}
        
        Provide:
        1. Short-term emotional forecast (next 3-7 days)
        2. Potential challenging periods ahead
        3. Preventive measures for emotional well-being
        4. Specific strategies for maintaining emotional balance
        
        Format as JSON with keys: forecast, challenges, preventive_measures, strategies
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are an emotional forecasting agent that predicts future states and suggests preventive measures."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="high"
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": f"Error generating forecast: {str(e)}"}

    def run(self) -> Dict[str, Any]:
        """
        Main execution method that analyzes patterns and generates emotional forecasts.
        """
        try:
            # Step 1: Analyze emotional patterns
            pattern_analysis = self._analyze_emotional_patterns()
            
            # Step 2: Generate forecast and recommendations
            forecast = self._generate_emotional_forecast(pattern_analysis)
            
            # Step 3: Compile results
            return {
                "timestamp": datetime.now().isoformat(),
                "pattern_analysis": pattern_analysis,
                "forecast": forecast,
                "next_update": (datetime.now() + timedelta(days=1)).isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Error in EmotionalForecastingAgent: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

if __name__ == "__main__":
    # Example usage
    test_history = [
        {
            "date": "2025-02-08",
            "emotion": "optimistic",
            "content": "Feeling positive about the progress I'm making with my projects."
        },
        {
            "date": "2025-02-07",
            "emotion": "stressed",
            "content": "Deadline pressure is building up, but I'm managing it step by step."
        }
    ]
    
    agent = EmotionalForecastingAgent(journal_history=test_history)
    results = agent.run()
    print(results)
