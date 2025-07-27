.PHONY: help install test clean run lint format docs

help: ## Show this help message
	@echo "FitTrackAI - Development Commands"
	@echo "=================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8

test: ## Run tests
	python -m pytest tests/ -v

test-coverage: ## Run tests with coverage
	python -m pytest tests/ --cov=app --cov-report=html --cov-report=term-missing

lint: ## Run linting
	flake8 app.py tests/

format: ## Format code with black
	black app.py tests/

run: ## Run the application
	python app.py

run-dev: ## Run the application in development mode
	FLASK_ENV=development python app.py

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/

build: ## Build the package
	python setup.py sdist bdist_wheel

docs: ## Generate documentation
	@echo "Documentation is in README.md"

check: ## Run all checks (lint, test, format)
	@echo "Running all checks..."
	@make lint
	@make test
	@make format

pre-commit: ## Run pre-commit checks
	@echo "Running pre-commit checks..."
	@make clean
	@make install-dev
	@make check

release: ## Prepare for release
	@echo "Preparing for release..."
	@make clean
	@make test-coverage
	@make build
	@echo "Release ready! Check dist/ directory." 