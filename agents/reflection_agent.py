from agency_swarm.tools import BaseTool
from pydantic import Field
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ReflectionAgent(BaseTool):
    """
    The AI Mirror agent that engages users in deep self-reflection.
    It uses structured questioning and cognitive bias detection to encourage introspection.
    """

    user_input: str = Field(
        ..., description="User's response or reflection input for the AI to analyze."
    )

    def run(self):
        """
        Uses AI to engage in introspective conversation.
        Returns a structured response with insights and follow-up questions.
        """
        # Initialize OpenAI client
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Prompt engineering for deep reflection
        prompt = f"""
        You are an AI Mirror, a deep reflection coach. Your goal is to guide users in self-discovery.
        
        Guidelines for analysis:
        1. Listen actively and identify underlying themes
        2. Detect cognitive biases or limiting beliefs
        3. Frame questions that promote deeper insight
        4. Offer gentle reframing of negative patterns
        5. Maintain a supportive, non-judgmental tone
        
        User's Reflection: {self.user_input}

        Provide a response that includes:
        1. A brief summary of understood feelings/situation
        2. Identification of potential biases or patterns
        3. 2-3 thought-provoking follow-up questions
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": prompt}
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"An error occurred during reflection: {str(e)}"


if __name__ == "__main__":
    # Example usage
    agent = ReflectionAgent(user_input="I feel stuck in my career but don't know what to do.")
    print(agent.run())
