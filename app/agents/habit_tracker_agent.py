from agency_swarm.tools import BaseTool
from pydantic import Field, BaseModel
from typing import List, Dict, Optional
import datetime
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class HabitLog(BaseModel):
    """Model for tracking individual habit logs"""
    date: str
    completed: bool
    notes: Optional[str] = None

class Habit(BaseModel):
    """Model for habit details"""
    name: str
    description: Optional[str]
    frequency: str  # daily, weekly, monthly
    target_days: List[str] = []  # e.g., ["Monday", "Wednesday", "Friday"] for weekly habits
    logs: List[HabitLog] = []
    created_at: str
    last_logged: str

class HabitTrackerAgent(BaseTool):
    """
    Advanced habit and goal tracking agent that provides insights,
    motivational feedback, and adaptive recommendations.
    """

    action: str = Field(
        ..., 
        description="Action to perform: 'log', 'analyze', or 'recommend'"
    )
    habit_data: Dict = Field(
        ..., 
        description="Habit information including name, logs, etc."
    )

    def _calculate_streak(self, logs: List[HabitLog], frequency: str) -> int:
        """
        Calculates the current streak taking into account habit frequency
        """
        if not logs:
            return 0

        logs.sort(key=lambda x: x['date'], reverse=True)
        streak = 0
        last_date = datetime.datetime.strptime(logs[0]['date'], "%Y-%m-%d")
        
        for log in logs:
            log_date = datetime.datetime.strptime(log['date'], "%Y-%m-%-d")
            date_diff = (last_date - log_date).days
            
            if frequency == "daily" and date_diff > 1:
                break
            elif frequency == "weekly" and date_diff > 7:
                break
            elif frequency == "monthly" and date_diff > 31:
                break
                
            if log['completed']:
                streak += 1
            else:
                break
                
            last_date = log_date
            
        return streak

    def _generate_motivation(self, habit: Dict, streak: int) -> str:
        """
        Generates personalized motivational message using OpenAI
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Generate a brief, motivational message for a user tracking their habit.
        
        Habit: {habit['name']}
        Description: {habit.get('description', '')}
        Current Streak: {streak} days
        Frequency: {habit['frequency']}
        
        Consider:
        1. Acknowledge their current progress
        2. Provide specific encouragement
        3. Keep it positive and actionable
        4. Keep it concise (2-3 sentences)
        
        Message:
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=100,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception:
            return f"Keep up your {habit['name']} streak of {streak} days! Every day counts!"

    def _analyze_progress(self, habit: Dict) -> Dict:
        """
        Analyzes habit progress and generates insights
        """
        total_logs = len(habit['logs'])
        completed_logs = sum(1 for log in habit['logs'] if log['completed'])
        
        if total_logs == 0:
            completion_rate = 0
        else:
            completion_rate = (completed_logs / total_logs) * 100
            
        streak = self._calculate_streak(habit['logs'], habit['frequency'])
        
        # Calculate trend (improving, declining, or stable)
        if total_logs >= 7:
            recent_rate = sum(1 for log in habit['logs'][-7:] if log['completed']) / 7 * 100
            older_rate = sum(1 for log in habit['logs'][-14:-7] if log['completed']) / 7 * 100
            
            if recent_rate > older_rate + 10:
                trend = "improving"
            elif recent_rate < older_rate - 10:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
            
        return {
            "total_days": total_logs,
            "completed_days": completed_logs,
            "completion_rate": round(completion_rate, 1),
            "current_streak": streak,
            "trend": trend
        }

    def _generate_recommendations(self, habit: Dict, analysis: Dict) -> List[str]:
        """
        Generates personalized recommendations based on habit analysis
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Generate 3 specific, actionable recommendations for improving habit adherence.
        
        Habit Details:
        - Name: {habit['name']}
        - Description: {habit.get('description', '')}
        - Frequency: {habit['frequency']}
        
        Current Progress:
        - Completion Rate: {analysis['completion_rate']}%
        - Current Streak: {analysis['current_streak']} days
        - Trend: {analysis['trend']}
        
        Provide 3 concise, specific recommendations that:
        1. Address current challenges
        2. Build on existing progress
        3. Are immediately actionable
        
        Format as a comma-separated list.
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            recommendations = [rec.strip() for rec in response.choices[0].message.content.split(",")]
            return recommendations[:3]  # Ensure we only return 3 recommendations
        except Exception:
            return ["Start small and build gradually",
                   "Set specific times for your habit",
                   "Track your progress daily"]

    def run(self) -> Dict:
        """
        Main function to handle habit tracking and analysis
        """
        try:
            habit = self.habit_data
            
            if self.action == "log":
                # Log new habit entry
                today = datetime.datetime.now().strftime("%Y-%m-%d")
                streak = self._calculate_streak(habit['logs'], habit['frequency'])
                motivation = self._generate_motivation(habit, streak)
                
                return {
                    "status": "success",
                    "streak": streak,
                    "motivation": motivation,
                    "timestamp": today
                }
                
            elif self.action == "analyze":
                # Analyze habit progress
                analysis = self._analyze_progress(habit)
                motivation = self._generate_motivation(habit, analysis['current_streak'])
                
                return {
                    "status": "success",
                    "analysis": analysis,
                    "motivation": motivation
                }
                
            elif self.action == "recommend":
                # Generate recommendations
                analysis = self._analyze_progress(habit)
                recommendations = self._generate_recommendations(habit, analysis)
                
                return {
                    "status": "success",
                    "recommendations": recommendations,
                    "analysis": analysis
                }
                
            else:
                return {
                    "status": "error",
                    "message": "Invalid action specified"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


if __name__ == "__main__":
    # Example habit data
    example_habit = {
        "name": "Meditation",
        "description": "15 minutes of mindfulness meditation",
        "frequency": "daily",
        "target_days": [],
        "created_at": "2024-01-01",
        "last_logged": "2024-01-28",
        "logs": [
            {"date": "2024-01-28", "completed": True, "notes": "Felt very focused"},
            {"date": "2024-01-27", "completed": True, "notes": "Short session but done"},
            {"date": "2024-01-26", "completed": True, "notes": None},
            {"date": "2024-01-25", "completed": False, "notes": "Too busy"},
        ]
    }
    
    # Test different actions
    actions = ["log", "analyze", "recommend"]
    
    for action in actions:
        print(f"\n🎯 Testing {action.upper()} action:")
        agent = HabitTrackerAgent(action=action, habit_data=example_habit)
        result = agent.run()
        print(json.dumps(result, indent=2))
