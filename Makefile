# Common developer commands. Run `make help` to list them.
.DEFAULT_GOAL := help
.PHONY: help install install-dev run lint format test check clean

help:           ## list the available commands
	@grep -E '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*## "}; {printf "  %-12s %s\n", $$1, $$2}'

install:        ## runtime dependencies + this package (editable)
	pip install -r requirements.txt

install-dev: install ## + lint/test tooling
	pip install -r requirements-dev.txt

run:            ## start the Streamlit app on http://localhost:8501
	streamlit run app.py

lint:           ## ruff lint + format check (what CI runs)
	ruff check .
	ruff format --check .

format:         ## auto-fix lint findings and reformat
	ruff check --fix .
	ruff format .

test:           ## run the unit and UI smoke tests (no downloads)
	pytest

check: lint test ## everything CI runs

clean:          ## remove caches and build artefacts
	rm -rf .pytest_cache .ruff_cache build dist src/*.egg-info
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
