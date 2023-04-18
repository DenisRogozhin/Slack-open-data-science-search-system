-include .env

# commands
lint:
	@isort src
	@flake8 src

test:
	@pytest

install:
	@pip install -U -r requirements.dev.txt
	@pip install -U -r requirements.txt

build: install lint test
