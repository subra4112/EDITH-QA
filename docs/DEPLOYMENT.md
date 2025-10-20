# EDITH-QA Deployment Guide

This guide covers various deployment options for EDITH-QA, from local development to production environments.

## 📋 Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [CI/CD Integration](#cicd-integration)
- [Production Considerations](#production-considerations)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## 🏠 Local Development

### Prerequisites

- Python 3.9+
- Android Studio with emulator
- API keys (OpenAI, Anthropic)
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/edith-qa.git
cd edith-qa

# Create virtual environment
python -m venv edith-env
source edith-env/bin/activate  # Windows: edith-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Set up environment variables
cp env.example .env
# Edit .env with your API keys

# Run tests
python -m pytest tests/

# Start development server
python run.py
```

## 🐳 Docker Deployment

### Single Container

```bash
# Build image
docker build -t edith-qa:latest .

# Run container
docker run -d \
  --name edith-qa \
  -p 8000:8000 \
  -e OPENAI_API_KEY="your-key" \
  -e ANTHROPIC_API_KEY="your-key" \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/images:/app/images \
  edith-qa:latest
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f edith-qa

# Scale services
docker-compose up -d --scale edith-qa=3
```

### Multi-Stage Build

```dockerfile
# Dockerfile.multi-stage
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim as runtime

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
CMD ["python", "run.py"]
```

## ☁️ Cloud Deployment

### AWS Deployment

#### EC2 Instance

```bash
# Launch EC2 instance (Ubuntu 20.04)
# Install Docker
sudo apt update
sudo apt install docker.io docker-compose

# Clone and deploy
git clone https://github.com/yourusername/edith-qa.git
cd edith-qa

# Set up environment
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"

# Deploy with Docker Compose
docker-compose up -d
```

#### ECS (Elastic Container Service)

```yaml
# ecs-task-definition.json
{
  "family": "edith-qa",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "edith-qa",
      "image": "your-account.dkr.ecr.region.amazonaws.com/edith-qa:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "OPENAI_API_KEY",
          "value": "your-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/edith-qa",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

### Google Cloud Platform

#### Cloud Run

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/PROJECT-ID/edith-qa

# Deploy to Cloud Run
gcloud run deploy edith-qa \
  --image gcr.io/PROJECT-ID/edith-qa \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your-key,ANTHROPIC_API_KEY=your-key
```

#### Kubernetes

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: edith-qa
spec:
  replicas: 3
  selector:
    matchLabels:
      app: edith-qa
  template:
    metadata:
      labels:
        app: edith-qa
    spec:
      containers:
      - name: edith-qa
        image: gcr.io/PROJECT-ID/edith-qa:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: edith-secrets
              key: openai-key
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
---
apiVersion: v1
kind: Service
metadata:
  name: edith-qa-service
spec:
  selector:
    app: edith-qa
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Azure Deployment

#### Container Instances

```bash
# Create resource group
az group create --name edith-rg --location eastus

# Deploy container
az container create \
  --resource-group edith-rg \
  --name edith-qa \
  --image your-registry.azurecr.io/edith-qa:latest \
  --dns-name-label edith-qa \
  --ports 8000 \
  --environment-variables OPENAI_API_KEY=your-key ANTHROPIC_API_KEY=your-key
```

## 🚀 CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t edith-qa:${{ github.sha }} .
    
    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push edith-qa:${{ github.sha }}
    
    - name: Deploy to production
      run: |
        # Deploy to your production environment
        kubectl set image deployment/edith-qa edith-qa=edith-qa:${{ github.sha }}
```

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry.com'
        IMAGE_NAME = 'edith-qa'
    }
    
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }
        
        stage('Test') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME}:${BUILD_NUMBER} python -m pytest tests/'
            }
        }
        
        stage('Deploy') {
            steps {
                sh 'docker push ${IMAGE_NAME}:${BUILD_NUMBER}'
                sh 'kubectl set image deployment/edith-qa edith-qa=${IMAGE_NAME}:${BUILD_NUMBER}'
            }
        }
    }
}
```

## 🏭 Production Considerations

### Security

```bash
# Use secrets management
kubectl create secret generic edith-secrets \
  --from-literal=openai-key=your-key \
  --from-literal=anthropic-key=your-key

# Enable RBAC
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: edith-qa-role
rules:
- apiGroups: [""]
  resources: ["secrets"]
  verbs: ["get", "list"]
```

### Performance Optimization

```yaml
# Resource limits
resources:
  requests:
    memory: "2Gi"
    cpu: "1000m"
  limits:
    memory: "4Gi"
    cpu: "2000m"

# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: edith-qa-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: edith-qa
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Monitoring

```yaml
# Prometheus monitoring
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'edith-qa'
      static_configs:
      - targets: ['edith-qa-service:8000']
```

### Logging

```yaml
# Fluentd logging
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluentd-config
data:
  fluent.conf: |
    <source>
      @type tail
      path /var/log/containers/edith-qa*.log
      pos_file /var/log/fluentd-containers.log.pos
      tag kubernetes.*
      format json
    </source>
    <match kubernetes.**>
      @type elasticsearch
      host elasticsearch.logging.svc.cluster.local
      port 9200
      index_name edith-qa
    </match>
```

## 📊 Monitoring and Maintenance

### Health Checks

```python
# health_check.py
from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint."""
    # Check dependencies
    checks = {
        "openai_api": check_openai_api(),
        "anthropic_api": check_anthropic_api(),
        "android_emulator": check_android_emulator()
    }
    
    all_healthy = all(checks.values())
    return {
        "ready": all_healthy,
        "checks": checks
    }
```

### Backup and Recovery

```bash
# Backup configuration
kubectl get configmap edith-qa-config -o yaml > backup-config.yaml

# Backup logs
kubectl logs deployment/edith-qa > backup-logs.txt

# Restore from backup
kubectl apply -f backup-config.yaml
```

### Updates and Rollbacks

```bash
# Rolling update
kubectl set image deployment/edith-qa edith-qa=edith-qa:v1.1.0

# Rollback
kubectl rollout undo deployment/edith-qa

# Check rollout status
kubectl rollout status deployment/edith-qa
```

## 🔧 Troubleshooting

### Common Issues

#### API Key Errors
```bash
# Check environment variables
kubectl exec deployment/edith-qa -- env | grep API_KEY

# Update secrets
kubectl create secret generic edith-secrets \
  --from-literal=openai-key=new-key \
  --dry-run=client -o yaml | kubectl apply -f -
```

#### Resource Limits
```bash
# Check resource usage
kubectl top pods -l app=edith-qa

# Adjust limits
kubectl patch deployment edith-qa -p '{"spec":{"template":{"spec":{"containers":[{"name":"edith-qa","resources":{"limits":{"memory":"4Gi"}}}]}}}}'
```

#### Network Issues
```bash
# Check service connectivity
kubectl exec deployment/edith-qa -- curl http://edith-qa-service:8000/health

# Debug network policies
kubectl describe networkpolicy edith-qa-netpol
```

## 📈 Scaling Strategies

### Horizontal Scaling

```yaml
# Auto-scaling configuration
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: edith-qa-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: edith-qa
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Vertical Scaling

```yaml
# Resource scaling
resources:
  requests:
    memory: "4Gi"
    cpu: "2000m"
  limits:
    memory: "8Gi"
    cpu: "4000m"
```

## 🎯 Best Practices

### Security
- Use secrets management for API keys
- Enable RBAC and network policies
- Regular security updates
- Monitor for vulnerabilities

### Performance
- Set appropriate resource limits
- Use horizontal pod autoscaling
- Implement caching strategies
- Monitor performance metrics

### Reliability
- Implement health checks
- Use rolling deployments
- Set up monitoring and alerting
- Regular backups

### Cost Optimization
- Use spot instances for non-critical workloads
- Implement auto-scaling
- Monitor resource usage
- Regular cost reviews

---

This deployment guide provides comprehensive coverage of EDITH-QA deployment options. Choose the approach that best fits your infrastructure and requirements.
