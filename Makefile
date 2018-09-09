.EXPORT_ALL_VARIABLES:
APP_VERSION			= $(shell git describe --abbrev=0 --tags)
APP_NAME				= stpke
DOCKER_ID_USER	= dmi7ry

all: build

build:
	docker-compose build

release:
	export APP_VERSION=latest ;\
	docker-compose build

run: build
	docker-compose up $(APP_NAME)

up: build
	docker-compose up -d $(APP_NAME)

stop:
	docker-compose stop $(APP_NAME)

shell:
	docker exec -it $(APP_NAME) bash

push-latest:
	export APP_VERSION=latest ;\
	docker-compose push

push:
	docker-compose push

publish: build push release push-latest
