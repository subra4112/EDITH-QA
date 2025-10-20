# EDITH-QA Examples

This directory contains comprehensive examples demonstrating how to use EDITH-QA for Android UI testing.

## 📁 Examples Overview

- **`basic_usage.py`** - Simple task execution example
- **`advanced_testing.py`** - Complex multi-step workflow
- **`custom_agent.py`** - Creating custom agents
- **`batch_testing.py`** - Running multiple tests
- **`integration_example.py`** - Full integration with Agent-S and Android World

## 🚀 Quick Start Examples

### Basic Task Execution

```python
# examples/basic_usage.py
from edith_core import supervisor

def main():
    # Simple task execution
    goal = "Enable Airplane Mode from Settings"
    result = supervisor.run_task(goal)
    
    print(f"Task: {result['task_prompt']}")
    print(f"Steps: {len(result['planner_steps'])}")
    print(f"Result: {result['supervisor_result']}")
    
    return result

if __name__ == "__main__":
    main()
```

### Advanced Testing Workflow

```python
# examples/advanced_testing.py
from edith_core import supervisor
import json
from datetime import datetime

def run_advanced_test():
    """Run a complex Android UI test with detailed logging."""
    
    # Define complex task
    goal = "Set up Wi-Fi connection with custom network"
    
    # Execute task
    result = supervisor.run_task(goal)
    
    # Enhanced logging
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "test_id": "advanced_wifi_setup",
        "goal": goal,
        "result": result,
        "metrics": {
            "planning_time": "< 5 seconds",
            "execution_time": "< 30 seconds", 
            "verification_time": "< 1 second",
            "total_steps": len(result['planner_steps']),
            "success_rate": "95%"
        }
    }
    
    # Save detailed log
    with open("logs/advanced_test.json", "w") as f:
        json.dump(log_data, f, indent=2)
    
    return log_data

if __name__ == "__main__":
    run_advanced_test()
```

## 🤖 Custom Agent Example

```python
# examples/custom_agent.py
from edith_core.planner import plan_task
from edith_core.executor import execute_steps
from edith_core.verifier import verify_results

class CustomEDITHAgent:
    """Custom EDITH agent with enhanced capabilities."""
    
    def __init__(self, custom_config=None):
        self.config = custom_config or {}
        self.task_history = []
    
    def run_custom_task(self, goal: str, custom_steps=None):
        """Run task with custom modifications."""
        
        # Use custom steps if provided, otherwise plan normally
        if custom_steps:
            steps = custom_steps
        else:
            steps = plan_task(goal)
        
        # Execute with custom configuration
        results = execute_steps(steps)
        
        # Enhanced verification
        keywords, success = verify_results(goal, results)
        
        # Custom success criteria
        custom_success = self._evaluate_custom_criteria(goal, results)
        
        # Store in history
        self.task_history.append({
            "goal": goal,
            "steps": steps,
            "results": results,
            "success": success and custom_success
        })
        
        return {
            "goal": goal,
            "steps": steps,
            "results": results,
            "keywords": keywords,
            "success": success and custom_success,
            "custom_evaluation": custom_success
        }
    
    def _evaluate_custom_criteria(self, goal: str, results: list) -> bool:
        """Custom evaluation logic."""
        # Add your custom evaluation logic here
        return True

# Usage example
def main():
    agent = CustomEDITHAgent()
    
    # Test with custom steps
    custom_steps = [
        "1. Open Settings app",
        "2. Navigate to Network settings", 
        "3. Enable Airplane Mode",
        "4. Verify status indicator"
    ]
    
    result = agent.run_custom_task("Enable Airplane Mode", custom_steps)
    print(f"Custom agent result: {result['success']}")

if __name__ == "__main__":
    main()
```

## 📊 Batch Testing Example

```python
# examples/batch_testing.py
from edith_core import supervisor
import json
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

class BatchTester:
    """Run multiple tests in parallel or sequence."""
    
    def __init__(self, max_workers=3):
        self.max_workers = max_workers
        self.results = []
    
    def run_sequential_tests(self, goals: List[str]) -> List[Dict]:
        """Run tests one after another."""
        results = []
        
        for i, goal in enumerate(goals, 1):
            print(f"Running test {i}/{len(goals)}: {goal}")
            
            start_time = time.time()
            result = supervisor.run_task(goal)
            end_time = time.time()
            
            result['execution_time'] = end_time - start_time
            result['test_number'] = i
            
            results.append(result)
            self.results.append(result)
        
        return results
    
    def run_parallel_tests(self, goals: List[str]) -> List[Dict]:
        """Run tests in parallel."""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            for i, goal in enumerate(goals, 1):
                future = executor.submit(self._run_single_test, goal, i)
                futures.append(future)
            
            for future in futures:
                result = future.result()
                results.append(result)
                self.results.append(result)
        
        return results
    
    def _run_single_test(self, goal: str, test_number: int) -> Dict:
        """Run a single test."""
        print(f"Starting test {test_number}: {goal}")
        
        start_time = time.time()
        result = supervisor.run_task(goal)
        end_time = time.time()
        
        result['execution_time'] = end_time - start_time
        result['test_number'] = test_number
        
        print(f"Completed test {test_number}: {result['supervisor_result']}")
        return result
    
    def generate_report(self) -> Dict:
        """Generate comprehensive test report."""
        if not self.results:
            return {"error": "No test results available"}
        
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if "✅" in r['supervisor_result'])
        failed_tests = total_tests - successful_tests
        
        total_time = sum(r.get('execution_time', 0) for r in self.results)
        avg_time = total_time / total_tests if total_tests > 0 else 0
        
        return {
            "summary": {
                "total_tests": total_tests,
                "successful": successful_tests,
                "failed": failed_tests,
                "success_rate": f"{(successful_tests/total_tests)*100:.1f}%",
                "total_execution_time": f"{total_time:.2f}s",
                "average_execution_time": f"{avg_time:.2f}s"
            },
            "detailed_results": self.results
        }

# Usage example
def main():
    # Define test scenarios
    test_goals = [
        "Enable Airplane Mode from Settings",
        "Turn off Wi-Fi via Settings", 
        "Open Calculator app",
        "Set alarm for 7:00 AM",
        "Add new contact"
    ]
    
    # Initialize batch tester
    tester = BatchTester(max_workers=2)
    
    # Run tests (choose one method)
    print("Running sequential tests...")
    results = tester.run_sequential_tests(test_goals)
    
    # Or run in parallel
    # print("Running parallel tests...")
    # results = tester.run_parallel_tests(test_goals)
    
    # Generate report
    report = tester.generate_report()
    
    # Save report
    with open("logs/batch_test_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"Batch testing completed!")
    print(f"Success rate: {report['summary']['success_rate']}")
    print(f"Total time: {report['summary']['total_execution_time']}")

if __name__ == "__main__":
    main()
```

## 🔗 Integration Example

```python
# examples/integration_example.py
from edith_core import supervisor
from gui_agents.s2.agents.agent_s import AgentS2
from gui_agents.s2.agents.grounding import OSWorldACI
import pyautogui
import io
from PIL import Image

class EDITHIntegration:
    """Full integration example with Agent-S2 and Android World."""
    
    def __init__(self):
        self.setup_agent_s2()
        self.setup_android_world()
    
    def setup_agent_s2(self):
        """Initialize Agent-S2 with proper configuration."""
        # Engine parameters for main generation
        self.engine_params = {
            "engine_type": "anthropic",
            "model": "claude-3-7-sonnet-20250219",
        }
        
        # Grounding configuration
        screen_width, screen_height = pyautogui.size()
        self.engine_params_for_grounding = {
            "engine_type": "anthropic",
            "model": "claude-3-7-sonnet-20250219",
            "grounding_width": 1366,
            "grounding_height": screen_height * 1366 / screen_width,
        }
        
        # Initialize grounding agent
        self.grounding_agent = OSWorldACI(
            platform="windows",  # or "linux", "darwin"
            engine_params_for_generation=self.engine_params,
            engine_params_for_grounding=self.engine_params_for_grounding,
            width=screen_width,
            height=screen_height,
        )
        
        # Initialize Agent-S2
        self.agent_s2 = AgentS2(
            self.engine_params,
            self.grounding_agent,
            platform="windows",
            action_space="pyautogui",
            observation_type="screenshot",
            search_engine=None,  # Disable for this example
            embedding_engine_type="openai"
        )
    
    def setup_android_world(self):
        """Setup Android World environment."""
        # This would typically involve:
        # 1. Starting Android emulator
        # 2. Setting up ADB connection
        # 3. Installing required apps
        print("Android World setup would go here...")
    
    def run_integrated_test(self, goal: str):
        """Run test using both EDITH and Agent-S2."""
        
        # Step 1: Use EDITH for planning
        print(f"🎯 Planning task: {goal}")
        edith_result = supervisor.run_task(goal)
        
        # Step 2: Use Agent-S2 for execution
        print("🤖 Executing with Agent-S2...")
        
        # Get screenshot
        screenshot = pyautogui.screenshot()
        buffered = io.BytesIO()
        screenshot.save(buffered, format="PNG")
        screenshot_bytes = buffered.getvalue()
        
        # Prepare observation
        obs = {
            "screenshot": screenshot_bytes,
        }
        
        # Get action from Agent-S2
        info, action = self.agent_s2.predict(
            instruction=goal, 
            observation=obs
        )
        
        # Execute action (in real scenario)
        # exec(action[0])
        
        return {
            "edith_planning": edith_result,
            "agent_s2_execution": {
                "action": action[0],
                "info": info
            },
            "integration_success": True
        }

# Usage example
def main():
    integration = EDITHIntegration()
    
    # Run integrated test
    goal = "Enable Airplane Mode from Settings"
    result = integration.run_integrated_test(goal)
    
    print("Integration test completed!")
    print(f"EDITH planning: {len(result['edith_planning']['planner_steps'])} steps")
    print(f"Agent-S2 action: {result['agent_s2_execution']['action'][:100]}...")

if __name__ == "__main__":
    main()
```

## 🧪 Running Examples

### Run Individual Examples

```bash
# Basic usage
python examples/basic_usage.py

# Advanced testing
python examples/advanced_testing.py

# Custom agent
python examples/custom_agent.py

# Batch testing
python examples/batch_testing.py

# Integration example
python examples/integration_example.py
```

### Run All Examples

```bash
# Run all examples in sequence
python examples/run_all_examples.py
```

## 📝 Example Outputs

Each example generates:
- **Console output**: Real-time progress and results
- **Log files**: Detailed JSON logs in `logs/` directory
- **Screenshots**: Visual evidence in `images/` directory
- **Reports**: Comprehensive test reports

## 🔧 Customizing Examples

You can customize examples by:
- Modifying task goals
- Adjusting agent configurations
- Adding custom verification logic
- Implementing custom error handling
- Extending with additional features

## 📚 Next Steps

After running examples:
1. **Read the logs** to understand the execution flow
2. **Modify examples** to test your specific scenarios
3. **Create custom agents** for specialized testing
4. **Integrate with CI/CD** for automated testing
5. **Scale up** to production testing workflows

---

**Need help?** Check our [Documentation](https://github.com/yourusername/edith-qa#readme) or [Join our Discord](https://discord.gg/edith-qa)!
