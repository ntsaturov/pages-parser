.DEFAULT_GOAL := help

## Executables
DOCKER_EXEC?=$(SUDO)$(shell which docker)
DOCKER_COMPOSE?=$(SUDO)$(shell which docker-compose)

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build:#env ## build docker image
	@($(DOCKER_EXEC) build \
	    --progress=plain \
	    -f infra/Dockerfile \
	    . -t python_base_image)

build_app: ## build docker-compose app
	@($(DOCKER_COMPOSE) -f infra/docker-compose.yml build)

run_app:build_app ## run docker-compose app
	@($(DOCKER_COMPOSE) -f infra/docker-compose.yml up -d)

stop_app: ## stop docker-compose app
	@($(DOCKER_COMPOSE) -f infra/docker-compose.yml stop)
