# Find OS to set python command
ifeq ($(OS),Windows_NT)
PY ?= python
else
PY ?= $(shell if command -v python3 >/dev/null 2>&1; then echo python3; elif command -v python >/dev/null 2>&1; then echo python; else echo ""; fi)
endif

VENV_DIR ?= .venv
VENV_PY ?= 3.13

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
	@coverage run -m pytest 