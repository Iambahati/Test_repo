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
			echo "Created .env.prod with default production settings"; \
		else \
			echo ".env.prod already exists."; \
		fi; \
	else \
		if [ ! -f .env ]; then \
			if [ -f .env.example ]; then \
				cp .env.example .env && \
				sed -i.bak "s|SECRET_KEY=.*|SECRET_KEY=$(shell openssl rand -base64 32 | tr -d '=' | tr -d '\n')|g" .env && \
				rm .env.bak; \
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
	find . -type f -name "*.sqlite3" -delete

docker-build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

docker-up:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

docker-down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

create-app:
ifndef APP_NAME
	@echo "Error: APP_NAME is required. Usage: make create-app APP_NAME=your_app_name"
	@exit 1
endif
	@echo "Creating Django app: $(APP_NAME)"
	# Create the app directory and run the Django startapp command
	cd src/apps && mkdir -p $(APP_NAME) && $(MANAGE) startapp $(APP_NAME) $(APP_NAME)
	@echo "Updating INSTALLED_APPS in base settings..."
	# Check if INSTALLED_APPS exists and append the new app
	@if grep -q "INSTALLED_APPS = \[" src/core/settings/base.py; then \
		sed -i.bak '/INSTALLED_APPS = \[/a \    '\''apps.$(APP_NAME)'\''\,' src/core/settings/base.py && \
		rm src/core/settings/base.py.bak; \
	else \
		$(error Error: INSTALLED_APPS list not found in base.py) \
	fi
	@echo "Created app $(APP_NAME) in src/apps/$(APP_NAME) and updated settings"

createsuperuser:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) $(MANAGE) createsuperuser

collectstatic:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) $(MANAGE) collectstatic --noinput

dbshell:
	DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) $(MANAGE) dbshell