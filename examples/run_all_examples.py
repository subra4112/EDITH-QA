#!/usr/bin/env python3
"""
EDITH-QA Run All Examples

This script runs all available examples in sequence to demonstrate
the full capabilities of EDITH-QA.
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from typing import List, Dict

def run_example(script_path: str, description: str) -> Dict:
    """Run a single example script and capture results."""
    
    print(f"\n🚀 Running: {description}")
    print(f"📁 Script: {script_path}")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        # Run the script
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        return {
            "script": script_path,
            "description": description,
            "success": result.returncode == 0,
            "duration": duration,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {
            "script": script_path,
            "description": description,
            "success": False,
            "duration": 300,
            "stdout": "",
            "stderr": "Script timed out after 5 minutes",
            "returncode": -1
        }
    except Exception as e:
        return {
            "script": script_path,
            "description": description,
            "success": False,
            "duration": 0,
            "stdout": "",
            "stderr": str(e),
            "returncode": -1
        }

def display_results(results: List[Dict]):
    """Display comprehensive results from all examples."""
    
    print("\n" + "=" * 80)
    print("📊 EDITH-QA EXAMPLES SUMMARY")
    print("=" * 80)
    
    total_examples = len(results)
    successful_examples = sum(1 for r in results if r['success'])
    failed_examples = total_examples - successful_examples
    total_duration = sum(r['duration'] for r in results)
    
    print(f"📈 Overall Statistics:")
    print(f"  Total Examples: {total_examples}")
    print(f"  Successful: {successful_examples}")
    print(f"  Failed: {failed_examples}")
    print(f"  Success Rate: {(successful_examples/total_examples)*100:.1f}%")
    print(f"  Total Duration: {total_duration:.2f}s")
    print(f"  Average Duration: {total_duration/total_examples:.2f}s")
    
    print(f"\n📋 Detailed Results:")
    print("-" * 80)
    
    for i, result in enumerate(results, 1):
        status = "✅ SUCCESS" if result['success'] else "❌ FAILED"
        print(f"{i:2d}. {result['description']}")
        print(f"    Status: {status}")
        print(f"    Duration: {result['duration']:.2f}s")
        print(f"    Script: {result['script']}")
        
        if not result['success'] and result['stderr']:
            print(f"    Error: {result['stderr'][:100]}...")
        
        print()
    
    # Show failed examples details
    failed_results = [r for r in results if not r['success']]
    if failed_results:
        print("❌ Failed Examples Details:")
        print("-" * 40)
        
        for result in failed_results:
            print(f"\n🔍 {result['description']}")
            print(f"   Script: {result['script']}")
            print(f"   Return Code: {result['returncode']}")
            if result['stderr']:
                print(f"   Error: {result['stderr']}")
            if result['stdout']:
                print(f"   Output: {result['stdout'][:200]}...")

def main():
    """Run all EDITH-QA examples."""
    
    print("🤖 EDITH-QA - Running All Examples")
    print("=" * 80)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Define examples to run
    examples = [
        {
            "script": "examples/basic_usage.py",
            "description": "Basic Usage - Simple task execution"
        },
        {
            "script": "examples/advanced_testing.py", 
            "description": "Advanced Testing - Complex workflows and analysis"
        }
    ]
    
    # Check if example files exist
    existing_examples = []
    for example in examples:
        if os.path.exists(example['script']):
            existing_examples.append(example)
        else:
            print(f"⚠️  Warning: {example['script']} not found, skipping...")
    
    if not existing_examples:
        print("❌ No example scripts found!")
        return
    
    print(f"📁 Found {len(existing_examples)} example(s) to run")
    
    # Run all examples
    results = []
    for example in existing_examples:
        result = run_example(example['script'], example['description'])
        results.append(result)
        
        # Brief pause between examples
        time.sleep(1)
    
    # Display results
    display_results(results)
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"logs/examples_summary_{timestamp}.json"
    
    os.makedirs("logs", exist_ok=True)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total_examples": len(results),
        "successful_examples": sum(1 for r in results if r['success']),
        "failed_examples": sum(1 for r in results if not r['success']),
        "total_duration": sum(r['duration'] for r in results),
        "results": results
    }
    
    import json
    with open(results_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📁 Results saved to: {results_file}")
    
    # Final status
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    if successful == total:
        print(f"\n🎉 All examples completed successfully!")
        print(f"✨ EDITH-QA is working perfectly!")
    else:
        print(f"\n⚠️  {total - successful} example(s) failed.")
        print(f"🔧 Please check the error messages above.")
    
    print(f"\n⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # Set up environment
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Examples will run in mock mode.")
    
    # Run all examples
    main()
