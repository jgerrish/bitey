PIPENV=pipenv

all: test lint
#PYTEST_OPTS = --capture=no

test:
	$(PIPENV) run python -m pytest $(PYTEST_OPTS)

lint:
	$(PIPENV) run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	$(PIPENV) run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	$(PIPENV) run black --check --diff .
