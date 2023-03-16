# Python testing
CMD		  = poetry run
PYMODULE  = openly
TESTS	  = tests
MAXLENGTH = 79

all: type test lint isort-check black-check bandit safety

lint:
	$(CMD) flake8 $(PYMODULE) $(TESTS)

type:
	$(CMD) mypy $(PYMODULE) $(TESTS)

test:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS)

test-cov:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report html

test-cov-xml:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report xml

isort:
	$(CMD) isort --profile black --line-length $(MAXLENGTH) $(PYMODULE) $(TESTS)

isort-check:
	$(CMD) isort --check-only --profile black --line-length $(MAXLENGTH) $(PYMODULE) $(TESTS)

black:
	$(CMD) black --line-length $(MAXLENGTH) $(PYMODULE) $(TESTS)

black-check:
	$(CMD) black --check --line-length $(MAXLENGTH) $(PYMODULE) $(TESTS)

bandit:
	$(CMD) bandit --recursive $(PYMODULE)

safety:
	$(CMD) safety --disable-optional-telemetry-data check

clean:
	git clean -Xdf # Delete all files in .gitignore

.PHONY: all clean lint type test test-cov black black-check isort isort-check bandit safety
