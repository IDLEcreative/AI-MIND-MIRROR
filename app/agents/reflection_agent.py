from .base_agent import BaseAgent
from pydantic import Field, BaseModel
from typing import List, Dict, Optional
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class ReflectionInsights(BaseModel):
    """Structure for reflection analysis results"""
    themes: List[str]
    cognitive_biases: List[str]
    emotional_state: Dict[str, float]
    follow_up_questions: List[str]
    reframing_suggestions: Optional[List[str]]
    summary: str

class ReflectionAgent(BaseAgent):
    """
    The AI Mirror agent that engages users in deep self-reflection.
    It uses structured questioning and cognitive bias detection to encourage introspection.
    """

    user_input: str = Field(
        ..., description="User's response or reflection input for the AI to analyze."
    )
    previous_reflections: Optional[List[Dict]] = Field(
        default=[],
        description="Previous reflection data for context and pattern recognition"
    )

    def _analyze_cognitive_biases(self) -> List[str]:
        """
        Analyzes the text for common cognitive biases
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Analyze this reflection for potential cognitive biases. Consider common biases like:
        - All-or-nothing thinking
        - Overgeneralization
        - Mental filtering
        - Jumping to conclusions
        - Catastrophizing
        - Emotional reasoning
        - Should statements
        - Personalization
        
        Text: {self.user_input}
        
        Return only the names of 1-3 most relevant biases as a comma-separated list.
        If no clear biases are present, return "none detected".
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are an expert in cognitive psychology, specializing in identifying cognitive biases and thought patterns."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                reasoning_effort="high"  # Deep analysis for cognitive bias detection
            )
            
            biases = response.choices[0].message.content.split(",")
            return [b.strip() for b in biases if b.strip().lower() != "none detected"]
        except Exception:
            return []

    def _extract_themes_and_emotions(self) -> Dict:
        """
        Extracts main themes and emotional content from the reflection
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Analyze this reflection for main themes and emotional content.
        
        Text: {self.user_input}
        
        Respond in JSON format:
        {{
            "themes": ["2-3 main themes"],
            "emotions": {{"emotion": "intensity_0_to_1"}}
        }}
        """
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are an expert in cognitive psychology, specializing in identifying cognitive biases and thought patterns."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                reasoning_effort="high"  # Deep analysis for cognitive bias detection
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception:
            return {"themes": [], "emotions": {}}

    def _generate_questions_and_reframing(self, biases: List[str], themes: List[str]) -> Dict:
        """
        Generates insightful questions and reframing suggestions
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Generate follow-up questions and reframing suggestions based on this reflection.
        
        Context:
        - Text: {self.user_input}
        - Identified Biases: {', '.join(biases) if biases else 'None detected'}
        - Main Themes: {', '.join(themes)}
        
        Respond in JSON format:
        {{
            "questions": ["2-3 thought-provoking questions"],
            "reframing": ["1-2 gentle reframing suggestions"]
        }}
        
        Guidelines:
        - Questions should be open-ended and promote deeper insight
        - Use "what" and "how" more than "why"
        - Reframing should be gentle and supportive
        - Focus on growth and possibility
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7
            )
            
            return json.loads(response.choices[0].message.content)
        except Exception:
            return {
                "questions": ["What else might be influencing this situation?"],
                "reframing": ["Consider viewing this as an opportunity for growth"]
            }

    def _generate_summary(self, insights: ReflectionInsights) -> str:
        """
        Generates a compassionate summary of the reflection analysis
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Create a brief, empathetic summary of this reflection analysis.
        
        Insights:
        - Themes: {', '.join(insights.themes)}
        - Emotions: {insights.emotional_state}
        - Biases: {', '.join(insights.cognitive_biases) if insights.cognitive_biases else 'None detected'}
        
        Original Text: {self.user_input}
        
        Create a 2-3 sentence summary that:
        1. Acknowledges the core feelings/situation
        2. Highlights key patterns or insights
        3. Offers gentle encouragement
        
        Summary:
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[{"role": "system", "content": prompt}],
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        except Exception:
            return "Thank you for sharing your reflection. I notice some important themes and patterns that we can explore further."

    def run(self) -> Dict:
        """
        Main function to process reflection and generate insights
        """
        try:
            # Analyze cognitive biases
            biases = self._analyze_cognitive_biases()
            
            # Extract themes and emotions
            content_analysis = self._extract_themes_and_emotions()
            
            # Generate questions and reframing suggestions
            guidance = self._generate_questions_and_reframing(
                biases=biases,
                themes=content_analysis.get('themes', [])
            )
            
            # Create insights object
            insights = ReflectionInsights(
                themes=content_analysis.get('themes', []),
                cognitive_biases=biases,
                emotional_state=content_analysis.get('emotions', {}),
                follow_up_questions=guidance.get('questions', []),
                reframing_suggestions=guidance.get('reframing', []),
                summary=""  # Will be filled below
            )
            
            # Generate summary
            insights.summary = self._generate_summary(insights)
            
            # Format response
            return {
                "status": "success",
                "insights": insights.dict(),
                "reflection_text": self.user_input
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "reflection_text": self.user_input
            }


if __name__ == "__main__":
    # Example usage
    test_reflections = [
        "I feel stuck in my career but don't know what to do. Every time I think about changing jobs, I worry about making the wrong choice.",
        "Today was amazing! I finally completed a project I've been working on for months. My team was really supportive.",
        "I keep procrastinating on important tasks and then feel guilty about it. I should be more disciplined."
    ]
    
    # Test with first reflection
    agent = ReflectionAgent(user_input=test_reflections[0])
    result = agent.run()
    
    # Print results in a readable format
    print("\n🤔 Reflection Analysis:")
    if result["status"] == "success":
        insights = result["insights"]
        
        print("\n💭 Summary:")
        print(insights["summary"])
        
        print("\n🎯 Main Themes:")
        for theme in insights["themes"]:
            print(f"• {theme}")
            
        if insights["cognitive_biases"]:
            print("\n🔍 Thinking Patterns to Consider:")
            for bias in insights["cognitive_biases"]:
                print(f"• {bias}")
        
        print("\n❓ Questions to Explore:")
        for question in insights["follow_up_questions"]:
            print(f"• {question}")
            
        if insights["reframing_suggestions"]:
            print("\n💡 Alternative Perspectives:")
            for suggestion in insights["reframing_suggestions"]:
                print(f"• {suggestion}")
                
        print("\n📊 Emotional Insights:")
        for emotion, intensity in insights["emotional_state"].items():
            print(f"• {emotion}: {int(intensity * 100)}%")
    else:
        print(f"Error: {result['message']}")
