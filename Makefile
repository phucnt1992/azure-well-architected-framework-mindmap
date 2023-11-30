SHELL := /bin/bash

.DEFAULT_GOAL := help

PYTHON_VENV_BIN := .venv/bin/


.PHONY: help
help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  init     - Initialize the project."
	@echo "  run      - Run to create markdown mindmap."
	@echo "  generate - Run to create sitemap HTML."
	@echo "  clean    - Clean the project."
	@echo "  test     - Test the project."
	@echo "  help     - Show this help message."

.PHONY: init
init:
	@echo "Initializing..."
	@python3 -m venv .venv
	@${PYTHON_VENV_BIN}/pip3 install --upgrade pip
	@${PYTHON_VENV_BIN}/pip3 install -r requirements.txt
	@npm install && npm run prepare
	@echo "Done."

.PHONY: run
run:
	@echo "Running..."
	@git clone https://github.com/MicrosoftDocs/well-architected.git
	@${PYTHON_VENV_BIN}/python3 main.py
	@echo "Done."

.PHONY: clean
clean:
	@echo "Cleaning..."
	@rm -rf __pycache__ .pytest_cache well-architected .venv output .coverage coverage.xml node_modules
	@echo "Done."

.PHONY: test
test:
	@echo "Testing..."
	@${PYTHON_VENV_BIN}/python3 -m pytest -v
	@echo "Done."

.PHONY: test-coverage
test-coverage:
	@echo "Testing with coverage..."
	@${PYTHON_VENV_BIN}/python3 -m pytest --doctest-modules --cov=mindmap --cov-report=xml --cov-report=html
	@echo "Done."

.PHONY: generate
generate: run
	@echo "Generating..."
	@npx --yes markmap-cli ./output/MINDMAP-1.md -o ./output/index.html
	@echo "Done."

.PHONY: lint
lint:
	@echo "Linting..."
	@echo "Running flake8..."
	@${PYTHON_VENV_BIN}/flake8
	@echo "Running markdownlint..."
	@npx markdownlint-cli --ignore node_modules --ignore well-architected --ignore output .
	@echo "Done."
