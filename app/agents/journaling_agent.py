from .base_agent import BaseAgent
from pydantic import Field
from textblob import TextBlob
from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Dict
import datetime

# Load environment variables
load_dotenv()

class JournalingAgent(BaseAgent):
    """
    AI journaling assistant that analyzes user entries, extracts themes, and tracks moods.
    Provides deep insights into emotional patterns and recurring themes.
    """

    journal_entry: str = Field(
        ..., description="User's journal entry to analyze for sentiment and themes."
    )

    def _analyze_emotions(self) -> Dict:
        """
        Performs detailed emotion analysis using TextBlob and custom processing.
        """
        blob = TextBlob(self.journal_entry)
        
        # Get overall sentiment
        sentiment_score = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine mood category
        if sentiment_score > 0.3:
            mood = "Very Positive"
        elif 0 < sentiment_score <= 0.3:
            mood = "Slightly Positive"
        elif -0.3 <= sentiment_score < 0:
            mood = "Slightly Negative"
        elif sentiment_score < -0.3:
            mood = "Very Negative"
        else:
            mood = "Neutral"
            
        return {
            "mood": mood,
            "sentiment_score": round(sentiment_score, 2),
            "subjectivity": round(subjectivity, 2)
        }

    def _extract_themes(self) -> List[str]:
        """
        Uses OpenAI to identify themes and topics from the journal entry.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Analyze this journal entry and identify the main themes and topics.
        Focus on emotional states, situations, relationships, and personal growth areas.
        Return exactly 3-5 relevant themes as a comma-separated list.
        
        Journal Entry: {self.journal_entry}
        
        Themes:"""
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are an insightful journaling assistant that helps identify themes and patterns in personal writing."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                reasoning_effort="high"  # Deep analysis for theme extraction
            )
            
            themes = [theme.strip() for theme in response.choices[0].message.content.split(",")]
            return themes
            
        except Exception as e:
            return ["Error extracting themes"]

    def _generate_insights(self, emotion_data: Dict, themes: List[str]) -> str:
        """
        Generates personalized insights based on the analysis.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = f"""
        Based on this journal analysis, provide brief, insightful feedback.
        
        Analysis:
        - Mood: {emotion_data['mood']}
        - Sentiment: {emotion_data['sentiment_score']}
        - Themes: {', '.join(themes)}
        - Entry: {self.journal_entry}
        
        Provide 2-3 sentences of insight that:
        1. Acknowledge the emotional state
        2. Connect themes to potential patterns
        3. Offer a gentle perspective for reflection
        
        Response:"""
        
        try:
            response = client.chat.completions.create(
                model="o3-mini",
                messages=[
                    {"role": "developer", "content": "You are an empathetic journaling coach that provides gentle, insightful feedback."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                reasoning_effort="medium"  # Balanced approach for generating insights
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return "Unable to generate insights at this time."

    def run(self) -> Dict:
        """
        Analyzes journal entry for sentiment, themes, and generates insights.
        """
        try:
            # Perform emotion analysis
            emotion_data = self._analyze_emotions()
            
            # Extract themes
            themes = self._extract_themes()
            
            # Generate insights
            insights = self._generate_insights(emotion_data, themes)
            
            # Add timestamp
            timestamp = datetime.datetime.now().isoformat()
            
            return {
                "timestamp": timestamp,
                "emotion_analysis": emotion_data,
                "themes": themes,
                "insights": insights,
                "entry_length": len(self.journal_entry.split())
            }
            
        except Exception as e:
            return {
                "error": f"An error occurred during analysis: {str(e)}",
                "timestamp": datetime.datetime.now().isoformat()
            }


if __name__ == "__main__":
    # Example usage with different types of journal entries
    test_entries = [
        "I felt really overwhelmed at work today. The deadlines are piling up, and I'm not sure how to handle it all.",
        "Had an amazing day! Finally completed my project and my team was really supportive. Feeling proud of what we achieved.",
        "Feeling mixed emotions about my decision to change careers. Excited but nervous about the unknown."
    ]
    
    # Test the agent with the first entry
    agent = JournalingAgent(journal_entry=test_entries[0])
    result = agent.run()
    
    # Print results in a readable format
    print("\n📝 Journal Analysis Results:")
    print(f"Timestamp: {result['timestamp']}")
    print(f"\n🎭 Emotion Analysis:")
    print(f"Mood: {result['emotion_analysis']['mood']}")
    print(f"Sentiment Score: {result['emotion_analysis']['sentiment_score']}")
    print(f"Subjectivity: {result['emotion_analysis']['subjectivity']}")
    print(f"\n🏷️ Themes Identified:")
    for theme in result['themes']:
        print(f"• {theme}")
    print(f"\n💡 AI Insights:")
    print(result['insights'])
    print(f"\n📊 Entry Stats:")
    print(f"Word Count: {result['entry_length']}")
