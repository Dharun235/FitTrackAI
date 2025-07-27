# FitTrackAI - Development Commands
# Local deployment only (no Docker)

.PHONY: help install setup run test clean lint format check

help: ## Show this help message
	@echo "FitTrackAI - Development Commands"
	@echo "=================================="
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dependencies
	@echo "📦 Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed successfully!"

setup: ## Setup Ollama (required for AI functionality)
	@echo "🤖 Setting up Ollama..."
	python setup_ollama.py
	@echo "✅ Ollama setup complete!"

run: ## Start the FitTrackAI application
	@echo "🚀 Starting FitTrackAI..."
	python start_app.py

dev: ## Start in development mode with auto-reload
	@echo "🔧 Starting in development mode..."
	python app.py

test: ## Run tests
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v

clean: ## Clean up temporary files and caches
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf .coverage
	@echo "✅ Cleanup complete!"

lint: ## Run code linting
	@echo "🔍 Running code linting..."
	flake8 app.py data_explorer.py setup_ollama.py start_app.py
	@echo "✅ Linting complete!"

format: ## Format code with black
	@echo "🎨 Formatting code..."
	black app.py data_explorer.py setup_ollama.py start_app.py
	@echo "✅ Code formatting complete!"

check: ## Run all checks (lint, format, test)
	@echo "🔍 Running all checks..."
	$(MAKE) lint
	$(MAKE) format
	$(MAKE) test
	@echo "✅ All checks complete!"

check-ollama: ## Check if Ollama is running
	@echo "🤖 Checking Ollama status..."
	@python -c "import requests; print('✅ Ollama is running' if requests.get('http://localhost:11434/api/tags', timeout=5).status_code == 200 else '❌ Ollama is not running')"

install-dev: ## Install development dependencies
	@echo "📦 Installing development dependencies..."
	pip install -r requirements.txt
	pip install pytest flake8 black
	@echo "✅ Development dependencies installed!"

full-setup: ## Complete setup (install + setup + check)
	@echo "🚀 Complete FitTrackAI setup..."
	$(MAKE) install
	$(MAKE) setup
	$(MAKE) check-ollama
	@echo "✅ Full setup complete! Run 'make run' to start the application."

# Database commands
db-info: ## Show database information
	@echo "📊 Database Information:"
	@python -c "import sqlite3; conn = sqlite3.connect('data/db/processed_apple_health_data.db'); cursor = conn.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"'); tables = cursor.fetchall(); print(f'Tables: {[t[0] for t in tables]}'); conn.close()"

# Quick start for new users
quick-start: ## Quick start guide for new users
	@echo "🚀 FitTrackAI Quick Start"
	@echo "========================"
	@echo "1. Install dependencies: make install"
	@echo "2. Setup Ollama: make setup"
	@echo "3. Start application: make run"
	@echo "4. Open browser: http://localhost:5000"
	@echo ""
	@echo "For more help, run: make help" 