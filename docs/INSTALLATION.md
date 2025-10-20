# 🚀 Installation & Setup Guide

## Prerequisites

Before installing EDITH-QA, ensure you have the following prerequisites:

### System Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Ubuntu 18.04+
- **Python**: 3.9, 3.10, 3.11, or 3.12
- **RAM**: Minimum 8GB, Recommended 16GB+
- **Storage**: At least 5GB free space
- **Network**: Stable internet connection for API calls

### Required Software
- **Android Studio**: For Android emulator
- **Docker**: For containerized environments (optional)
- **Git**: For version control

## 🔑 API Keys Setup

EDITH-QA requires API keys for AI services. Get your keys from:

### 1. OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create account or sign in
3. Navigate to API Keys section
4. Create new secret key
5. Copy the key (starts with `sk-`)

### 2. Anthropic API Key
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Create account or sign in
3. Navigate to API Keys section
4. Create new key
5. Copy the key (starts with `sk-ant-`)

### 3. Hugging Face Token (Optional)
1. Visit [Hugging Face](https://huggingface.co/)
2. Create account or sign in
3. Go to Settings → Access Tokens
4. Create new token
5. Copy the token

## 📦 Installation Methods

### Method 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/edith-qa.git
cd edith-qa

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
export OPENAI_API_KEY="your-openai-key-here"
export ANTHROPIC_API_KEY="your-anthropic-key-here"
export HF_TOKEN="your-huggingface-token-here"  # Optional

# Verify installation
python -c "from edith_core import supervisor; print('✅ Installation successful!')"
```

### Method 2: Development Install

```bash
# Clone the repository
git clone https://github.com/yourusername/edith-qa.git
cd edith-qa

# Create virtual environment
python -m venv edith-env
source edith-env/bin/activate  # On Windows: edith-env\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/
```

### Method 3: Docker Install

```bash
# Clone the repository
git clone https://github.com/yourusername/edith-qa.git
cd edith-qa

# Build Docker image
docker build -t edith-qa:latest .

# Run with environment variables
docker run -e OPENAI_API_KEY="your-key" \
           -e ANTHROPIC_API_KEY="your-key" \
           -v $(pwd)/logs:/app/logs \
           edith-qa:latest
```

## 🤖 Android Environment Setup

### Step 1: Install Android Studio

#### Windows
1. Download [Android Studio](https://developer.android.com/studio)
2. Run installer with default settings
3. Follow setup wizard
4. Install Android SDK

#### macOS
```bash
# Using Homebrew
brew install --cask android-studio

# Or download from official website
# https://developer.android.com/studio
```

#### Linux (Ubuntu)
```bash
# Add repository
sudo apt update
sudo apt install openjdk-11-jdk

# Download and install Android Studio
wget https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2023.1.1.28/android-studio-2023.1.1.28-linux.tar.gz
tar -xzf android-studio-2023.1.1.28-linux.tar.gz
sudo mv android-studio /opt/
```

### Step 2: Create Android Virtual Device (AVD)

1. Open Android Studio
2. Go to **Tools** → **AVD Manager**
3. Click **Create Virtual Device**
4. Select **Pixel 6** hardware
5. Choose **Tiramisu, API Level 33** system image
6. Name it **AndroidWorldAvd**
7. Click **Finish**

### Step 3: Launch Emulator

```bash
# Find emulator path
# Windows: %LOCALAPPDATA%\Android\Sdk\emulator\emulator.exe
# macOS: ~/Library/Android/sdk/emulator/emulator
# Linux: ~/Android/Sdk/emulator/emulator

# Launch with required flags
emulator -avd AndroidWorldAvd -no-snapshot -grpc 8554
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required API Keys
OPENAI_API_KEY=sk-proj-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Optional Configuration
HF_TOKEN=hf_your-huggingface-token-here
PERPLEXICA_URL=http://localhost:3000/api/search
GROUNDING_MODEL_RESIZE_WIDTH=1366

# Logging Configuration
LOG_LEVEL=INFO
LOG_DIR=logs
```

### Agent Configuration

Create `config/agent_config.yaml`:

```yaml
planner:
  model: "gpt-4"
  temperature: 0.2
  max_tokens: 1000
  
executor:
  screenshot_dir: "images"
  step_delay: 1.0
  max_retries: 3
  
verifier:
  min_keyword_matches: 3
  case_sensitive: false
  
supervisor:
  max_execution_time: 300
  enable_recovery: true
```

## 🧪 Verification & Testing

### Basic Functionality Test

```bash
# Test core functionality
python -c "
from edith_core import supervisor
result = supervisor.run_task('Test basic functionality')
print('✅ Core system working!')
print(f'Result: {result[\"supervisor_result\"]}')
"
```

### Agent-S Integration Test

```bash
# Test Agent-S integration
python -c "
from gui_agents.s2.agents.agent_s import AgentS2
print('✅ Agent-S integration working!')
"
```

### Android World Test

```bash
# Test Android World environment
cd android_world
python minimal_task_runner.py --task=ContactsAddContact
```

## 🐛 Troubleshooting

### Common Issues

#### 1. API Key Errors
```bash
# Error: OpenAI API key not found
# Solution: Set environment variable
export OPENAI_API_KEY="your-key-here"

# Error: Anthropic API key not found  
# Solution: Set environment variable
export ANTHROPIC_API_KEY="your-key-here"
```

#### 2. Android Emulator Issues
```bash
# Error: Emulator not found
# Solution: Check PATH and emulator installation
which emulator
adb devices

# Error: AVD not found
# Solution: Create AVD in Android Studio
# Tools → AVD Manager → Create Virtual Device
```

#### 3. Python Dependencies
```bash
# Error: Module not found
# Solution: Install missing dependencies
pip install -r requirements.txt

# Error: Version conflicts
# Solution: Use virtual environment
python -m venv edith-env
source edith-env/bin/activate
pip install -r requirements.txt
```

#### 4. Permission Issues (Linux/macOS)
```bash
# Error: Permission denied for pyautogui
# Solution: Grant accessibility permissions
# macOS: System Preferences → Security & Privacy → Accessibility
# Linux: Install xdotool and xinput
sudo apt install xdotool xinput
```

### Debug Mode

Enable debug logging:

```bash
# Set debug environment variable
export LOG_LEVEL=DEBUG

# Run with verbose output
python run.py --verbose

# Check logs
tail -f logs/debug-*.log
```

## 📊 Performance Optimization

### System Optimization

```bash
# Increase file descriptor limits (Linux/macOS)
ulimit -n 65536

# Optimize Python performance
export PYTHONOPTIMIZE=1
export PYTHONUNBUFFERED=1
```

### Memory Optimization

```python
# In your code, use memory-efficient settings
import os
os.environ['PYTHONHASHSEED'] = '0'
os.environ['OMP_NUM_THREADS'] = '1'
```

## 🔄 Updates & Maintenance

### Updating EDITH-QA

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run tests to verify
python -m pytest tests/
```

### Updating Agent-S

```bash
# Update Agent-S submodule
cd Agent-S
git pull origin main
cd ..

# Reinstall if needed
pip install -e Agent-S/
```

### Updating Android World

```bash
# Update Android World submodule
cd android_world
git pull origin main
cd ..

# Reinstall if needed
pip install -e android_world/
```

## 📞 Support

If you encounter issues during installation:

1. **Check the logs**: Look in `logs/` directory for error messages
2. **Verify prerequisites**: Ensure all required software is installed
3. **Test API keys**: Verify your API keys are valid and have sufficient credits
4. **Check GitHub Issues**: Search for similar problems in our issue tracker
5. **Create new issue**: Provide detailed error messages and system information

### Getting Help

- 📧 **Email**: support@edith-qa.com
- 💬 **Discord**: [Join our community](https://discord.gg/edith-qa)
- 🐛 **GitHub Issues**: [Report bugs](https://github.com/yourusername/edith-qa/issues)
- 📖 **Wiki**: [Documentation](https://github.com/yourusername/edith-qa/wiki)

---

**Next Steps**: After successful installation, proceed to the [Usage Guide](USAGE.md) to start testing your Android applications!
