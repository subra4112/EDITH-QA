# EDITH-QA API Documentation

## Overview

EDITH-QA provides a comprehensive API for intelligent Android UI testing through its multi-agent system. This documentation covers all available functions, classes, and methods.

## 🎯 Core API

### Supervisor Agent

The main entry point for task execution.

#### `run_task(goal: str) -> dict`

Executes a complete Android UI task using the multi-agent system.

**Parameters:**
- `goal` (str): Natural language description of the task to perform

**Returns:**
- `dict`: Complete task execution result with the following structure:
  ```python
  {
      "task_prompt": str,           # Original task goal
      "planner_steps": List[str],   # Generated step-by-step plan
      "executor_results": List[str], # Execution results for each step
      "verifier_keywords": List[str], # Keywords matched during verification
      "supervisor_result": str      # Final success/failure message
  }
  ```

**Example:**
```python
from edith_core import supervisor

result = supervisor.run_task("Enable Airplane Mode from Settings")
print(f"Task completed: {result['supervisor_result']}")
```

**Raises:**
- `ValueError`: If goal is empty or invalid
- `Exception`: If task execution fails

---

## 📋 Planner Agent

Converts high-level goals into actionable step-by-step plans.

### `plan_task(user_goal: str) -> List[str]`

Generates a step-by-step plan for the given goal using GPT-4.

**Parameters:**
- `user_goal` (str): High-level task description

**Returns:**
- `List[str]`: List of numbered, actionable steps

**Example:**
```python
from edith_core.planner import plan_task

steps = plan_task("Enable Airplane Mode from Settings")
for i, step in enumerate(steps, 1):
    print(f"{i}. {step}")
```

**Configuration:**
- Model: GPT-4
- Temperature: 0.2 (for consistent planning)
- Max tokens: 1000

---

## ⚡ Executor Agent

Executes planned steps with visual feedback and error handling.

### `execute_steps(step_list: List[str]) -> List[str]`

Executes a list of planned steps and returns execution results.

**Parameters:**
- `step_list` (List[str]): List of steps to execute

**Returns:**
- `List[str]`: Execution results for each step

**Example:**
```python
from edith_core.executor import execute_steps

steps = [
    "1. Open Settings app",
    "2. Navigate to Network settings",
    "3. Enable Airplane Mode"
]

results = execute_steps(steps)
for result in results:
    print(result)
```

**Features:**
- Mock execution with screenshot generation
- Step-by-step visual feedback
- Error handling and retry logic
- Performance timing

---

## ✅ Verifier Agent

Validates task completion using intelligent keyword matching.

### `verify_results(goal: str, executor_results: List[str]) -> Tuple[List[str], bool]`

Verifies task completion by matching keywords from the goal with execution results.

**Parameters:**
- `goal` (str): Original task goal
- `executor_results` (List[str]): Results from step execution

**Returns:**
- `Tuple[List[str], bool]`: (matched_keywords, success_status)

**Example:**
```python
from edith_core.verifier import verify_results

goal = "Enable Airplane Mode"
results = [
    "Step 1: SUCCESS",
    "Step 2: SUCCESS", 
    "Step 3: SUCCESS - Airplane Mode Enabled"
]

keywords, success = verify_results(goal, results)
print(f"Matched keywords: {keywords}")
print(f"Success: {success}")
```

**Success Criteria:**
- Minimum 3 keyword matches required
- Case-insensitive matching
- Fuzzy matching support

---

## 🤖 Agent-S Integration

Advanced computer vision and UI interaction capabilities.

### AgentS2 Class

Main agent class for Agent-S2 integration.

```python
from gui_agents.s2.agents.agent_s import AgentS2
from gui_agents.s2.agents.grounding import OSWorldACI

# Initialize Agent-S2
agent = AgentS2(
    engine_params={
        "engine_type": "anthropic",
        "model": "claude-3-7-sonnet-20250219"
    },
    grounding_agent=OSWorldACI(...),
    platform="windows",
    action_space="pyautogui",
    observation_type="screenshot"
)
```

#### `predict(instruction: str, observation: dict) -> Tuple[dict, List[str]]`

Generates actions based on instruction and current observation.

**Parameters:**
- `instruction` (str): Task instruction
- `observation` (dict): Current state observation

**Returns:**
- `Tuple[dict, List[str]]`: (info, actions)

---

## 📱 Android World Integration

Comprehensive Android testing environment.

### Task Execution

```python
from android_world.run import main as run_android_world

# Run Android World tasks
run_android_world([
    "--suite_family=android_world",
    "--agent_name=t3a_gpt4",
    "--tasks=ContactsAddContact,ClockStopWatchRunning"
])
```

### Available Tasks

- **Settings Tasks**: Airplane mode, Wi-Fi, Bluetooth
- **App Tasks**: Calculator, Contacts, Clock
- **System Tasks**: File management, notifications
- **Custom Tasks**: User-defined scenarios

---

## 🔧 Configuration API

### Configuration Management

```python
import toml

# Load configuration
with open('config/config.toml', 'r') as f:
    config = toml.load(f)

# Access configuration
planner_config = config['agents']['planner']
executor_config = config['agents']['executor']
```

### Environment Variables

```python
import os

# Required API keys
openai_key = os.getenv('OPENAI_API_KEY')
anthropic_key = os.getenv('ANTHROPIC_API_KEY')

# Optional configuration
log_level = os.getenv('LOG_LEVEL', 'INFO')
max_execution_time = int(os.getenv('MAX_EXECUTION_TIME', '300'))
```

---

## 📊 Logging and Monitoring

### Logging Configuration

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/edith.log'),
        logging.StreamHandler()
    ]
)
```

### Performance Monitoring

```python
import time
from edith_core import supervisor

# Monitor execution time
start_time = time.time()
result = supervisor.run_task("Enable Airplane Mode")
end_time = time.time()

execution_time = end_time - start_time
print(f"Task completed in {execution_time:.2f} seconds")
```

---

## 🚀 Advanced Usage

### Custom Agent Implementation

```python
from edith_core.planner import plan_task
from edith_core.executor import execute_steps
from edith_core.verifier import verify_results

class CustomEDITHAgent:
    def __init__(self, custom_config=None):
        self.config = custom_config or {}
    
    def run_custom_task(self, goal: str, custom_steps=None):
        # Use custom steps or plan normally
        steps = custom_steps or plan_task(goal)
        
        # Execute with custom configuration
        results = execute_steps(steps)
        
        # Enhanced verification
        keywords, success = verify_results(goal, results)
        
        return {
            "goal": goal,
            "steps": steps,
            "results": results,
            "success": success
        }
```

### Batch Processing

```python
from concurrent.futures import ThreadPoolExecutor

def run_batch_tasks(goals: List[str], max_workers: int = 3):
    """Run multiple tasks in parallel."""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(supervisor.run_task, goal) for goal in goals]
        results = [future.result() for future in futures]
    
    return results
```

---

## 🔒 Security and Safety

### API Key Management

```python
# Secure API key handling
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Never hardcode API keys
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment")
```

### Execution Safety

```python
# Mock execution for safety
os.environ['EDITH_MOCK_MODE'] = 'true'

# Permission dialogs for real actions
def safe_execute(action: str):
    if os.getenv('EDITH_MOCK_MODE') == 'true':
        print(f"Mock execution: {action}")
    else:
        # Show permission dialog
        if confirm_execution(action):
            exec(action)
```

---

## 📈 Performance Optimization

### Caching

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def cached_plan_task(goal: str) -> List[str]:
    """Cache planning results for repeated goals."""
    return plan_task(goal)
```

### Async Execution

```python
import asyncio

async def async_run_task(goal: str):
    """Run task asynchronously."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, supervisor.run_task, goal)
```

---

## 🐛 Error Handling

### Exception Handling

```python
from edith_core import supervisor

try:
    result = supervisor.run_task("Enable Airplane Mode")
except ValueError as e:
    print(f"Invalid goal: {e}")
except Exception as e:
    print(f"Task execution failed: {e}")
    # Log error for debugging
    logging.error(f"Task execution error: {e}", exc_info=True)
```

### Retry Logic

```python
import time
from functools import wraps

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry_on_failure(max_retries=3)
def robust_run_task(goal: str):
    return supervisor.run_task(goal)
```

---

## 📚 Examples

### Complete Workflow Example

```python
from edith_core import supervisor
import json
from datetime import datetime

def run_complete_test(goal: str):
    """Run a complete test with logging and analysis."""
    
    # Execute task
    result = supervisor.run_task(goal)
    
    # Enhanced logging
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "goal": goal,
        "result": result,
        "metrics": {
            "steps_count": len(result['planner_steps']),
            "success": "✅" in result['supervisor_result'],
            "keywords_matched": len(result['verifier_keywords'])
        }
    }
    
    # Save log
    with open(f"logs/test_{int(datetime.now().timestamp())}.json", "w") as f:
        json.dump(log_data, f, indent=2)
    
    return log_data

# Usage
result = run_complete_test("Enable Airplane Mode from Settings")
print(f"Test completed: {result['metrics']['success']}")
```

---

## 🔗 Integration Examples

### FastAPI Integration

```python
from fastapi import FastAPI
from pydantic import BaseModel
from edith_core import supervisor

app = FastAPI()

class TaskRequest(BaseModel):
    goal: str

@app.post("/execute-task")
async def execute_task(request: TaskRequest):
    result = supervisor.run_task(request.goal)
    return result
```

### CLI Integration

```python
import click
from edith_core import supervisor

@click.command()
@click.argument('goal')
def run_task_cli(goal):
    """Run EDITH-QA task from command line."""
    result = supervisor.run_task(goal)
    click.echo(f"Result: {result['supervisor_result']}")

if __name__ == '__main__':
    run_task_cli()
```

---

This API documentation provides comprehensive coverage of EDITH-QA's capabilities. For more examples and advanced usage patterns, see the `examples/` directory in the repository.
