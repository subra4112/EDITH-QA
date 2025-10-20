# EDITH-QA Makefile

.PHONY: help install install-dev test test-unit test-integration lint format clean build deploy

# Default target
help: ## Show this help message
	@echo "EDITH-QA Development Commands"
	@echo "=============================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation
install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pre-commit install

# Testing
test: ## Run all tests
	python -m pytest tests/ -v --cov=edith_core --cov-report=html --cov-report=term

test-unit: ## Run unit tests only
	python -m pytest tests/unit/ -v

test-integration: ## Run integration tests only
	python -m pytest tests/integration/ -v

test-performance: ## Run performance tests only
	python -m pytest tests/performance/ -v

test-coverage: ## Run tests with coverage report
	python -m pytest tests/ --cov=edith_core --cov-report=html --cov-report=term-missing

# Code Quality
lint: ## Run linting checks
	flake8 edith_core/ tests/
	mypy edith_core/
	bandit -r edith_core/

format: ## Format code
	black edith_core/ tests/ examples/
	isort edith_core/ tests/ examples/

format-check: ## Check code formatting
	black --check edith_core/ tests/ examples/
	isort --check-only edith_core/ tests/ examples/

# Security
security: ## Run security checks
	safety check
	bandit -r edith_core/

# Building
build: ## Build package
	python -m build

build-check: ## Check package build
	twine check dist/*

# Development
dev-setup: ## Set up development environment
	python -m venv edith-env
	@echo "Activate virtual environment:"
	@echo "  source edith-env/bin/activate  # Linux/macOS"
	@echo "  edith-env\\Scripts\\activate     # Windows"
	@echo "Then run: make install-dev"

run: ## Run EDITH-QA
	python run.py

run-examples: ## Run all examples
	python examples/run_all_examples.py

# Docker
docker-build: ## Build Docker image
	docker build -t edith-qa:latest .

docker-run: ## Run Docker container
	docker run -p 8000:8000 \
		-e OPENAI_API_KEY=$$OPENAI_API_KEY \
		-e ANTHROPIC_API_KEY=$$ANTHROPIC_API_KEY \
		-v $$(pwd)/logs:/app/logs \
		-v $$(pwd)/images:/app/images \
		edith-qa:latest

docker-compose-up: ## Start services with Docker Compose
	docker-compose up -d

docker-compose-down: ## Stop Docker Compose services
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f edith-qa

# Documentation
docs: ## Generate documentation
	sphinx-build -b html docs/ docs/_build/html

docs-serve: ## Serve documentation locally
	cd docs/_build/html && python -m http.server 8001

# Cleaning
clean: ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .tox/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-logs: ## Clean up log files
	rm -rf logs/*.log
	rm -rf logs/*.json
	rm -rf test_logs/
	rm -rf test_images/

clean-all: clean clean-logs ## Clean everything

# Deployment
deploy-staging: ## Deploy to staging
	@echo "Deploying to staging..."
	# Add staging deployment commands here

deploy-prod: ## Deploy to production
	@echo "Deploying to production..."
	# Add production deployment commands here

# CI/CD
ci-test: ## Run CI test suite
	python -m pytest tests/ -v --cov=edith_core --cov-report=xml
	flake8 edith_core/ tests/
	mypy edith_core/
	bandit -r edith_core/

ci-build: ## Run CI build
	python -m build
	twine check dist/*

# Utilities
check-deps: ## Check for dependency updates
	pip list --outdated

update-deps: ## Update dependencies
	pip install --upgrade pip
	pip install -r requirements.txt --upgrade
	pip install -r requirements-dev.txt --upgrade

# Android World
android-setup: ## Set up Android World environment
	cd android_world && python setup.py install

android-test: ## Run Android World tests
	cd android_world && python minimal_task_runner.py --task=ContactsAddContact

# Agent-S
agent-s-setup: ## Set up Agent-S
	cd Agent-S && pip install -r requirements.txt

agent-s-test: ## Test Agent-S integration
	python -c "from gui_agents.s2.agents.agent_s import AgentS2; print('Agent-S2 import successful')"

# Performance
benchmark: ## Run performance benchmarks
	python -m pytest tests/performance/ -v --benchmark-only

profile: ## Profile EDITH-QA performance
	python -m cProfile -o profile.prof run.py
	python -c "import pstats; pstats.Stats('profile.prof').sort_stats('cumulative').print_stats(20)"

# Monitoring
monitor: ## Start monitoring dashboard
	@echo "Starting monitoring dashboard..."
	# Add monitoring commands here

# Backup
backup: ## Backup project data
	@echo "Creating backup..."
	tar -czf backup-$$(date +%Y%m%d-%H%M%S).tar.gz logs/ images/ config/

# Version
version: ## Show version information
	@echo "EDITH-QA Version Information"
	@echo "============================"
	@python -c "import sys; print(f'Python: {sys.version}')"
	@python -c "import edith_core; print(f'EDITH-QA: {getattr(edith_core, \"__version__\", \"unknown\")}')" 2>/dev/null || echo "EDITH-QA: not installed"
	@echo "Git: $$(git rev-parse --short HEAD 2>/dev/null || echo 'not a git repo')"

# Environment
env-check: ## Check environment setup
	@echo "Environment Check"
	@echo "================"
	@echo "Python: $$(python --version)"
	@echo "Pip: $$(pip --version)"
	@echo "OpenAI API Key: $$(if [ -n \"$$OPENAI_API_KEY\" ]; then echo 'Set'; else echo 'Not set'; fi)"
	@echo "Anthropic API Key: $$(if [ -n \"$$ANTHROPIC_API_KEY\" ]; then echo 'Set'; else echo 'Not set'; fi)"
	@echo "Docker: $$(docker --version 2>/dev/null || echo 'Not installed')"
	@echo "Git: $$(git --version 2>/dev/null || echo 'Not installed')"

# Quick commands
quick-test: ## Quick test run
	python -m pytest tests/unit/test_supervisor.py -v

quick-run: ## Quick run with sample task
	python -c "from edith_core import supervisor; print(supervisor.run_task('Test basic functionality')['supervisor_result'])"

# Help for specific targets
help-test: ## Show test help
	@echo "Test Commands:"
	@echo "  make test              - Run all tests"
	@echo "  make test-unit         - Run unit tests only"
	@echo "  make test-integration  - Run integration tests only"
	@echo "  make test-performance  - Run performance tests only"
	@echo "  make test-coverage     - Run tests with coverage"

help-docker: ## Show Docker help
	@echo "Docker Commands:"
	@echo "  make docker-build      - Build Docker image"
	@echo "  make docker-run        - Run Docker container"
	@echo "  make docker-compose-up - Start with Docker Compose"
	@echo "  make docker-logs       - View Docker logs"
