# EDITH-QA Test Suite

This directory contains comprehensive tests for EDITH-QA.

## 📁 Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_supervisor.py   # Supervisor agent tests
│   ├── test_planner.py      # Planner agent tests
│   ├── test_executor.py     # Executor agent tests
│   └── test_verifier.py     # Verifier agent tests
├── integration/             # Integration tests
│   ├── test_workflow.py     # End-to-end workflow tests
│   ├── test_agent_s.py      # Agent-S integration tests
│   └── test_android_world.py # Android World integration tests
├── performance/             # Performance tests
│   ├── test_benchmarks.py   # Performance benchmarks
│   └── test_load.py         # Load testing
├── fixtures/                # Test data and fixtures
│   ├── sample_goals.json    # Sample task goals
│   ├── mock_responses.json  # Mock API responses
│   └── test_images/         # Test screenshots
└── conftest.py              # Pytest configuration
```

## 🧪 Running Tests

### Run All Tests
```bash
python -m pytest tests/ -v
```

### Run Specific Test Categories
```bash
# Unit tests only
python -m pytest tests/unit/ -v

# Integration tests only
python -m pytest tests/integration/ -v

# Performance tests only
python -m pytest tests/performance/ -v
```

### Run with Coverage
```bash
python -m pytest tests/ --cov=edith_core --cov-report=html --cov-report=term
```

### Run Specific Tests
```bash
# Run specific test file
python -m pytest tests/unit/test_supervisor.py -v

# Run specific test function
python -m pytest tests/unit/test_supervisor.py::test_run_task_success -v

# Run tests matching pattern
python -m pytest tests/ -k "test_supervisor" -v
```

## 📊 Test Coverage

Current test coverage targets:
- **Overall**: 80%+
- **Core modules**: 90%+
- **Critical paths**: 95%+

## 🔧 Test Configuration

Tests use pytest with the following configuration:

```python
# conftest.py
import pytest
import os
import tempfile
from unittest.mock import Mock, patch

@pytest.fixture
def mock_openai_api():
    """Mock OpenAI API responses."""
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value = {
            'choices': [{'message': {'content': 'Mocked response'}}]
        }
        yield mock

@pytest.fixture
def temp_log_dir():
    """Create temporary directory for test logs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def sample_goal():
    """Sample task goal for testing."""
    return "Enable Airplane Mode from Settings"
```

## 🎯 Test Categories

### Unit Tests
Test individual components in isolation:
- Agent functionality
- Data processing
- Utility functions
- Configuration handling

### Integration Tests
Test component interactions:
- Agent communication
- End-to-end workflows
- External service integration
- Data flow validation

### Performance Tests
Test system performance:
- Execution time benchmarks
- Memory usage monitoring
- Load testing
- Scalability validation

## 📝 Writing Tests

### Test Naming Convention
```python
def test_component_functionality_scenario():
    """Test description."""
    pass
```

### Example Test Structure
```python
import pytest
from edith_core.supervisor import run_task

class TestSupervisor:
    """Test cases for Supervisor agent."""
    
    def test_run_task_success(self, sample_goal, mock_openai_api):
        """Test successful task execution."""
        # Arrange
        expected_steps = 5
        
        # Act
        result = run_task(sample_goal)
        
        # Assert
        assert result is not None
        assert 'task_prompt' in result
        assert 'planner_steps' in result
        assert len(result['planner_steps']) >= expected_steps
        assert 'supervisor_result' in result
    
    def test_run_task_with_invalid_goal(self):
        """Test task execution with invalid goal."""
        # Arrange
        invalid_goal = ""
        
        # Act & Assert
        with pytest.raises(ValueError):
            run_task(invalid_goal)
    
    @pytest.mark.parametrize("goal,expected_keywords", [
        ("Enable Airplane Mode", ["enable", "airplane", "mode"]),
        ("Turn off Wi-Fi", ["turn", "off", "wi-fi"]),
        ("Open Calculator", ["open", "calculator"]),
    ])
    def test_goal_keyword_extraction(self, goal, expected_keywords):
        """Test keyword extraction from goals."""
        # This would test the verifier's keyword extraction
        pass
```

## 🚀 Continuous Integration

Tests run automatically on:
- Every pull request
- Every push to main branch
- Scheduled nightly runs

### CI Test Matrix
- Python versions: 3.9, 3.10, 3.11, 3.12
- Operating systems: Ubuntu, Windows, macOS
- Test types: Unit, Integration, Performance

## 📈 Test Metrics

Track these metrics:
- **Test Coverage**: Percentage of code covered
- **Test Execution Time**: How long tests take to run
- **Test Reliability**: Flaky test detection
- **Test Maintenance**: Time spent updating tests

## 🔍 Debugging Tests

### Verbose Output
```bash
python -m pytest tests/ -v -s
```

### Debug Mode
```bash
python -m pytest tests/ --pdb
```

### Test Discovery
```bash
python -m pytest --collect-only tests/
```

## 📚 Test Documentation

Each test should include:
- Clear docstring explaining purpose
- Arrange-Act-Assert structure
- Meaningful assertions
- Edge case coverage
- Performance considerations

## 🤝 Contributing Tests

When adding new features:
1. Write unit tests for new functions
2. Add integration tests for workflows
3. Update existing tests if needed
4. Ensure test coverage doesn't decrease
5. Document any new test fixtures

## 🐛 Test Issues

Common test issues and solutions:

### Flaky Tests
- Use proper mocking
- Avoid timing dependencies
- Use deterministic test data

### Slow Tests
- Mock external dependencies
- Use smaller test datasets
- Parallel test execution

### Test Maintenance
- Keep tests simple
- Use descriptive names
- Regular test review
