.DEFAULT_GOAL := help

## General settings

## Executables
POETRY_EXEC?=$(DOCKER_EXEC) run --rm -v $(PWD):/app -w /app python_base_image poetry
DOCKER_EXEC?=$(SUDO)$(shell which docker)

GIT_BRANCH?=$(shell git rev-parse --abbrev-ref HEAD)
ifneq "$(GIT_BRANCH)" "main"
  SHORT_COMMIT_HASH?=$(shell git rev-parse --short HEAD)
  IMAGE_SUFFIX?=-$(shell echo "$(GIT_BRANCH)" | tr "/" "-")-$(SHORT_COMMIT_HASH)
else
  IMAGE_SUFFIX?=
endif


help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

env:
	$(eval APP_VERSION=$(shell $(POETRY_EXEC) version -s))
	$(eval IMAGE_VERSION=$(APP_VERSION)$(IMAGE_SUFFIX))
	$(eval APP_NAME=$(shell $(POETRY_EXEC) version | cut -d " " -f1))
	$(eval IMAGE_TAG=$(APP_NAME):$(IMAGE_VERSION))

app_name:env ## get application name
	@echo $(APP_NAME)

app_version:env ## get image version (target using in teamcity-common-v3)
	@echo $(IMAGE_VERSION)

image_tag:env ## get image tag
	@echo $(IMAGE_TAG)

increment_version:env ## increment version
	@$(POETRY_EXEC) version minor
	$(eval NEW_APP_VERSION=$(shell $(POETRY_EXEC) version -s))

build:#env ## build docker image
	@($(DOCKER_EXEC) build \
	    --progress=plain \
	    -f infra/Dockerfile \
	    . -t python_base_image)

build_app: ## build docker-compose app
	sudo docker-compose -f infra/docker-compose.yml build

run_app:build_app ## run docker-compose app
	sudo docker-compose -f infra/docker-compose.yml up -d

stop_app: ## stop docker-compose app
	sudo docker-compose -f infra/docker-compose.yml stop
