# supervisor.py

from edith_core.planner import plan_task
from edith_core.executor import execute_steps
from edith_core.verifier import verify_results


def run_task(goal: str):
    print(f"\n🎯 [Supervisor] New Task: {goal}")

    # Step 1: Plan
    steps = plan_task(goal)
    print("\n[Planner Output]")
    for idx, step in enumerate(steps, 1):
        print(f"{idx}. {step}")

    # Step 2: Execute
    results = execute_steps(steps)
    print("\n[Executor] Execution complete.\n")

    # Step 3: Verify
    matched_keywords, success = verify_results(goal, results)

    # Step 4: Final decision
    if success:
        supervisor_result = "✅ [Supervisor] Task completed successfully!"
    else:
        supervisor_result = "❌ [Supervisor] Task failed. Manual review required."

    print(f"\n{supervisor_result}\n")

    # Return all data for logging
    return {
        "task_prompt": goal,
        "planner_steps": steps,
        "executor_results": results,
        "verifier_keywords": matched_keywords,
        "supervisor_result": supervisor_result
    }
