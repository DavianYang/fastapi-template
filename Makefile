export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

all: down build up test

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down --remove-orphans

test: up
	docker-compose exec web pytest . -T

down:
	docker-compose down --remove-orphans

all: down build up test
	