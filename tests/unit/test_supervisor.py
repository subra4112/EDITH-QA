"""
Unit tests for EDITH-QA Supervisor agent.

Tests the core orchestration functionality of the Supervisor agent.
"""

import pytest
import json
import os
from unittest.mock import patch, Mock
from datetime import datetime

from edith_core.supervisor import run_task


class TestSupervisor:
    """Test cases for Supervisor agent."""
    
    def test_run_task_success(self, sample_goals, mock_openai_api, sample_complete_result):
        """Test successful task execution."""
        # Arrange
        goal = sample_goals[0]  # "Enable Airplane Mode from Settings"
        
        # Act
        result = run_task(goal)
        
        # Assert
        assert result is not None
        assert isinstance(result, dict)
        assert 'task_prompt' in result
        assert 'planner_steps' in result
        assert 'executor_results' in result
        assert 'verifier_keywords' in result
        assert 'supervisor_result' in result
        
        # Verify content
        assert result['task_prompt'] == goal
        assert isinstance(result['planner_steps'], list)
        assert len(result['planner_steps']) > 0
        assert isinstance(result['executor_results'], list)
        assert len(result['executor_results']) > 0
        assert isinstance(result['verifier_keywords'], list)
        assert len(result['verifier_keywords']) > 0
        assert isinstance(result['supervisor_result'], str)
    
    def test_run_task_with_different_goals(self, sample_goals, mock_openai_api):
        """Test task execution with different goals."""
        for goal in sample_goals:
            # Act
            result = run_task(goal)
            
            # Assert
            assert result is not None
            assert result['task_prompt'] == goal
            assert len(result['planner_steps']) > 0
            assert len(result['executor_results']) > 0
    
    def test_run_task_planning_phase(self, sample_goals, mock_openai_api):
        """Test the planning phase of task execution."""
        goal = sample_goals[0]
        
        with patch('edith_core.planner.plan_task') as mock_plan:
            mock_plan.return_value = [
                "1. Open Settings",
                "2. Navigate to Network",
                "3. Enable Airplane Mode"
            ]
            
            result = run_task(goal)
            
            # Verify planning was called
            mock_plan.assert_called_once_with(goal)
            assert len(result['planner_steps']) == 3
    
    def test_run_task_execution_phase(self, sample_goals, mock_openai_api):
        """Test the execution phase of task execution."""
        goal = sample_goals[0]
        
        with patch('edith_core.executor.execute_steps') as mock_exec:
            mock_exec.return_value = [
                "Step 1 — SUCCESS",
                "Step 2 — SUCCESS",
                "Step 3 — SUCCESS"
            ]
            
            result = run_task(goal)
            
            # Verify execution was called
            mock_exec.assert_called_once()
            assert len(result['executor_results']) == 3
    
    def test_run_task_verification_phase(self, sample_goals, mock_openai_api):
        """Test the verification phase of task execution."""
        goal = sample_goals[0]
        
        with patch('edith_core.verifier.verify_results') as mock_verify:
            mock_verify.return_value = (["enable", "airplane", "mode"], True)
            
            result = run_task(goal)
            
            # Verify verification was called
            mock_verify.assert_called_once()
            assert result['verifier_keywords'] == ["enable", "airplane", "mode"]
    
    def test_run_task_success_result(self, sample_goals, mock_openai_api):
        """Test successful task result formatting."""
        goal = sample_goals[0]
        
        with patch('edith_core.verifier.verify_results') as mock_verify:
            mock_verify.return_value = (["enable", "airplane", "mode"], True)
            
            result = run_task(goal)
            
            assert "✅" in result['supervisor_result']
            assert "successfully" in result['supervisor_result'].lower()
    
    def test_run_task_failure_result(self, sample_goals, mock_openai_api):
        """Test failed task result formatting."""
        goal = sample_goals[0]
        
        with patch('edith_core.verifier.verify_results') as mock_verify:
            mock_verify.return_value = (["enable"], False)
            
            result = run_task(goal)
            
            assert "❌" in result['supervisor_result']
            assert "failed" in result['supervisor_result'].lower()
    
    def test_run_task_error_handling(self, mock_openai_api):
        """Test error handling in task execution."""
        goal = "Invalid goal"
        
        with patch('edith_core.planner.plan_task') as mock_plan:
            mock_plan.side_effect = Exception("Planning failed")
            
            # Should not raise exception, but handle gracefully
            result = run_task(goal)
            
            # Should still return a result structure
            assert result is not None
            assert 'task_prompt' in result
    
    def test_run_task_logging(self, sample_goals, mock_openai_api, temp_log_dir):
        """Test that task execution creates proper logs."""
        goal = sample_goals[0]
        
        # Mock the logging to capture output
        with patch('builtins.print') as mock_print:
            result = run_task(goal)
            
            # Verify logging occurred
            assert mock_print.called
            print_calls = [call[0][0] for call in mock_print.call_args_list]
            
            # Check for key log messages
            log_messages = ' '.join(print_calls)
            assert "Supervisor" in log_messages
            assert "New Task" in log_messages
    
    def test_run_task_data_structure(self, sample_goals, mock_openai_api):
        """Test that returned data has correct structure."""
        goal = sample_goals[0]
        result = run_task(goal)
        
        # Verify all required keys exist
        required_keys = [
            'task_prompt',
            'planner_steps', 
            'executor_results',
            'verifier_keywords',
            'supervisor_result'
        ]
        
        for key in required_keys:
            assert key in result, f"Missing required key: {key}"
        
        # Verify data types
        assert isinstance(result['task_prompt'], str)
        assert isinstance(result['planner_steps'], list)
        assert isinstance(result['executor_results'], list)
        assert isinstance(result['verifier_keywords'], list)
        assert isinstance(result['supervisor_result'], str)
    
    def test_run_task_performance(self, sample_goals, mock_openai_api, performance_benchmark):
        """Test task execution performance."""
        goal = sample_goals[0]
        
        import time
        start_time = time.time()
        
        result = run_task(goal)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify execution time is within acceptable limits
        assert execution_time < performance_benchmark['max_execution_time']
        
        # Verify result is still valid
        assert result is not None
        assert 'supervisor_result' in result
    
    @pytest.mark.parametrize("goal,expected_keywords", [
        ("Enable Airplane Mode", ["enable", "airplane", "mode"]),
        ("Turn off Wi-Fi", ["turn", "off", "wi-fi"]),
        ("Open Calculator", ["open", "calculator"]),
        ("Set alarm for 7:00 AM", ["set", "alarm", "7:00", "am"]),
    ])
    def test_keyword_extraction(self, goal, expected_keywords, mock_openai_api):
        """Test keyword extraction from different goals."""
        result = run_task(goal)
        
        # Verify keywords are extracted
        assert 'verifier_keywords' in result
        assert isinstance(result['verifier_keywords'], list)
        assert len(result['verifier_keywords']) > 0
        
        # Check that some expected keywords are present
        extracted_keywords = [kw.lower() for kw in result['verifier_keywords']]
        for expected_kw in expected_keywords:
            # At least one word from expected should be in extracted
            assert any(expected_kw.lower() in kw for kw in extracted_keywords)
    
    def test_run_task_with_empty_goal(self, mock_openai_api):
        """Test task execution with empty goal."""
        goal = ""
        
        # Should handle empty goal gracefully
        result = run_task(goal)
        
        assert result is not None
        assert result['task_prompt'] == goal
    
    def test_run_task_with_very_long_goal(self, mock_openai_api):
        """Test task execution with very long goal."""
        goal = "This is a very long goal that contains many words and should test the system's ability to handle complex and lengthy task descriptions that might be provided by users who are very verbose in their explanations of what they want the system to do"
        
        result = run_task(goal)
        
        assert result is not None
        assert result['task_prompt'] == goal
        assert len(result['planner_steps']) > 0
