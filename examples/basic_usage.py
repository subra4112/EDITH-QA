#!/usr/bin/env python3
"""
EDITH-QA Basic Usage Example

This example demonstrates the core functionality of EDITH-QA:
- Task planning with GPT-4
- Step-by-step execution
- Result verification
- Comprehensive logging
"""

import os
import sys
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edith_core import supervisor

def main():
    """Run a basic EDITH-QA test."""
    
    print("🤖 EDITH-QA Basic Usage Example")
    print("=" * 50)
    
    # Define the task goal
    goal = "Enable Airplane Mode from Settings"
    
    print(f"🎯 Task Goal: {goal}")
    print()
    
    # Run the task using EDITH's supervisor
    print("🚀 Starting task execution...")
    start_time = datetime.now()
    
    try:
        result = supervisor.run_task(goal)
        end_time = datetime.now()
        execution_time = (end_time - start_time).total_seconds()
        
        print("\n📊 Task Execution Results:")
        print("-" * 30)
        
        # Display results
        print(f"✅ Task: {result['task_prompt']}")
        print(f"📋 Planned Steps: {len(result['planner_steps'])}")
        print(f"⚡ Executed Steps: {len(result['executor_results'])}")
        print(f"🔍 Verified Keywords: {result['verifier_keywords']}")
        print(f"🎯 Final Result: {result['supervisor_result']}")
        print(f"⏱️ Execution Time: {execution_time:.2f} seconds")
        
        # Show planned steps
        print("\n📝 Planned Steps:")
        for i, step in enumerate(result['planner_steps'], 1):
            print(f"  {i}. {step}")
        
        # Show execution results
        print("\n⚡ Execution Results:")
        for i, result_step in enumerate(result['executor_results'], 1):
            print(f"  {i}. {result_step}")
        
        # Success analysis
        success = "✅" in result['supervisor_result']
        print(f"\n🎉 Task {'SUCCESSFUL' if success else 'FAILED'}")
        
        if success:
            print("✨ EDITH-QA successfully completed the Android UI task!")
        else:
            print("❌ Task failed. Check logs for details.")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during task execution: {str(e)}")
        return None

if __name__ == "__main__":
    # Set up environment (you should set these in your actual environment)
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Using mock mode.")
    
    # Run the example
    result = main()
    
    if result:
        print("\n🎯 Example completed successfully!")
        print("📁 Check the 'logs/' directory for detailed logs")
        print("🖼️  Check the 'images/' directory for screenshots")
    else:
        print("\n❌ Example failed. Please check your setup.")
        sys.exit(1)
