# 🤝 Contributing to EDITH-QA

Thank you for your interest in contributing to EDITH-QA! We welcome contributions from the community and are excited to work with you to improve this intelligent Android testing framework.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Community Guidelines](#community-guidelines)

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please read and follow our Code of Conduct:

- **Be respectful**: Treat everyone with respect and kindness
- **Be inclusive**: Welcome newcomers and help them learn
- **Be constructive**: Provide helpful feedback and suggestions
- **Be patient**: Remember that everyone is learning and growing

### Unacceptable Behavior

- Harassment, discrimination, or offensive comments
- Personal attacks or trolling
- Spam or off-topic discussions
- Sharing private information without permission

## 🚀 Getting Started

### 1. Fork the Repository

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/yourusername/edith-qa.git
cd edith-qa

# Add upstream remote
git remote add upstream https://github.com/originalusername/edith-qa.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv edith-dev
source edith-dev/bin/activate  # On Windows: edith-dev\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### 3. Create a Branch

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Or bugfix branch
git checkout -b bugfix/issue-number-description
```

## 🛠️ Development Setup

### Required Tools

- **Python 3.9+**: Core development language
- **Git**: Version control
- **Docker**: For testing (optional)
- **Android Studio**: For Android testing
- **VS Code/PyCharm**: Recommended IDEs

### Development Dependencies

```bash
# Install all development dependencies
pip install -r requirements-dev.txt

# This includes:
# - pytest: Testing framework
# - black: Code formatting
# - flake8: Linting
# - mypy: Type checking
# - pre-commit: Git hooks
```

### IDE Configuration

#### VS Code Settings (`.vscode/settings.json`)
```json
{
    "python.defaultInterpreterPath": "./edith-dev/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"]
}
```

#### PyCharm Configuration
1. Open project in PyCharm
2. Go to Settings → Project → Python Interpreter
3. Select your virtual environment
4. Enable pytest as test runner

## 📝 Contribution Guidelines

### Types of Contributions

We welcome various types of contributions:

#### 🐛 Bug Fixes
- Fix existing issues
- Improve error handling
- Add better logging

#### ✨ New Features
- Add new test scenarios
- Implement new agents
- Enhance existing functionality

#### 📚 Documentation
- Improve README files
- Add code comments
- Create tutorials

#### 🧪 Testing
- Add unit tests
- Improve test coverage
- Add integration tests

#### 🔧 Infrastructure
- CI/CD improvements
- Docker configurations
- Performance optimizations

### Coding Standards

#### Python Style Guide
We follow PEP 8 with some modifications:

```python
# Use type hints
def plan_task(user_goal: str) -> List[str]:
    """Plan a task using GPT-4."""
    pass

# Use descriptive variable names
task_steps = plan_task(goal)
execution_results = execute_steps(task_steps)

# Use docstrings for all functions
def verify_results(goal: str, results: List[str]) -> Tuple[List[str], bool]:
    """
    Verify task completion using keyword matching.
    
    Args:
        goal: Original task goal
        results: Execution results
        
    Returns:
        Tuple of matched keywords and success status
    """
    pass
```

#### Code Formatting
```bash
# Format code with black
black edith_core/

# Check formatting
black --check edith_core/

# Sort imports
isort edith_core/
```

#### Linting
```bash
# Run flake8 linting
flake8 edith_core/

# Run mypy type checking
mypy edith_core/
```

### Testing Requirements

#### Unit Tests
```python
# tests/test_planner.py
import pytest
from edith_core.planner import plan_task

def test_plan_task_basic():
    """Test basic task planning functionality."""
    goal = "Enable Airplane Mode"
    steps = plan_task(goal)
    
    assert isinstance(steps, list)
    assert len(steps) > 0
    assert all(isinstance(step, str) for step in steps)
```

#### Integration Tests
```python
# tests/test_integration.py
import pytest
from edith_core import supervisor

def test_full_workflow():
    """Test complete workflow from goal to result."""
    goal = "Test basic functionality"
    result = supervisor.run_task(goal)
    
    assert "task_prompt" in result
    assert "planner_steps" in result
    assert "executor_results" in result
    assert "verifier_keywords" in result
    assert "supervisor_result" in result
```

#### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_planner.py

# Run with coverage
python -m pytest tests/ --cov=edith_core

# Run specific test
python -m pytest tests/test_planner.py::test_plan_task_basic
```

## 🔄 Pull Request Process

### Before Submitting

1. **Test your changes**:
   ```bash
   python -m pytest tests/
   python -m pytest tests/ --cov=edith_core
   ```

2. **Format your code**:
   ```bash
   black edith_core/
   isort edith_core/
   ```

3. **Check linting**:
   ```bash
   flake8 edith_core/
   mypy edith_core/
   ```

4. **Update documentation** if needed

5. **Add tests** for new functionality

### Pull Request Template

When creating a PR, please include:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test improvement
- [ ] Infrastructure change

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** on different environments
4. **Documentation** review
5. **Final approval** and merge

## 🐛 Issue Reporting

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Check documentation** for solutions
3. **Test with latest version**

### Issue Template

```markdown
## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- EDITH-QA Version: [e.g., 1.0.0]

## Additional Context
Any other relevant information
```

### Feature Requests

```markdown
## Feature Description
Clear description of the requested feature

## Use Case
Why is this feature needed?

## Proposed Solution
How should this feature work?

## Alternatives Considered
Other approaches you've considered

## Additional Context
Any other relevant information
```

## 🌟 Recognition

### Contributors

We recognize contributors in several ways:

- **GitHub Contributors**: Listed in repository contributors
- **Release Notes**: Mentioned in release announcements
- **Documentation**: Credited in relevant sections
- **Community**: Recognized in discussions

### Contribution Levels

- **🥉 Bronze**: 1-5 contributions
- **🥈 Silver**: 6-15 contributions  
- **🥇 Gold**: 16+ contributions
- **💎 Diamond**: Major contributions or maintainer status

## 📞 Getting Help

### Communication Channels

- **GitHub Discussions**: General questions and discussions
- **GitHub Issues**: Bug reports and feature requests
- **Discord**: Real-time community chat
- **Email**: support@edith-qa.com

### Mentorship Program

We offer mentorship for new contributors:

1. **Pair programming** sessions
2. **Code review** guidance
3. **Architecture** explanations
4. **Best practices** training

To request mentorship, open an issue with the `mentorship` label.

## 📄 License

By contributing to EDITH-QA, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You

Thank you for contributing to EDITH-QA! Your contributions help make Android testing more intelligent and accessible for developers worldwide.

---

**Questions?** Feel free to reach out to us through any of the communication channels above. We're here to help!
