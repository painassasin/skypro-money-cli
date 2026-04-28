.PHONY: format
format:
	ruff format .
	ruff check . --fix

.PHONY: check
check:
	ruff check .
	ruff format --check .

.PHONY: test
test:
	pytest -vv
