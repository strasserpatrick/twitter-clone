format-src:
	black src
	isort src
	flake8 src

format-tests:
	black test
	isort test
	flake8 test

format-all: format-src format-tests
