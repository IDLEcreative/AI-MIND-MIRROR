from pydantic import BaseModel, Field
from pydantic import Field, BaseModel
from typing import List, Dict, Optional
from openai import OpenAI
import os
from dotenv import load_dotenv
import datetime
import json

# Load environment variables
load_dotenv()

class WellBeingMetrics(BaseModel):
    """Model for tracking well-being metrics"""
    mood: int  # 1-10
    energy: int  # 1-10
    stress: int  # 1-10
    sleep_quality: Optional[int]  # 1-10
    social_connection: Optional[int]  # 1-10
    notes: Optional[str]

class CheckInAgent(BaseModel):
    """
    Advanced AI agent for conducting comprehensive mental well-being check-ins
    and providing personalized self-care recommendations.
    """

    metrics: Dict = Field(
        ..., 
        description="User's self-reported well-being metrics"
    )
    previous_checkins: Optional[List[Dict]] = Field(
        default=[],
        description="Previous check-in data for trend analysis"
    )

    def _analyze_trends(self) -> Dict:
        """
        Analyzes trends in well-being metrics over time
        """
        if not self.previous_checkins:
            return {"trend": "insufficient_data"}
            
        recent_mood_avg = sum(check['metrics']['mood'] for check in self.previous_checkins[-7:]) / min(7, len(self.previous_checkins))
        current_mood = self.metrics['mood']
        
        trend = {
            "mood_trend": "improving" if current_mood > recent_mood_avg + 1 
                         else "declining" if current_mood < recent_mood_avg - 1 
                         else "stable",
            "recent_mood_avg": round(recent_mood_avg, 1),
            "current_mood": current_mood
        }
        
        return trend

    def _generate_well_being_advice(self) -> Dict:
        """
        Generates personalized well-being recommendations using AI
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        trends = self._analyze_trends()
        
        prompt = f"""
        Generate personalized well-being recommendations based on the user's check-in data.
        
        Current Metrics:
        - Mood: {self.metrics['mood']}/10
        - Energy: {self.metrics['energy']}/10
        - Stress: {self.metrics['stress']}/10
        - Sleep Quality: {self.metrics.get('sleep_quality', 'Not reported')}/10
        - Social Connection: {self.metrics.get('social_connection', 'Not reported')}/10
        
        Trend: {trends['mood_trend']}
        Notes: {self.metrics.get('notes', 'No notes provided')}
        
        Provide recommendations in this JSON format:
        {{
            "immediate_actions": ["1-2 things to do right now"],
            "short_term": ["2-3 suggestions for today"],
            "long_term": ["1-2 habits to consider"],
            "encouragement": "A brief encouraging message",
            "focus_areas": ["Key areas needing attention"]
        }}
        
        Keep suggestions specific, actionable, and compassionate.
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are an empathetic well-being coach specializing in mental health analysis and personalized care recommendations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="high"  # Deep analysis for well-being insights
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return self._get_fallback_recommendations()

    def _get_fallback_recommendations(self) -> Dict:
        """
        Provides basic recommendations when AI generation fails
        """
        mood = self.metrics['mood']
        stress = self.metrics['stress']
        
        if mood < 4:
            return {
                "immediate_actions": ["Take 3 deep breaths", "Step outside for fresh air"],
                "short_term": ["Call a friend or family member", "Do something creative", "Take a relaxing bath"],
                "long_term": ["Consider starting a gratitude journal", "Develop a regular exercise routine"],
                "encouragement": "Remember that difficult moments are temporary. You're taking positive steps by checking in.",
                "focus_areas": ["Self-care", "Emotional support"]
            }
        elif mood < 7:
            return {
                "immediate_actions": ["Do a quick stretch", "Listen to uplifting music"],
                "short_term": ["Go for a walk", "Connect with a friend", "Try a new hobby"],
                "long_term": ["Build a morning routine", "Practice mindfulness"],
                "encouragement": "You're doing well! Keep building on your positive momentum.",
                "focus_areas": ["Mood enhancement", "Energy boosting"]
            }
        else:
            return {
                "immediate_actions": ["Celebrate this moment", "Share your positivity"],
                "short_term": ["Plan something fun", "Help someone else", "Try something new"],
                "long_term": ["Document what's working", "Share your strategies with others"],
                "encouragement": "Wonderful to see you thriving! Your positive habits are paying off.",
                "focus_areas": ["Maintaining momentum", "Sharing joy"]
            }

    def _generate_insight_summary(self, recommendations: Dict) -> str:
        """
        Creates a user-friendly summary of insights and recommendations
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Create a brief, encouraging summary of the user's well-being check-in.
        
        Metrics:
        - Mood: {self.metrics['mood']}/10
        - Energy: {self.metrics['energy']}/10
        - Stress: {self.metrics['stress']}/10
        
        Key Recommendations:
        {json.dumps(recommendations, indent=2)}
        
        Create a 2-3 sentence summary that:
        1. Acknowledges their current state
        2. Highlights key recommendations
        3. Ends with encouragement
        
        Summary:
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "system", "content": prompt}],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception:
            return "Thank you for checking in. Focus on your recommended actions, and remember that small steps lead to significant progress."

    def run(self) -> Dict:
        """
        Processes the check-in and provides comprehensive well-being feedback
        """
        try:
            # Get recommendations
            recommendations = self._generate_well_being_advice()
            
            # Generate summary
            summary = self._generate_insight_summary(recommendations)
            
            # Analyze trends
            trends = self._analyze_trends()
            
            return {
                "timestamp": datetime.datetime.now().isoformat(),
                "metrics": self.metrics,
                "trends": trends,
                "recommendations": recommendations,
                "summary": summary,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "timestamp": datetime.datetime.now().isoformat()
            }


if __name__ == "__main__":
    # Example check-in data
    metrics = {
        "mood": 6,
        "energy": 7,
        "stress": 4,
        "sleep_quality": 8,
        "social_connection": 7,
        "notes": "Feeling okay but a bit overwhelmed with work"
    }
    
    # Previous check-ins for trend analysis
    previous_checkins = [
        {
            "timestamp": "2024-01-30T10:00:00",
            "metrics": {"mood": 7, "energy": 8, "stress": 3}
        },
        {
            "timestamp": "2024-01-29T10:00:00",
            "metrics": {"mood": 5, "energy": 6, "stress": 6}
        }
    ]
    
    # Run check-in
    agent = CheckInAgent(metrics=metrics, previous_checkins=previous_checkins)
    result = agent.run()
    
    # Print results in a readable format
    print("\n🌟 Well-being Check-in Results:")
    print(f"\n📊 Current Metrics:")
    for metric, value in result['metrics'].items():
        if metric != 'notes':
            print(f"• {metric.replace('_', ' ').title()}: {value}/10")
    
    print(f"\n📈 Trends:")
    for key, value in result['trends'].items():
        print(f"• {key.replace('_', ' ').title()}: {value}")
    
    print(f"\n💭 Summary:")
    print(result['summary'])
    
    print(f"\n🎯 Recommendations:")
    for category, items in result['recommendations'].items():
        if category != 'encouragement':
            print(f"\n{category.replace('_', ' ').title()}:")
            for item in items:
                print(f"• {item}")
    
    print(f"\n💝 {result['recommendations']['encouragement']}")
