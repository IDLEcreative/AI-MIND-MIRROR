import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from datetime import datetime

from app.agents.agent_orchestrator import AgentOrchestrator

# Define a dummy run method that returns a simple dictionary for testing

def dummy_run(self):
    return {"dummy": True}


@pytest.mark.integration
def test_journal_processing(monkeypatch):
    # Create a dummy agent class that returns meaningful test data
    class TestAgent:
        def __init__(self, **kwargs):
            pass

        def run(self):
            return {
                "analysis": "Test analysis",
                "recommendations": ["Test recommendation 1", "Test recommendation 2"],
                "confidence": 0.85
            }

    # Patch all agents with our test agent
    monkeypatch.setattr("app.agents.agent_orchestrator.BehaviorChangeAgent", TestAgent)
    monkeypatch.setattr("app.agents.agent_orchestrator.CatalystAgent", TestAgent)
    monkeypatch.setattr("app.agents.agent_orchestrator.HabitTrackerAgent", TestAgent)
    monkeypatch.setattr("app.agents.agent_orchestrator.JournalingAgent", TestAgent)
    monkeypatch.setattr("app.agents.agent_orchestrator.ReflectionAgent", TestAgent)
    monkeypatch.setattr("app.agents.agent_orchestrator.SelfCompassionAgent", TestAgent)
    monkeypatch.setattr("app.agents.agent_orchestrator.LifeReflectionSynthesizer", TestAgent)
    monkeypatch.setattr("app.agents.agent_orchestrator.CheckInAgent", TestAgent)
    monkeypatch.setattr("app.agents.agent_orchestrator.EmotionalForecastingAgent", TestAgent)

    # Test journal entries with various emotional states and content
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
        },
        {
            "date": "2025-02-06",
            "content": "Had a great breakthrough! Finally solved that complex problem I was stuck on.",
            "emotion": "excited"
        }
    ]
    
    # Create test data dictionary
    test_data = {
        "journal_entries": test_entries,
        "habits": [{"action": "analyze", "habit_data": {}}],  # Minimal valid habit data
        "well_being_metrics": {"mood": 7}
    }
    
    # Initialize orchestrator with test data
    orchestrator = AgentOrchestrator(journal_data=test_data)
    insights = orchestrator.run()
    
    # Verify structure of insights
    assert "agent_insights" in insights, "Missing agent_insights in response"
    assert "holistic_synthesis" in insights, "Missing holistic_synthesis in response"
    assert "timestamp" in insights, "Missing timestamp in response"
    
    # Verify each agent produced meaningful output
    agent_insights = insights["agent_insights"]
    
    # Check that all expected insights are present
    expected_keys = {
        'behavior_insights',
        'catalyst_insights',
        'compassion_guidance',
        'emotional_forecasts',
        'habit_insights',
        'well_being_insights',
        'journal_analysis',
        'reflection_insights',
        'life_narrative'
    }
    
    assert set(agent_insights.keys()) == expected_keys, f"Missing or extra insights. Found: {agent_insights.keys()}"
    
    # Verify each insight has the expected structure
    for key, insight in agent_insights.items():
        assert isinstance(insight, dict), f"{key} should return a dictionary"
        assert "analysis" in insight, f"{key} missing analysis"
        assert "recommendations" in insight, f"{key} missing recommendations"
        assert isinstance(insight["recommendations"], list), f"{key} recommendations should be a list"
        assert "confidence" in insight, f"{key} missing confidence score"
        assert isinstance(insight["confidence"], float), f"{key} confidence should be a float"



def test_agent_communication(monkeypatch):
    # Create a dummy agent class
    class DummyAgent:
        def __init__(self, **kwargs):
            pass

        def run(self):
            return {"dummy": True}

    # Monkey-patch each agent class with our dummy agent
    from app.agents.behavior_change_agent import BehaviorChangeAgent
    monkeypatch.setattr("app.agents.agent_orchestrator.BehaviorChangeAgent", DummyAgent)

    from app.agents.catalyst_agent import CatalystAgent
    monkeypatch.setattr("app.agents.agent_orchestrator.CatalystAgent", DummyAgent)

    from app.agents.habit_tracker_agent import HabitTrackerAgent
    monkeypatch.setattr("app.agents.agent_orchestrator.HabitTrackerAgent", DummyAgent)

    from app.agents.journaling_agent import JournalingAgent
    monkeypatch.setattr("app.agents.agent_orchestrator.JournalingAgent", DummyAgent)

    from app.agents.reflection_agent import ReflectionAgent
    monkeypatch.setattr("app.agents.agent_orchestrator.ReflectionAgent", DummyAgent)

    from app.agents.self_compassion_agent import SelfCompassionAgent
    monkeypatch.setattr("app.agents.agent_orchestrator.SelfCompassionAgent", DummyAgent)

    from app.agents.life_reflection_synthesizer import LifeReflectionSynthesizer
    monkeypatch.setattr("app.agents.agent_orchestrator.LifeReflectionSynthesizer", DummyAgent)

    from app.agents.checkin_agent import CheckInAgent
    monkeypatch.setattr("app.agents.agent_orchestrator.CheckInAgent", DummyAgent)

    # Also patch the EmotionalForecastingAgent which is imported in the orchestrator
    monkeypatch.setattr("app.agents.agent_orchestrator.EmotionalForecastingAgent", DummyAgent)

    # Create dummy journal_data simulating minimal input
    dummy_data = {
        "journal_entries": [{"date": "2025-02-08", "content": "Test entry."}],
        "habits": [{"action": "analyze", "habit_data": {}}],
        "well_being_metrics": {"mood": 5}
    }

    # Initialize the orchestrator with dummy data
    orchestrator = AgentOrchestrator(journal_data=dummy_data)
    insights = orchestrator.run()

    # Verify that the insights returned is a dictionary
    assert isinstance(insights, dict), "Insights should be a dictionary"

    # The orchestrator returns a nested dictionary with each agent's results
    expected_keys = {
        'behavior_insights',
        'catalyst_insights',
        'compassion_guidance',
        'emotional_forecasts',
        'habit_insights',
        'well_being_insights',
        'journal_analysis',
        'reflection_insights',
        'life_narrative'
    }

    # Verify all expected agent results are present
    assert set(insights['agent_insights'].keys()) == expected_keys, f"Missing expected agent results. Found: {insights['agent_insights'].keys()}"

    # Verify each agent returned the dummy output
    for agent_key, agent_result in insights['agent_insights'].items():
        assert agent_result == {"dummy": True}, f"Agent {agent_key} did not return the expected dummy output"
