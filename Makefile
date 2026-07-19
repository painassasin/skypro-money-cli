.PHONY: install-requirements
install-requirements:
	uv sync --frozen --all-groups

.PHONY: format
format:
	ruff format .
	ruff check . --fix

.PHONY: check
check:
	ruff check .
	ruff format --check .
	mypy .
	typos .
	uv lock --check

.PHONY: test
test:
	pytest -vv
