.PHONY: install install-dev run lint format test check clean

install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-dev.txt

run:
	streamlit run app.py

lint:
	ruff check .

format:
	ruff check --fix .

test:
	pytest

check: lint test

clean:
	rm -rf .pytest_cache .ruff_cache *.egg-info
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
