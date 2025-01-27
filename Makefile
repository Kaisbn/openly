# Python testing
CMD		  = poetry run
PYMODULE  = openly
TESTS	  = tests
MAXLENGTH = 79

all: test check

check: type-check format-check bandit safety

test:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS)

test-cov:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report html

test-cov-xml:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report xml

type-check:
	$(CMD) mypy $(PYMODULE) $(TESTS)

format:
	$(CMD) ruff format $(PYMODULE) $(TESTS)

format-check:
	$(CMD) ruff check $(PYMODULE) $(TESTS)

bandit:
	$(CMD) bandit --recursive $(PYMODULE)

safety:
	$(CMD) safety --disable-optional-telemetry scan

clean:
	git clean -Xdf # Delete all files in .gitignore

.PHONY: all clean lint type test test-cov black black-check isort isort-check bandit safety
