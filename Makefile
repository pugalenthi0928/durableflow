.PHONY: install run test lint format check

install:
	uv sync --all-groups

run:
	uv run uvicorn durableflow.main:app --reload

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy src

format:
	uv run ruff check --fix .
	uv run ruff format .

check: lint test

