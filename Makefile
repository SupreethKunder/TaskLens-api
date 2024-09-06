IMAGE_NAME := $(DOCKER_USERNAME)/$(CLIENT_NAME)-$(CNAME)

all: make-commits

.PHONY: requirements
requirements:
	@echo "$(RELEASE_TYPE)"
	@poetry install


.PHONY: do-build
do-build: requirements
	@poetry build


.PHONY: docker-deploy
docker-deploy: do-build
	@export DOCKER_BUILDKIT=1
	@docker buildx create --use
	@docker buildx build . --push -t $(IMAGE_NAME):$(VERSION)-$(DEPLOYMENT_TYPE)


.PHONY: make-commits
make-commits: docker-deploy
	@git config --local user.email "github-actions[bot]@users.noreply.github.com"
	@git config --local user.name "github-actions[bot]"
	@git add pyproject.toml
	@git push origin main -f
