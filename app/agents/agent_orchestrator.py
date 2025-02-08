"""
Agent Orchestrator: Coordinates the interaction between different agents to provide holistic insights.
"""
from typing import Dict, List, Any
from datetime import datetime
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from .habit_tracker_agent import HabitTrackerAgent
from .checkin_agent import CheckInAgent
from .journaling_agent import JournalingAgent
from .reflection_agent import ReflectionAgent
from .catalyst_agent import CatalystAgent
from .emotional_forecasting_agent import EmotionalForecastingAgent
from .behavior_change_agent import BehaviorChangeAgent
from .life_reflection_synthesizer import LifeReflectionSynthesizer
from .self_compassion_agent import SelfCompassionAgent
from pydantic import BaseModel, Field

class AgentOrchestrator(BaseModel):
    """Orchestrates the interaction between different agents to provide comprehensive insights."""
    
    journal_data: Dict = Field(
        ..., 
        description="Complete journal data including entries, habits, check-ins, and reflections."
    )
    
    def _run_agents(self) -> Dict[str, Any]:
        """
        Runs all agents in parallel and collects their insights.
        """
        try:
            # Initialize all agents with the appropriate data
            habit = HabitTrackerAgent(habits=self.journal_data.get("habits", []))
            checkin = CheckInAgent(metrics=self.journal_data.get("well_being_metrics", []))
            journaling = JournalingAgent(journal_entries=self.journal_data.get("journal_entries", []))
            reflection = ReflectionAgent(entries=self.journal_data.get("journal_entries", []))
            catalyst = CatalystAgent(journal_entries=self.journal_data.get("journal_entries", []))
            emotional = EmotionalForecastingAgent(journal_history=self.journal_data.get("journal_entries", []))
            behavior = BehaviorChangeAgent(journal_entries=self.journal_data.get("journal_entries", []))
            life_reflection = LifeReflectionSynthesizer(journal_archive=self.journal_data.get("journal_entries", []))
            compassion = SelfCompassionAgent(journal_entries=self.journal_data.get("journal_entries", []))
            
            # Collect insights from all agents
            return {
                "habit_insights": habit.run(),
                "well_being_insights": checkin.run(),
                "journal_analysis": journaling.run(),
                "reflection_insights": reflection.run(),
                "catalyst_insights": catalyst.run(),
                "emotional_forecasts": emotional.run(),
                "behavior_insights": behavior.run(),
                "life_narrative": life_reflection.run(),
                "compassion_guidance": compassion.run()
            }
            
            return insights
            
        except Exception as e:
            return {"error": f"Error running agents: {str(e)}"}

    def _synthesize_insights(self, agent_insights: Dict) -> Dict:
        """
        Synthesizes insights from all agents into cohesive recommendations.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Synthesize these multi-agent insights into cohesive, actionable guidance:
        
        Agent Insights: {json.dumps(agent_insights, indent=2)}
        
        Create a holistic summary that:
        1. Identifies key themes across all agent analyses
        2. Highlights important patterns and connections
        3. Provides prioritized, actionable recommendations
        4. Suggests areas for focused attention
        
        Format as JSON with keys: themes, patterns, recommendations, focus_areas
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are an insight synthesizer that creates cohesive guidance from multi-agent analyses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="high"
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return {"error": f"Error synthesizing insights: {str(e)}"}

    def run(self) -> Dict[str, Any]:
        """
        Main execution method that orchestrates all agents and synthesizes their insights.
        """
        try:
            # Step 1: Run all agents
            agent_insights = self._run_agents()
            
            # Step 2: Synthesize insights
            synthesis = self._synthesize_insights(agent_insights)
            
            # Step 3: Compile final results
            return {
                "timestamp": datetime.now().isoformat(),
                "agent_insights": agent_insights,
                "holistic_synthesis": synthesis
            }
            
        except Exception as e:
            return {
                "error": f"Error in AgentOrchestrator: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

if __name__ == "__main__":
    # Example usage
    test_entries = [
        {
            "date": "2025-02-08",
            "content": "Made progress on the project today. Still doubting my abilities sometimes.",
            "emotion": "mixed"
        },
        {
            "date": "2025-02-07",
            "content": "Trying to establish better work habits. It's challenging but I'm seeing small improvements.",
            "emotion": "hopeful"
        }
    ]
    
    orchestrator = AgentOrchestrator(journal_entries=test_entries)
    results = orchestrator.run()
    print(json.dumps(results, indent=2))
