# Configuration
ifeq ($(OS),Windows_NT)
    PYTHON := python
    RM_RF := rmdir /s /q
    MKDIR := mkdir
    CP := copy
    RMDIR := rmdir /s /q
    SEP := $(strip \)
    RM := del /f /q
    ENV_SET := set
else
    PYTHON := python3
    RM_RF := rm -rf
    MKDIR := mkdir -p
    CP := cp
    RMDIR := rm -rf
    SEP := /
    RM := rm -f
    ENV_SET := export
endif

PIP := $(PYTHON) -m pip
MANAGE := $(PYTHON) src$(SEP)manage.py
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

.PHONY: help install run migrate migrations shell test clean docker-build docker-up docker-down env-setup create-app createsuperuser collectstatic dbshell init

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
	$(MKDIR) src$(SEP)db
	$(ENV_SET) DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) && $(MANAGE) makemigrations

# Environment setup
env-setup:
ifeq ($(OS),Windows_NT)
	@if not exist $(ENV_FILE) ( \
		if exist .env.example ( \
			$(CP) .env.example $(ENV_FILE) && \
			echo SECRET_KEY=$(shell $(PYTHON) -c "import secrets; print(secrets.token_urlsafe(32))") >> $(ENV_FILE) && \
			echo DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) >> $(ENV_FILE) && \
			echo DEBUG=True >> $(ENV_FILE) \
		) else ( \
			echo Error: .env.example not found & exit 1 \
		) \
	) else ( \
		echo $(ENV_FILE) already exists. \
	)
else
	@if [ ! -f "$(ENV_FILE)" ]; then \
		if [ -f .env.example ]; then \
			$(CP) .env.example $(ENV_FILE) && \
			echo "SECRET_KEY=$$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')" >> $(ENV_FILE) && \
			echo "DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS)" >> $(ENV_FILE) && \
			echo "DEBUG=True" >> $(ENV_FILE); \
		else \
			echo "Error: .env.example not found"; \
			exit 1; \
		fi; \
	else \
		echo "$(ENV_FILE) already exists."; \
	fi
endif


install:
	$(PIP) install -r requirements.txt

run:
	$(ENV_SET) DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) && $(MANAGE) runserver 0.0.0.0:8000

migrate:
	$(ENV_SET) DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) && $(MANAGE) migrate

migrations:
	$(ENV_SET) DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) && $(MANAGE) makemigrations

shell:
	$(ENV_SET) DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) && $(MANAGE) shell

test:
	$(ENV_SET) DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) && $(MANAGE) test

clean:
ifeq ($(OS),Windows_NT)
	@for /r %%x in (*.pyc) do del %%x
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
else
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
endif

docker-build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

docker-up:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

docker-down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

create-app:
ifeq ($(OS),Windows_NT)
	@if "$(filter-out $@,$(MAKECMDGOALS))"=="" ( \
		echo Error: App name(s) required. Usage: make create-app app1 [app2 ...] && \
		exit 1 \
	)
	@if not exist "src\core\settings\base.py" ( \
		echo Error: src\core\settings\base.py not found && \
		exit 1 \
	)
	@for %%a in ($(filter-out $@,$(MAKECMDGOALS))) do ( \
		echo Creating Django app: %%a && \
		if not exist "src\apps\%%a" mkdir "src\apps\%%a" && \
		django-admin startapp %%a "src\apps\%%a" && \
		echo from django.apps import AppConfig > "src\apps\%%a\apps.py" && \
		echo. >> "src\apps\%%a\apps.py" && \
		echo class %%~nA^Config(AppConfig): >> "src\apps\%%a\apps.py" && \
		echo     name = 'apps.%%a' >> "src\apps\%%a\apps.py" \
	)
else
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
			$(MKDIR) src/apps/$$app; \
		fi; \
		django-admin startapp $$app src/apps/$$app; \
		echo "from django.apps import AppConfig\n\nclass $$(echo $$app | sed 's/.*/\u&/')Config(AppConfig):\n    name = 'apps.$$app'" > src/apps/$$app/apps.py; \
	done
endif

%:
	@:

createsuperuser:
	$(ENV_SET) DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) && $(MANAGE) createsuperuser

collectstatic:
	$(ENV_SET) DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) && $(MANAGE) collectstatic --noinput

dbshell:
	$(ENV_SET) DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS) && $(MANAGE) dbshell