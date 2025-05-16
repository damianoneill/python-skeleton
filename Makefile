.PHONY: help install install-dev clean lint format test test-cov test-unit test-integration build run sync lock pre-commit pre-commit-install pre-commit-update check

# Use bash as shell
SHELL := /bin/bash

# Project name (from top-level directory name)
PROJECT_NAME ?= $(shell basename $(CURDIR))

# Default command if not specified
CMD ?= $(PROJECT_NAME)

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

venv: ## Create a virtual environment if it doesn't exist
	@if [ ! -d "$(VENV_PATH)" ]; then \
		echo "Creating virtual environment at $(VENV_PATH)"; \
		uv venv $(VENV_PATH); \
		echo "Virtual environment created. Activate with: source $(VENV_PATH)/bin/activate"; \
	else \
		echo "Virtual environment already exists at $(VENV_PATH)"; \
	fi

install: venv ## Install the package for production
	uv pip install -e .

install-dev: venv ## Install the package with development dependencies
	uv pip install -e . --group dev
	$(MAKE) pre-commit-install

clean: ## Clean up build artifacts and temporary files
	uv tool run pyclean . --debris
	rm -rf htmlcov
	# pyclean with --debris handles Python bytecode, pytest cache, coverage database,
	# and packaging artifacts (build, dist, egg-info)

lint: ## Check code style with Ruff (with auto-fixes)
	uv run ruff check --fix .

format: ## Format code with Ruff
	uv run ruff format .

test: ## Run all tests
	uv run pytest

test-cov: ## Run tests with coverage
	uv run pytest --cov --cov-report=term --cov-report=html

test-unit: ## Run only unit tests
	uv run pytest -m unit

test-integration: ## Run only integration tests
	uv run pytest -m integration

build: ## Build the package
	uv pip install build
	uv run python -m build

run: ## Run a specific command (usage: make run CMD=command, defaults to directory name)
	uv run $(CMD)

sync: ## Sync dependencies
	uv sync

lock: ## Update lockfile
	uv lock

pre-commit: ## Run pre-commit on all files
	uvx pre-commit run --all-files

pre-commit-install: ## Install pre-commit hooks
	uvx pre-commit install

pre-commit-update: ## Update pre-commit hooks
	uvx pre-commit autoupdate

check: clean format lint pre-commit test ## Run all checks and tests

# Default target
all: clean format lint test
