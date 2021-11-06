PIPENV=pipenv

all: test lint

test:
	$(PIPENV) run python -m pytest

lint:
	$(PIPENV) run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	$(PIPENV) run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	$(PIPENV) run black --check --diff .
