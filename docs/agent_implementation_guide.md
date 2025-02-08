# Mind Mirror Agent Implementation Guide

## Quick Start

### Setting Up a New Agent

1. **Basic Structure**
```python
from typing import Dict, List, Any
from pydantic import Field
from .base_agent import BaseAgent

class NewAgent(BaseAgent):
    """Agent description"""
    
    journal_data: Dict = Field(
        ..., 
        description="Data description"
    )
    
    def run(self) -> Dict[str, Any]:
        """Main execution method"""
        pass
```

2. **Required Methods**
- `run()`: Main entry point
- Analysis methods (e.g., `_analyze_data()`)
- Processing methods (e.g., `_generate_insights()`)

## Integration with AgentOrchestrator

### Adding a New Agent

1. Import the agent in `agent_orchestrator.py`:
```python
from .new_agent import NewAgent
```

2. Add to `_run_agents()`:
```python
new_agent = NewAgent(journal_entries=self.journal_entries)
insights["new_agent"] = new_agent.run()
```

## Common Patterns

### Data Processing
```python
def _process_journal_entries(self, entries: List[Dict]) -> str:
    return "\n".join([
        f"Date: {entry.get('date', 'Unknown')}\n"
        f"Content: {entry.get('content', '')}"
        for entry in entries
    ])
```

### Model Interaction
```python
def _get_model_response(self, prompt: str) -> Dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        response = client.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "developer", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            reasoning_effort="high"
        )
        return response.choices[0].message.content
    except Exception as e:
        return {"error": str(e)}
```

## Error Handling

### Template
```python
try:
    # Agent logic
    result = self._process_data()
    return {
        "timestamp": datetime.now().isoformat(),
        "result": result
    }
except Exception as e:
    return {
        "error": f"Error in {self.__class__.__name__}: {str(e)}",
        "timestamp": datetime.now().isoformat()
    }
```

## Testing

### Test Categories

1. **Unit Tests**
   - Test individual agent functionality
   - Mock dependencies and external services
   - Focus on specific methods and edge cases

2. **Integration Tests** (`@pytest.mark.integration`)
   - Test agent communication through orchestrator
   - Verify data flow between components
   - Ensure correct insight aggregation

### Running Tests

```bash
# Run all tests
pytest

# Run only integration tests
pytest -m integration

# Skip integration tests
pytest -m "not integration"

# Run with verbose output
pytest -v
```

### Test Templates

1. **Unit Test**
```python
def test_agent():
    test_data = {
        "date": "2025-02-08",
        "content": "Test entry"
    }
    agent = NewAgent(journal_entries=[test_data])
    result = agent.run()
    assert "error" not in result
    assert "timestamp" in result
```

2. **Integration Test**
```python
@pytest.mark.integration
def test_agent_communication(monkeypatch):
    # Mock agent responses
    class TestAgent:
        def run(self):
            return {
                "analysis": "Test analysis",
                "recommendations": ["Test recommendation"]
            }
            
    # Patch agents
    monkeypatch.setattr("app.agents.NewAgent", TestAgent)
    
    # Run orchestrator
    orchestrator = AgentOrchestrator(journal_data=test_data)
    insights = orchestrator.run()
    
    # Verify results
    assert "agent_insights" in insights
    assert "new_agent_insights" in insights["agent_insights"]
```

## Performance Optimization

### Caching
```python
from functools import lru_cache

class OptimizedAgent(BaseAgent):
    @lru_cache(maxsize=128)
    def _cached_analysis(self, data_key: str) -> Dict:
        # Analysis logic
        pass
```

### Batch Processing
```python
def _batch_process(self, entries: List[Dict], batch_size: int = 10) -> List[Dict]:
    results = []
    for i in range(0, len(entries), batch_size):
        batch = entries[i:i + batch_size]
        results.extend(self._process_batch(batch))
    return results
```

## Debugging

### Logging Template
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DebuggableAgent(BaseAgent):
    def run(self) -> Dict[str, Any]:
        logger.info(f"Starting {self.__class__.__name__}")
        try:
            result = self._process_data()
            logger.info(f"Completed processing: {len(result)} insights")
            return result
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {str(e)}")
            raise
```

## Best Practices

### Code Organization
1. Keep analysis methods private
2. Use descriptive variable names
3. Document complex logic
4. Include type hints

### Performance
1. Batch process when possible
2. Cache expensive operations
3. Use async where appropriate
4. Implement timeouts

### Maintainability
1. Follow PEP 8
2. Write unit tests
3. Document public methods
4. Use meaningful commit messages

## Common Issues

### Troubleshooting
1. Check API key environment variable
2. Verify input data format
3. Monitor response timeouts
4. Check error logs

### Solutions
1. Implement retry logic
2. Add data validation
3. Use timeout decorators
4. Implement fallback options

## Security

### Best Practices
1. Use environment variables
2. Validate input data
3. Sanitize outputs
4. Log securely

## Deployment

### Checklist
1. Environment variables set
2. Dependencies installed
3. Tests passing
4. Documentation updated
5. Error handling verified

## Support

### Resources
1. OpenAI documentation
2. FastAPI documentation
3. Python type hints guide
4. Testing frameworks
