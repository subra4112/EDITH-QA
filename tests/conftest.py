"""
EDITH-QA Test Configuration and Fixtures

This module provides pytest configuration and shared fixtures for all tests.
"""

import pytest
import os
import tempfile
import json
from unittest.mock import Mock, patch
from datetime import datetime
from typing import Dict, List, Any

# Test configuration
pytest_plugins = ["pytest_cov"]


@pytest.fixture(scope="session")
def test_config():
    """Test configuration settings."""
    return {
        "log_level": "DEBUG",
        "max_execution_time": 30,
        "step_delay": 0.1,
        "max_retries": 1,
        "mock_mode": True
    }


@pytest.fixture
def mock_openai_api():
    """Mock OpenAI API responses for testing."""
    mock_response = {
        'choices': [{
            'message': {
                'content': '1. Open Settings app\n2. Navigate to Network settings\n3. Enable Airplane Mode\n4. Verify status'
            }
        }]
    }
    
    with patch('openai.ChatCompletion.create') as mock:
        mock.return_value = mock_response
        yield mock


@pytest.fixture
def mock_anthropic_api():
    """Mock Anthropic API responses for testing."""
    mock_response = {
        'content': [{
            'text': 'Mocked Agent-S2 response'
        }]
    }
    
    with patch('anthropic.Anthropic.messages.create') as mock:
        mock.return_value = mock_response
        yield mock


@pytest.fixture
def temp_log_dir():
    """Create temporary directory for test logs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_image_dir():
    """Create temporary directory for test images."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_goals():
    """Sample task goals for testing."""
    return [
        "Enable Airplane Mode from Settings",
        "Turn off Wi-Fi via Settings",
        "Open Calculator app",
        "Set alarm for 7:00 AM",
        "Add new contact"
    ]


@pytest.fixture
def sample_planning_result():
    """Sample planning result for testing."""
    return {
        "task_prompt": "Enable Airplane Mode from Settings",
        "planner_steps": [
            "1. Unlock the Android device if it's locked.",
            "2. Locate and tap on the 'Apps' icon on the home screen.",
            "3. Scroll through the apps and find the 'Settings' app.",
            "4. Tap on the 'Settings' app to open it.",
            "5. Scroll down the settings menu and find the 'Network & Internet' option.",
            "6. Tap on the 'Network & Internet' option to open it.",
            "7. Find and tap on the 'Airplane Mode' option.",
            "8. Toggle the switch to the 'On' position to enable Airplane Mode.",
            "9. Verify that Airplane Mode is enabled by checking the status bar."
        ]
    }


@pytest.fixture
def sample_execution_result():
    """Sample execution result for testing."""
    return [
        "1. Unlock the Android device if it's locked. — SUCCESS",
        "2. Locate and tap on the 'Apps' icon on the home screen. — SUCCESS",
        "3. Scroll through the apps and find the 'Settings' app. — SUCCESS",
        "4. Tap on the 'Settings' app to open it. — SUCCESS",
        "5. Scroll down the settings menu and find the 'Network & Internet' option. — SUCCESS",
        "6. Tap on the 'Network & Internet' option to open it. — SUCCESS",
        "7. Find and tap on the 'Airplane Mode' option. — SUCCESS",
        "8. Toggle the switch to the 'On' position to enable Airplane Mode. — SUCCESS",
        "9. Verify that Airplane Mode is enabled by checking the status bar. — SUCCESS"
    ]


@pytest.fixture
def sample_verification_result():
    """Sample verification result for testing."""
    return {
        "matched_keywords": ["enable", "airplane", "mode", "settings"],
        "success": True
    }


@pytest.fixture
def sample_complete_result():
    """Sample complete test result for testing."""
    return {
        "timestamp": datetime.now().isoformat(),
        "task_prompt": "Enable Airplane Mode from Settings",
        "planner_steps": [
            "1. Unlock the Android device if it's locked.",
            "2. Locate and tap on the 'Apps' icon on the home screen.",
            "3. Scroll through the apps and find the 'Settings' app.",
            "4. Tap on the 'Settings' app to open it.",
            "5. Scroll down the settings menu and find the 'Network & Internet' option.",
            "6. Tap on the 'Network & Internet' option to open it.",
            "7. Find and tap on the 'Airplane Mode' option.",
            "8. Toggle the switch to the 'On' position to enable Airplane Mode.",
            "9. Verify that Airplane Mode is enabled by checking the status bar."
        ],
        "executor_results": [
            "1. Unlock the Android device if it's locked. — SUCCESS",
            "2. Locate and tap on the 'Apps' icon on the home screen. — SUCCESS",
            "3. Scroll through the apps and find the 'Settings' app. — SUCCESS",
            "4. Tap on the 'Settings' app to open it. — SUCCESS",
            "5. Scroll down the settings menu and find the 'Network & Internet' option. — SUCCESS",
            "6. Tap on the 'Network & Internet' option to open it. — SUCCESS",
            "7. Find and tap on the 'Airplane Mode' option. — SUCCESS",
            "8. Toggle the switch to the 'On' position to enable Airplane Mode. — SUCCESS",
            "9. Verify that Airplane Mode is enabled by checking the status bar. — SUCCESS"
        ],
        "verifier_keywords": ["enable", "airplane", "mode", "settings"],
        "supervisor_result": "✅ [Supervisor] Task completed successfully!"
    }


@pytest.fixture
def mock_screenshot():
    """Mock screenshot data for testing."""
    # Create a simple mock image data
    import numpy as np
    from PIL import Image
    
    # Create a simple test image
    img_array = np.ones((100, 100, 3), dtype=np.uint8) * 128  # Gray image
    img = Image.fromarray(img_array)
    
    # Convert to bytes
    import io
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return buffered.getvalue()


@pytest.fixture
def mock_android_env():
    """Mock Android environment for testing."""
    mock_env = Mock()
    mock_env.reset.return_value = None
    mock_env.step.return_value = {
        'observation': {'screenshot': b'mock_screenshot_data'},
        'reward': 1.0,
        'done': True
    }
    return mock_env


@pytest.fixture
def mock_agent_s2():
    """Mock Agent-S2 for testing."""
    mock_agent = Mock()
    mock_agent.predict.return_value = (
        {'reflection': 'Mock reflection', 'executor_plan': 'Mock plan'},
        ['pyautogui.click(100, 200)']
    )
    mock_agent.reset.return_value = None
    return mock_agent


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment before each test."""
    # Set test environment variables
    os.environ['EDITH_TEST_MODE'] = 'true'
    os.environ['LOG_LEVEL'] = 'DEBUG'
    
    # Create test directories
    os.makedirs('test_logs', exist_ok=True)
    os.makedirs('test_images', exist_ok=True)
    
    yield
    
    # Cleanup after test
    import shutil
    if os.path.exists('test_logs'):
        shutil.rmtree('test_logs')
    if os.path.exists('test_images'):
        shutil.rmtree('test_images')


@pytest.fixture
def performance_benchmark():
    """Performance benchmark data for testing."""
    return {
        "max_execution_time": 30.0,
        "max_planning_time": 5.0,
        "max_verification_time": 1.0,
        "min_success_rate": 0.8
    }


# Test markers
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "performance: marks tests as performance tests"
    )


# Test collection hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on test file location
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        
        # Add slow marker for tests that take longer
        if "slow" in item.name or "benchmark" in item.name:
            item.add_marker(pytest.mark.slow)
