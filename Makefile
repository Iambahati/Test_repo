# Configuration
PYTHON := python
PIP := pip
MANAGE := $(PYTHON) src/manage.py
DOCKER_COMPOSE := docker-compose
ENV_FILE := .env

# Default environment
ENV := local

# Environment-specific settings
ifeq ($(ENV),prod)
    DJANGO_SETTINGS := core.settings.prod
    DOCKER_COMPOSE_FILE := docker-compose.prod.yml
else
    DJANGO_SETTINGS := core.settings.local
    DOCKER_COMPOSE_FILE := docker-compose.yml
endif

.PHONY: help install run migrate migrations shell test clean docker-build docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install              Install dependencies for $(ENV) environment"
	@echo "  make run                  Run Django development server"
	@echo "  make migrate             Apply database migrations"
	@echo "  make migrations          Create new migrations"
	@echo "  make shell               Open Django shell"
	@echo "  make test                Run tests"
	@echo "  make clean               Remove Python compiled files"
	@echo "  make docker-build        Build Docker images"
	@echo "  make docker-up           Start Docker containers"
	@echo "  make docker-down         Stop Docker containers"
	@echo ""
	@echo "Environment selection:"
	@echo "  make ENV=prod <command>  Run command in production environment"
	@echo "  make ENV=local <command> Run command in local environment (default)"

install:
	$(PIP) install -r requirements/$(ENV).txt

run:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) $(MANAGE) runserver 0.0.0.0:8000

migrate:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) $(MANAGE) migrate

migrations:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) $(MANAGE) makemigrations

shell:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) $(MANAGE) shell

test:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) $(MANAGE) test

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Docker commands
docker-build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

docker-up:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

docker-down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

# Create superuser
createsuperuser:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) $(MANAGE) createsuperuser

# Collect static files
collectstatic:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) $(MANAGE) collectstatic --noinput

# Database commands
dbshell:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) $(MANAGE) dbshell
