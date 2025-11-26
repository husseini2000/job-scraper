# ─────────────────────────────────────────────
#   Job Scraper Pipeline - Makefile
#   Provides clean commands for development,
#   testing, linting, running ETL, and setup.
# ─────────────────────────────────────────────

# Default target
.DEFAULT_GOAL := help

# Configurable venv dir
VENV_DIR ?= .venv

# Detect platform and configure python/venv commands accordingly
ifeq ($(OS),Windows_NT)
	PYTHON ?= py -3
	VENV_PY := $(VENV_DIR)\\Scripts\\python.exe
	VENV_PIP := $(VENV_DIR)\\Scripts\\pip.exe
	ACTIVATE_MSG := $(VENV_DIR)\\Scripts\\Activate.ps1
else
	PYTHON ?= $(shell command -v python3 2>/dev/null || command -v python)
	VENV_PY := $(VENV_DIR)/bin/python
	VENV_PIP := $(VENV_DIR)/bin/pip
	ACTIVATE_MSG := source $(VENV_DIR)/bin/activate
endif

.PHONY: help install test lint format clean clean-data run scrape dev-setup

# ─────────────────────────────────────────────
# Help Menu
# ─────────────────────────────────────────────
help:
	@echo ""
	@echo "📌 Job Scraper Pipeline — Available Commands"
	@echo "───────────────────────────────────────────"
	@echo "  make install        Install dependencies (creates venv at $(VENV_DIR))"
	@echo "  make dev-setup      First-time development setup"
	@echo "  make test           Run tests with coverage"
	@echo "  make lint           Run flake8 + mypy"
	@echo "  make format         Format code using black"
	@echo "  make run            Run the full ETL pipeline"
	@echo "  make scrape SITE=x  Run specific scraper"
	@echo "  make scrape         Run all scrapers"
	@echo "  make clean          Remove build/test artifacts"
	@echo "  make clean-data     Delete all scraped data ⚠️"
	@echo ""

# ─────────────────────────────────────────────
# Install Dependencies
# ─────────────────────────────────────────────
install:
	@echo "Creating virtual environment at $(VENV_DIR)..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Installing dependencies..."
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r requirements.txt
	@echo "✓ Installation complete!"
	@echo "Activate with:"
	@echo "  $(ACTIVATE_MSG)"

# ─────────────────────────────────────────────
# Testing
# ─────────────────────────────────────────────
test:
	@echo "Running tests with coverage..."
	$(VENV_PY) -m pytest tests/ -v --cov=. --cov-report=html --cov-report=term
	@echo "✓ Coverage report generated at: htmlcov/index.html"

# ─────────────────────────────────────────────
# Lint + Type Check
# ─────────────────────────────────────────────
lint:
	@echo "Running flake8..."
	$(VENV_PY) -m flake8 extract/ transform/ load/ pipeline/ core/ --max-line-length=100
	@echo "Running mypy..."
	$(VENV_PY) -m mypy extract/ transform/ load/ pipeline/ core/ --ignore-missing-imports
	@echo "✓ Linting complete!"

# ─────────────────────────────────────────────
# Format code
# ─────────────────────────────────────────────
format:
	@echo "Formatting code with black..."
	$(VENV_PY) -m black extract/ transform/ load/ pipeline/ core/ cli.py
	@echo "✓ Code formatted!"

# ─────────────────────────────────────────────
# Clean build + cache files
# ─────────────────────────────────────────────
clean:
	@echo "Cleaning generated and cached files..."
	$(PYTHON) - <<PY
	import shutil, glob, os
	for d in glob.glob('**/__pycache__', recursive=True):
		shutil.rmtree(d, ignore_errors=True)
	for f in glob.glob('**/*.pyc', recursive=True) + glob.glob('**/*.pyo', recursive=True):
		try:
			os.remove(f)
		except Exception:
			pass
	for d in ('.pytest_cache', '.coverage', 'htmlcov', '.mypy_cache'):
		shutil.rmtree(d, ignore_errors=True)
	print('✓ Cleanup complete!')
	PY

# ─────────────────────────────────────────────
# Clean scraped data (dangerous)
# ─────────────────────────────────────────────
clean-data:
	@echo "⚠️ WARNING: This will delete ALL scraped data."
	@$(PYTHON) - <<PY
	resp = input('Proceed? [y/N] ').strip().lower()
	if resp in ('y', 'yes'):
		import shutil
		for p in ('data/raw', 'data/intermediate', 'data/processed', 'data/logs'):
			shutil.rmtree(p, ignore_errors=True)
		print('✓ Data cleaned!')
	else:
		print('Cancelled.')
	PY

# ─────────────────────────────────────────────
# Run full ETL Pipeline
# ─────────────────────────────────────────────
run:
	@echo "Running full ETL pipeline..."
	$(VENV_PY) cli.py pipeline --all

# ─────────────────────────────────────────────
# Run scrapers
# ─────────────────────────────────────────────
scrape:
	@if [ -z "$(SITE)" ]; then \
		echo "Running all scrapers..."; \
		$(VENV_PY) cli.py scrape --all; \
	else \
		echo "Running scraper: $(SITE)"; \
		$(VENV_PY) cli.py scrape --site $(SITE); \
	fi

# ─────────────────────────────────────────────
# Development Setup
# ─────────────────────────────────────────────
dev-setup: install
	@echo "Setting up development environment..."
	@$(PYTHON) - <<PY
	import os
	dirs = [
		'data/raw', 'data/intermediate', 'data/processed', 'data/logs',
		'metadata/cache', 'metadata/mapping'
	]
	for d in dirs:
		os.makedirs(d, exist_ok=True)
	print('✓ Development setup complete!')
	PY
		@echo "Next steps:"
		@echo "  $(ACTIVATE_MSG)"
		@echo "  make test"

