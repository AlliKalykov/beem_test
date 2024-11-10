REQUIREMENTS_DIR := requirements
PIP_COMPILE_ARGS := --generate-hashes --allow-unsafe --no-header --no-emit-index-url --verbose
PIP_COMPILE := cd $(REQUIREMENTS_DIR) && pip-compile $(PIP_COMPILE_ARGS)
DJANGO_ADMIN := django-cadmin

.PHONY: fix
fix:
	isort .

.PHONY: lint
lint:
	ec
	flake8
	isort -qc .

.PHONY: test
test:
	pytest

.PHONY: check-migrations
check-migrations:
	$(DJANGO_ADMIN) makemigrations --dry-run --check

.PHONY: migrations
migrations:
	$(DJANGO_ADMIN) makemigrations --no-header

.PHONY: migrate
migrate:
	$(DJANGO_ADMIN) migrate

.PHONY: compile-requirements
compile-requirements:
	pip install pip-tools
	$(PIP_COMPILE) requirements.in
	$(PIP_COMPILE) requirements.lint.in
	$(PIP_COMPILE) requirements.test.in
	$(PIP_COMPILE) requirements.dev.in
	test -f $(REQUIREMENTS_DIR)/requirements.local.in && $(PIP_COMPILE) requirements.local.in || exit 0

.PHONY: sync-requirements
sync-requirements:
	pip install pip-tools
	cd $(REQUIREMENTS_DIR) && pip-sync requirements.txt requirements.*.txt

.PHONY: get-closest-tag
get-closest-tag:
	git describe --tags --abbrev=0

.PHONY: docker-build
docker-build:
	docker-compose -f docker-compose-local.yml build

.PHONY: docker-start
docker-start:
	docker-compose -f docker-compose-local.yml up

.PHONY: docker-down
docker-down:
	docker-compose -f docker-compose-local.yml down

.DEFAULT_GOAL :=
