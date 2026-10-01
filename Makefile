# =============================================================================
# hello-world - Development tasks
# =============================================================================
# Run `make help` to list the available targets.

.DEFAULT_GOAL := help
SHELL := /usr/bin/env bash
.SHELLFLAGS := -euo pipefail -c

PYTHON ?= python3
VENV := .venv
BIN := $(VENV)/bin
IMAGE := hello-world

.PHONY: help
help: ## Show this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n\nTargets:\n"} \
		/^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

# -----------------------------------------------------------------------------
# Setup
# -----------------------------------------------------------------------------

$(VENV)/.installed: pyproject.toml
	$(PYTHON) -m venv $(VENV)
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e ".[dev]"
	@touch $@

.PHONY: install
install: $(VENV)/.installed ## Create the virtual environment and install dev dependencies

.PHONY: hooks
hooks: install ## Install the pre-commit hooks
	$(BIN)/pre-commit install

# -----------------------------------------------------------------------------
# Quality
# -----------------------------------------------------------------------------

.PHONY: lint
lint: install ## Run the linter and check formatting
	$(BIN)/ruff check .
	$(BIN)/ruff format --check .

.PHONY: format
format: install ## Format the code and apply safe fixes
	$(BIN)/ruff format .
	$(BIN)/ruff check --fix .

.PHONY: typecheck
typecheck: install ## Run the static type checker (strict mode)
	$(BIN)/mypy

# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------

.PHONY: test
test: install ## Run the full test suite
	$(BIN)/pytest

.PHONY: coverage
coverage: install ## Run the test suite with coverage (fails under 100%)
	$(BIN)/pytest --cov --cov-report=term-missing --cov-report=xml

.PHONY: verify
verify: ## Verify the output byte by byte
	./scripts/verify_output.sh

.PHONY: check
check: lint typecheck coverage verify ## Run every check, as in CI

.PHONY: bench
bench: install ## Run the micro-benchmarks
	$(BIN)/python benchmarks/bench_greeting.py

# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------

.PHONY: run
run: install ## Run the application
	$(BIN)/python -m hello_world

.PHONY: docker-build
docker-build: ## Build the Docker image
	docker build --tag $(IMAGE):latest .

.PHONY: docker-run
docker-run: docker-build ## Run the application in Docker
	docker run --rm $(IMAGE):latest

# -----------------------------------------------------------------------------
# Housekeeping
# -----------------------------------------------------------------------------

.PHONY: clean
clean: ## Remove build artifacts and caches
	find . -type d -name __pycache__ -prune -exec rm -r {} +
	rm -rf build dist .pytest_cache .mypy_cache .ruff_cache .hypothesis .coverage coverage.xml htmlcov

.PHONY: distclean
distclean: clean ## Remove build artifacts, caches and the virtual environment
	rm -rf $(VENV)
