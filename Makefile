# Configuration
PYTHON := python3
PIP := pip
MANAGE := $(PYTHON) src/manage.py
DOCKER_COMPOSE := docker-compose

# Default environment
ENV := local

# Environment-specific settings
ifeq ($(ENV),prod)
    DJANGO_SETTINGS := core.settings.prod
    DOCKER_COMPOSE_FILE := docker-compose.prod.yml
    ENV_FILE := .env.prod
else
    DJANGO_SETTINGS := core.settings.local
    DOCKER_COMPOSE_FILE := docker-compose.yml
    ENV_FILE := .env
endif

.PHONY: help install run migrate migrations shell test clean docker-build docker-up docker-down env-setup create-app createsuperuser collectstatic dbshell

help:
	@echo "Available commands:"
	@echo "  make init               Initialize project"
	@echo "  make env-setup          Create environment configuration"
	@echo "  make install            Install dependencies"
	@echo "  make run                Run Django development server"
	@echo "  make create-app         Create new Django app"
	@echo "  make migrate            Apply database migrations"
	@echo "  make migrations         Create new migrations"
	@echo "  make shell              Open Django shell"
	@echo "  make test               Run tests"
	@echo "  make clean              Remove Python compiled files"
	@echo "  make docker-build       Build Docker images"
	@echo "  make docker-up          Start Docker containers"
	@echo "  make docker-down        Stop Docker containers"
	@echo ""
	@echo "Environment selection:"
	@echo "  make ENV=prod <command>  Run command in production environment"
	@echo "  make ENV=local <command> Run command in local environment (default)"

init:
	mkdir -p src/db
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) $(MANAGE) migrate

# Environment setup
env-setup:
	@if [ "$(ENV)" = "prod" ]; then \
		if [ ! -f .env.prod ]; then \
			echo "Creating production environment file .env.prod"; \
			echo "# Django Production Settings" > .env.prod; \
			echo "SECRET_KEY=$(shell openssl rand -base64 32 | tr -d '=' | tr -d '\n')" >> .env.prod; \
			echo "DJANGO_SETTINGS_MODULE=core.settings.prod" >> .env.prod; \
			echo "DEBUG=0" >> .env.prod; \
			echo "ALLOWED_HOSTS=your-domain.com,www.your-domain.com" >> .env.prod; \
			echo "# Database Configuration" >> .env.prod; \
			echo "DB_NAME=django_prod" >> .env.prod; \
			echo "DB_USER=django_user" >> .env.prod; \
			echo "DB_PASSWORD=$(shell openssl rand -base64 12)" >> .env.prod; \
			echo "DB_HOST=db" >> .env.prod; \
			echo "DB_PORT=5432" >> .env.prod; \
			echo "Created .env.prod and DJANGO_SETTINGS_MODULE set to core.settings.prod"; \
		else \
			echo ".env.prod already exists."; \
		fi; \
	else \
		if [ ! -f .env ]; then \
			if [ -f .env.example ]; then \
				cp .env.example .env && \
				sed -i.bak "s|DJANGO_SETTINGS_MODULE=.*|DJANGO_SETTINGS_MODULE=core.settings.local|g" .env && \
				sed -i.bak "s|DEBUG=.*|DEBUG=True|g" .env && \
				sed -i.bak "s|SECRET_KEY=.*|SECRET_KEY=$(shell openssl rand -base64 32 | tr -d '=' | tr -d '\n')|g" .env && \
				rm .env.bak; \
				echo "Created .env and DJANGO_SETTINGS_MODULE set to core.settings.local"; \
			else \
				echo "Error: .env.example not found"; \
				exit 1; \
			fi; \
		else \
			echo ".env already exists."; \
		fi; \
	fi

install:
	$(PIP) install -r requirements.txt

run:
	$(MANAGE) runserver 0.0.0.0:8000

migrate:
	$(MANAGE) migrate

migrations:
	$(MANAGE) makemigrations

shell:
	$(MANAGE) shell

test:
	$(MANAGE) test

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	# find . -type f -name "*.sqlite3" -delete

docker-build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

docker-up:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

docker-down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

create-app:
	@if [ -z "$(filter-out $@,$(MAKECMDGOALS))" ]; then \
		echo "Error: App name(s) required. Usage: make create-app app1 [app2 ...]"; \
		exit 1; \
	fi
	@if [ ! -f "src/core/settings/base.py" ]; then \
		echo "Error: src/core/settings/base.py not found"; \
		exit 1; \
	fi
	@for app in $(filter-out $@,$(MAKECMDGOALS)); do \
		echo "Creating Django app: $$app"; \
		if [ ! -d "src/apps/$$app" ]; then \
			mkdir -p src/apps/$$app; \
		fi; \
		django-admin startapp $$app src/apps/$$app; \
		touch src/apps/$$app/apps.py; \
		capitalized_app=$$(echo "$$app" | sed 's/.*/\u&/'); \
		echo "from django.apps import AppConfig\n\nclass $${capitalized_app}Config(AppConfig):\n    name = 'apps.$$app'" > src/apps/$$app/apps.py; \
		echo "Updating INSTALLED_APPS in settings..."; \
		if ! grep -q "'apps.$$app'" src/core/settings/base.py; then \
			sed -i '/INSTALLED_APPS = \[/,/]/ s/]/    "apps.'"$$app"'",\n]/' src/core/settings/base.py; \
			echo "✓ Created app $$app and updated INSTALLED_APPS"; \
		else \
			 echo "App $$app already registered"; \
		fi; \
	done

%:
	@:

createsuperuser:
	$(MANAGE) createsuperuser

collectstatic:
	$(MANAGE) collectstatic --noinput

dbshell:
	$(MANAGE) dbshell


