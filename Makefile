-include .env

# commands
lint:
	@isort development
	@flake8 development

test:
	@pytest

install:
	@pip install -U -r requirements.dev.txt
	@pip install -U -r requirements.txt

build: install lint test

# docker: control services
stop:
	@docker-compose stop

down:
	@docker-compose down -v --remove-orphans


# docker: built containers
build.test:
	@docker-compose build test

dc.test: stop build.test
	@docker-compose run test make build;
	@docker-compose stop;
