# Find OS to set python command
ifeq ($(OS),Windows_NT)
PY ?= python
else
PY ?= $(shell if command -v python3 >/dev/null 2>&1; then echo python3; elif command -v python >/dev/null 2>&1; then echo python; else echo ""; fi)
endif

VENV_DIR ?= .venv
VENV_PY ?= 3.11

ifeq ($(PY),)
$(error Not found python in PATH. Pass PY=python or run from a shell with python)
endif

.PHONY: install
install:
ifeq ($(OS),Windows_NT)
	@echo "Windows: using $(PY), venv=$(VENV_DIR)"
	@$(PY) -m pip install --upgrade pip
	@$(PY) -m pip install uv
	@uv venv -p $(VENV_PY) "$(VENV_DIR)"
	@"$(VENV_DIR)\Scripts\activate"
	@uv sync --frozen
else
	@echo "Unix: using $(PY), venv=$(VENV_DIR)"
	@$(PY) -m pip install --upgrade pip
	@$(PY) -m pip install uv
	@uv venv -p $(VENV_PY) "$(VENV_DIR)"
	@"$(VENV_DIR)/bin/activate"
	@uv sync --frozen
endif

.PHONY: test
test:
	@pytest --cov=src --cov=app --cov-report=term-missing test app src

.PHONY: run-app
run-app:  ## Run the FastAPI application.
	uvicorn app.api.router.v0.main:app --reload --port 8080

.PHONY: run-ruff
run-ruff: run-ruff-lint run-ruff-format  ## Run ruff to delete unused imports.

.PHONY: run-ruff-lint
run-ruff-lint:  ## Run ruff lint to delete unused imports.
	@echo "Running ruff lint to delete unused imports..."
	ruff check --fix .

.PHONY: run-ruff-format
run-ruff-format:  ## Run ruff format to delete unused imports.
	@echo "Running ruff format to delete unused imports..."
	ruff format .

.PHONY: run-pre-commit
run-pre-commit:  ## Run pre-commit checks on all files.
	@echo "Running pre-commit checks..."
	pre-commit run --all-files
