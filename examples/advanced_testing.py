#!/usr/bin/env python3
"""
EDITH-QA Advanced Testing Example

This example demonstrates advanced features:
- Complex multi-step workflows
- Detailed logging and metrics
- Error handling and recovery
- Performance monitoring
"""

import os
import sys
import json
import time
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from edith_core import supervisor

class AdvancedTester:
    """Advanced testing framework with enhanced capabilities."""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.test_history = []
        self.performance_metrics = {}
    
    def run_complex_test(self, goal: str, test_id: str = None) -> Dict:
        """Run a complex test with detailed monitoring."""
        
        test_id = test_id or f"test_{int(time.time())}"
        
        print(f"🚀 Starting Advanced Test: {test_id}")
        print(f"🎯 Goal: {goal}")
        print("=" * 60)
        
        # Initialize test data
        test_data = {
            "test_id": test_id,
            "goal": goal,
            "start_time": datetime.now().isoformat(),
            "phases": {}
        }
        
        try:
            # Phase 1: Planning
            print("📋 Phase 1: Task Planning...")
            planning_start = time.time()
            
            result = supervisor.run_task(goal)
            
            planning_time = time.time() - planning_start
            test_data["phases"]["planning"] = {
                "duration": planning_time,
                "steps_count": len(result['planner_steps']),
                "status": "completed"
            }
            
            print(f"✅ Planning completed in {planning_time:.2f}s")
            print(f"📝 Generated {len(result['planner_steps'])} steps")
            
            # Phase 2: Analysis
            print("\n🔍 Phase 2: Result Analysis...")
            analysis_start = time.time()
            
            analysis = self._analyze_results(result)
            analysis_time = time.time() - analysis_start
            
            test_data["phases"]["analysis"] = {
                "duration": analysis_time,
                "analysis": analysis,
                "status": "completed"
            }
            
            print(f"✅ Analysis completed in {analysis_time:.2f}s")
            
            # Phase 3: Performance Evaluation
            print("\n📊 Phase 3: Performance Evaluation...")
            perf_start = time.time()
            
            performance = self._evaluate_performance(result, planning_time, analysis_time)
            perf_time = time.time() - perf_start
            
            test_data["phases"]["performance"] = {
                "duration": perf_time,
                "metrics": performance,
                "status": "completed"
            }
            
            print(f"✅ Performance evaluation completed in {perf_time:.2f}s")
            
            # Complete test data
            test_data.update({
                "end_time": datetime.now().isoformat(),
                "total_duration": time.time() - planning_start,
                "result": result,
                "success": "✅" in result['supervisor_result'],
                "grade": self._calculate_grade(result, performance)
            })
            
            # Store in history
            self.test_history.append(test_data)
            
            # Display results
            self._display_results(test_data)
            
            return test_data
            
        except Exception as e:
            test_data.update({
                "end_time": datetime.now().isoformat(),
                "error": str(e),
                "success": False,
                "status": "failed"
            })
            
            print(f"❌ Test failed with error: {str(e)}")
            return test_data
    
    def _analyze_results(self, result: Dict) -> Dict:
        """Analyze test results for insights."""
        
        analysis = {
            "planning_quality": self._evaluate_planning_quality(result['planner_steps']),
            "execution_efficiency": self._evaluate_execution_efficiency(result['executor_results']),
            "verification_accuracy": self._evaluate_verification_accuracy(result),
            "overall_coherence": self._evaluate_overall_coherence(result)
        }
        
        return analysis
    
    def _evaluate_planning_quality(self, steps: List[str]) -> Dict:
        """Evaluate the quality of task planning."""
        
        return {
            "step_count": len(steps),
            "step_length_avg": sum(len(step) for step in steps) / len(steps) if steps else 0,
            "has_verification": any("verify" in step.lower() for step in steps),
            "has_error_handling": any("error" in step.lower() or "fail" in step.lower() for step in steps),
            "complexity_score": min(len(steps) / 5, 1.0)  # Normalized complexity
        }
    
    def _evaluate_execution_efficiency(self, results: List[str]) -> Dict:
        """Evaluate execution efficiency."""
        
        success_count = sum(1 for result in results if "SUCCESS" in result)
        
        return {
            "total_steps": len(results),
            "successful_steps": success_count,
            "success_rate": success_count / len(results) if results else 0,
            "efficiency_score": success_count / len(results) if results else 0
        }
    
    def _evaluate_verification_accuracy(self, result: Dict) -> Dict:
        """Evaluate verification accuracy."""
        
        keywords = result.get('verifier_keywords', [])
        goal_words = result.get('task_prompt', '').lower().split()
        
        return {
            "matched_keywords": len(keywords),
            "total_goal_words": len(goal_words),
            "match_rate": len(keywords) / len(goal_words) if goal_words else 0,
            "verification_score": min(len(keywords) / 3, 1.0)  # Normalized score
        }
    
    def _evaluate_overall_coherence(self, result: Dict) -> Dict:
        """Evaluate overall coherence of the test."""
        
        steps = result.get('planner_steps', [])
        execution = result.get('executor_results', [])
        
        return {
            "step_execution_alignment": len(steps) == len(execution),
            "coherence_score": 1.0 if len(steps) == len(execution) else 0.8,
            "completeness": len(execution) / len(steps) if steps else 0
        }
    
    def _evaluate_performance(self, result: Dict, planning_time: float, analysis_time: float) -> Dict:
        """Evaluate overall performance metrics."""
        
        total_time = planning_time + analysis_time
        
        return {
            "planning_time": planning_time,
            "analysis_time": analysis_time,
            "total_time": total_time,
            "steps_per_second": len(result.get('planner_steps', [])) / total_time if total_time > 0 else 0,
            "performance_score": self._calculate_performance_score(total_time, len(result.get('planner_steps', [])))
        }
    
    def _calculate_performance_score(self, total_time: float, step_count: int) -> float:
        """Calculate performance score based on time and complexity."""
        
        # Ideal: 1 step per second, with bonus for more steps
        ideal_time = step_count * 1.0
        time_score = max(0, 1.0 - (total_time - ideal_time) / ideal_time) if ideal_time > 0 else 0
        
        # Complexity bonus
        complexity_bonus = min(step_count / 10, 0.2)
        
        return min(time_score + complexity_bonus, 1.0)
    
    def _calculate_grade(self, result: Dict, performance: Dict) -> str:
        """Calculate overall grade for the test."""
        
        success = "✅" in result['supervisor_result']
        perf_score = performance.get('performance_score', 0)
        
        if success and perf_score >= 0.9:
            return "A+"
        elif success and perf_score >= 0.8:
            return "A"
        elif success and perf_score >= 0.7:
            return "B+"
        elif success and perf_score >= 0.6:
            return "B"
        elif success:
            return "C"
        else:
            return "F"
    
    def _display_results(self, test_data: Dict):
        """Display comprehensive test results."""
        
        print("\n" + "=" * 60)
        print("📊 ADVANCED TEST RESULTS")
        print("=" * 60)
        
        # Basic info
        print(f"🆔 Test ID: {test_data['test_id']}")
        print(f"🎯 Goal: {test_data['goal']}")
        print(f"⏱️  Total Duration: {test_data['total_duration']:.2f}s")
        print(f"🎓 Grade: {test_data['grade']}")
        print(f"✅ Success: {'Yes' if test_data['success'] else 'No'}")
        
        # Phase breakdown
        print(f"\n📋 Phase Breakdown:")
        for phase, data in test_data['phases'].items():
            print(f"  {phase.title()}: {data['duration']:.2f}s")
        
        # Analysis results
        analysis = test_data['phases']['analysis']['analysis']
        print(f"\n🔍 Analysis Results:")
        print(f"  Planning Quality: {analysis['planning_quality']['complexity_score']:.2f}")
        print(f"  Execution Efficiency: {analysis['execution_efficiency']['efficiency_score']:.2f}")
        print(f"  Verification Accuracy: {analysis['verification_accuracy']['verification_score']:.2f}")
        print(f"  Overall Coherence: {analysis['overall_coherence']['coherence_score']:.2f}")
        
        # Performance metrics
        perf = test_data['phases']['performance']['metrics']
        print(f"\n📈 Performance Metrics:")
        print(f"  Performance Score: {perf['performance_score']:.2f}")
        print(f"  Steps per Second: {perf['steps_per_second']:.2f}")
        
        print("\n" + "=" * 60)
    
    def save_report(self, filename: str = None):
        """Save comprehensive test report."""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/advanced_test_report_{timestamp}.json"
        
        os.makedirs("logs", exist_ok=True)
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_tests": len(self.test_history),
            "test_history": self.test_history,
            "summary": self._generate_summary()
        }
        
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        
        print(f"📁 Report saved to: {filename}")
        return filename
    
    def _generate_summary(self) -> Dict:
        """Generate summary statistics."""
        
        if not self.test_history:
            return {}
        
        successful_tests = sum(1 for test in self.test_history if test.get('success', False))
        total_tests = len(self.test_history)
        
        grades = [test.get('grade', 'F') for test in self.test_history]
        grade_counts = {grade: grades.count(grade) for grade in set(grades)}
        
        return {
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "success_rate": successful_tests / total_tests if total_tests > 0 else 0,
            "grade_distribution": grade_counts,
            "average_duration": sum(test.get('total_duration', 0) for test in self.test_history) / total_tests
        }

def main():
    """Run advanced testing examples."""
    
    print("🚀 EDITH-QA Advanced Testing Example")
    print("=" * 60)
    
    # Initialize advanced tester
    tester = AdvancedTester()
    
    # Define complex test scenarios
    test_scenarios = [
        {
            "goal": "Enable Airplane Mode from Settings",
            "test_id": "airplane_mode_advanced"
        },
        {
            "goal": "Set up Wi-Fi connection with custom network",
            "test_id": "wifi_setup_advanced"
        },
        {
            "goal": "Configure notification settings for all apps",
            "test_id": "notifications_advanced"
        }
    ]
    
    # Run tests
    for scenario in test_scenarios:
        print(f"\n🧪 Running Test: {scenario['test_id']}")
        result = tester.run_complex_test(scenario['goal'], scenario['test_id'])
        
        if result.get('success'):
            print(f"✅ Test {scenario['test_id']} completed successfully!")
        else:
            print(f"❌ Test {scenario['test_id']} failed!")
        
        print("-" * 60)
    
    # Generate comprehensive report
    print("\n📊 Generating comprehensive report...")
    report_file = tester.save_report()
    
    print(f"\n🎉 Advanced testing completed!")
    print(f"📁 Detailed report saved to: {report_file}")
    print(f"📈 Total tests run: {len(tester.test_history)}")
    
    # Display summary
    summary = tester._generate_summary()
    if summary:
        print(f"\n📊 Summary:")
        print(f"  Success Rate: {summary['success_rate']:.1%}")
        print(f"  Average Duration: {summary['average_duration']:.2f}s")
        print(f"  Grade Distribution: {summary['grade_distribution']}")

if __name__ == "__main__":
    # Set up environment
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set. Using mock mode.")
    
    # Run advanced testing
    main()
