# EDITH-QA Docker Configuration

## Dockerfile

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p logs images

# Expose port for FastAPI server
EXPOSE 8000

# Set default command
CMD ["python", "run.py"]
```

## Docker Compose

```yaml
version: '3.8'

services:
  edith-qa:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - HF_TOKEN=${HF_TOKEN}
    volumes:
      - ./logs:/app/logs
      - ./images:/app/images
    restart: unless-stopped
    
  android-emulator:
    image: budtmo/docker-android:emulator_11.0
    privileged: true
    ports:
      - "6080:6080"
      - "5554:5554"
      - "5555:5555"
    environment:
      - EMULATOR_DEVICE=Samsung Galaxy S10
      - WEB_VNC=true
    volumes:
      - android-storage:/root/android_emulator
    depends_on:
      - edith-qa

volumes:
  android-storage:
```

## Build and Run

```bash
# Build Docker image
docker build -t edith-qa:latest .

# Run with Docker Compose
docker-compose up -d

# Run individual container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY="your-key" \
  -e ANTHROPIC_API_KEY="your-key" \
  edith-qa:latest
```
