"""
Unit tests for EDITH-QA Planner agent.

Tests the task planning functionality using GPT-4.
"""

import pytest
from unittest.mock import patch, Mock

from edith_core.planner import plan_task


class TestPlanner:
    """Test cases for Planner agent."""
    
    def test_plan_task_basic(self, sample_goals, mock_openai_api):
        """Test basic task planning functionality."""
        goal = sample_goals[0]  # "Enable Airplane Mode from Settings"
        
        # Act
        steps = plan_task(goal)
        
        # Assert
        assert isinstance(steps, list)
        assert len(steps) > 0
        assert all(isinstance(step, str) for step in steps)
        
        # Verify steps are numbered
        for i, step in enumerate(steps, 1):
            assert str(i) in step or step.startswith(f"{i}.")
    
    def test_plan_task_with_different_goals(self, sample_goals, mock_openai_api):
        """Test planning with different types of goals."""
        for goal in sample_goals:
            steps = plan_task(goal)
            
            assert isinstance(steps, list)
            assert len(steps) > 0
            
            # Each step should be a string
            for step in steps:
                assert isinstance(step, str)
                assert len(step.strip()) > 0
    
    def test_plan_task_step_structure(self, sample_goals, mock_openai_api):
        """Test that planned steps have proper structure."""
        goal = sample_goals[0]
        steps = plan_task(goal)
        
        # Verify step structure
        for step in steps:
            # Should not be empty
            assert len(step.strip()) > 0
            
            # Should contain actionable content
            action_words = ['open', 'tap', 'click', 'navigate', 'find', 'enable', 'disable', 'set', 'configure']
            assert any(word in step.lower() for word in action_words)
    
    def test_plan_task_completeness(self, sample_goals, mock_openai_api):
        """Test that planned steps cover the complete task."""
        goal = sample_goals[0]  # "Enable Airplane Mode from Settings"
        steps = plan_task(goal)
        
        # Should include key actions
        step_text = ' '.join(steps).lower()
        
        # Should mention settings
        assert 'settings' in step_text
        
        # Should mention airplane mode
        assert 'airplane' in step_text or 'airplane mode' in step_text
        
        # Should include verification step
        verification_words = ['verify', 'check', 'confirm', 'ensure']
        assert any(word in step_text for word in verification_words)
    
    def test_plan_task_api_integration(self, sample_goals):
        """Test integration with OpenAI API."""
        goal = sample_goals[0]
        
        with patch('openai.ChatCompletion.create') as mock_api:
            # Mock API response
            mock_response = {
                'choices': [{
                    'message': {
                        'content': '1. Open Settings app\n2. Navigate to Network settings\n3. Enable Airplane Mode\n4. Verify status'
                    }
                }]
            }
            mock_api.return_value = mock_response
            
            steps = plan_task(goal)
            
            # Verify API was called correctly
            mock_api.assert_called_once()
            call_args = mock_api.call_args
            
            # Check that the prompt contains the goal
            prompt = call_args[1]['messages'][0]['content']
            assert goal in prompt
            
            # Verify response parsing
            assert len(steps) == 4
            assert 'Open Settings app' in steps[0]
            assert 'Enable Airplane Mode' in steps[2]
    
    def test_plan_task_error_handling(self, sample_goals):
        """Test error handling in planning."""
        goal = sample_goals[0]
        
        with patch('openai.ChatCompletion.create') as mock_api:
            # Mock API error
            mock_api.side_effect = Exception("API Error")
            
            # Should handle error gracefully
            with pytest.raises(Exception):
                plan_task(goal)
    
    def test_plan_task_empty_response(self, sample_goals):
        """Test handling of empty API response."""
        goal = sample_goals[0]
        
        with patch('openai.ChatCompletion.create') as mock_api:
            # Mock empty response
            mock_response = {
                'choices': [{
                    'message': {
                        'content': ''
                    }
                }]
            }
            mock_api.return_value = mock_response
            
            steps = plan_task(goal)
            
            # Should handle empty response
            assert isinstance(steps, list)
            # Empty response should result in empty list or single empty string
            assert len(steps) == 0 or (len(steps) == 1 and steps[0] == '')
    
    def test_plan_task_malformed_response(self, sample_goals):
        """Test handling of malformed API response."""
        goal = sample_goals[0]
        
        with patch('openai.ChatCompletion.create') as mock_api:
            # Mock malformed response
            mock_response = {
                'choices': [{
                    'message': {
                        'content': 'This is not a numbered list\nJust some text\nWithout proper formatting'
                    }
                }]
            }
            mock_api.return_value = mock_response
            
            steps = plan_task(goal)
            
            # Should still return a list
            assert isinstance(steps, list)
            # Should split on newlines
            assert len(steps) >= 3
    
    def test_plan_task_step_numbering(self, sample_goals, mock_openai_api):
        """Test that steps are properly numbered."""
        goal = sample_goals[0]
        steps = plan_task(goal)
        
        # Check numbering patterns
        for i, step in enumerate(steps, 1):
            # Should start with number or contain number
            step_lower = step.lower().strip()
            assert (step_lower.startswith(f"{i}.") or 
                   step_lower.startswith(f"{i} ") or
                   f"{i}." in step or
                   f"{i} " in step)
    
    def test_plan_task_complex_goal(self, mock_openai_api):
        """Test planning with complex, multi-part goals."""
        complex_goal = "Set up a new Wi-Fi connection with custom network name 'MyNetwork' and password 'password123', then test the connection"
        
        steps = plan_task(complex_goal)
        
        assert isinstance(steps, list)
        assert len(steps) > 3  # Should have multiple steps for complex goal
        
        # Should include network setup steps
        step_text = ' '.join(steps).lower()
        assert 'wifi' in step_text or 'wi-fi' in step_text
        assert 'network' in step_text
        assert 'password' in step_text or 'pass' in step_text
    
    def test_plan_task_verification_steps(self, sample_goals, mock_openai_api):
        """Test that plans include verification steps."""
        goal = sample_goals[0]
        steps = plan_task(goal)
        
        # Should include verification
        step_text = ' '.join(steps).lower()
        verification_words = ['verify', 'check', 'confirm', 'ensure', 'test']
        assert any(word in step_text for word in verification_words)
    
    def test_plan_task_step_length(self, sample_goals, mock_openai_api):
        """Test that steps are appropriately detailed."""
        goal = sample_goals[0]
        steps = plan_task(goal)
        
        for step in steps:
            # Steps should be detailed enough to be actionable
            assert len(step.strip()) > 10  # Minimum length for actionable step
            
            # But not too verbose
            assert len(step.strip()) < 200  # Maximum reasonable length
    
    def test_plan_task_consistency(self, sample_goals, mock_openai_api):
        """Test consistency of planning results."""
        goal = sample_goals[0]
        
        # Run planning multiple times
        results = []
        for _ in range(3):
            steps = plan_task(goal)
            results.append(steps)
        
        # All results should be valid
        for steps in results:
            assert isinstance(steps, list)
            assert len(steps) > 0
        
        # Results should be similar (same general structure)
        step_counts = [len(steps) for steps in results]
        assert all(count > 0 for count in step_counts)
        
        # Step counts should be within reasonable range
        min_steps = min(step_counts)
        max_steps = max(step_counts)
        assert max_steps - min_steps <= 3  # Allow some variation
    
    def test_plan_task_with_empty_goal(self, mock_openai_api):
        """Test planning with empty goal."""
        goal = ""
        
        steps = plan_task(goal)
        
        # Should handle empty goal
        assert isinstance(steps, list)
        # May return empty list or minimal steps
        assert len(steps) >= 0
    
    def test_plan_task_with_special_characters(self, mock_openai_api):
        """Test planning with special characters in goal."""
        goal = "Enable Airplane Mode & turn off Wi-Fi (test connection)"
        
        steps = plan_task(goal)
        
        assert isinstance(steps, list)
        assert len(steps) > 0
        
        # Should handle special characters gracefully
        step_text = ' '.join(steps)
        assert 'airplane' in step_text.lower()
        assert 'wifi' in step_text.lower() or 'wi-fi' in step_text.lower()
