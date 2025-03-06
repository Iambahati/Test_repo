import os
import sys
import shutil
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template.engine import Engine
from django.template import Context


class Command(BaseCommand):
    help = 'Create a new Django project with the recommended structure'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='Name of the project to create')
        parser.add_argument('--directory', type=str, help='Directory where the project will be created')
        parser.add_argument('--template', type=str, help='Template to use for project creation')

    def handle(self, *args, **options):
        project_name = options['name']
        directory = options.get('directory') or os.getcwd()
        template = options.get('template')
        
        project_dir = os.path.join(directory, project_name)
        
        # Check if project directory already exists
        if os.path.exists(project_dir):
            raise CommandError(f'Directory {project_dir} already exists')
        
        self.stdout.write(self.style.SUCCESS(f'Creating new Django project: {project_name}'))
        
        # Create project directory
        os.makedirs(project_dir)
        
        # If template is provided, use it
        if template:
            self._create_from_template(template, project_dir, project_name)
        else:
            self._create_default_structure(project_dir, project_name)
        
        self.stdout.write(self.style.SUCCESS(f'Project {project_name} created successfully at {project_dir}'))
        self.stdout.write(self.style.SUCCESS('Run the following commands to get started:'))
        self.stdout.write(f'cd {project_name}')
        self.stdout.write('python -m venv venv')
        self.stdout.write('source venv/bin/activate  # On Windows: venv\\Scripts\\activate')
        self.stdout.write('pip install -r requirements.txt')
        self.stdout.write('python src/manage.py env_setup')
        self.stdout.write('python src/manage.py init')
        self.stdout.write('python src/manage.py migrate')
        self.stdout.write('python src/manage.py runserver')

    def _create_default_structure(self, project_dir, project_name):
        # Create directory structure
        os.makedirs(os.path.join(project_dir, 'src', 'core', 'settings'))
        os.makedirs(os.path.join(project_dir, 'src', 'apps'))
        os.makedirs(os.path.join(project_dir, 'src', 'db'))
        os.makedirs(os.path.join(project_dir, 'src', 'templates'))
        os.makedirs(os.path.join(project_dir, 'src', 'static'))
        os.makedirs(os.path.join(project_dir, 'src', 'media'))
        
        # Create manage.py
        with open(os.path.join(project_dir, 'src', 'manage.py'), 'w') as f:
            f.write(self._get_manage_py_content(project_name))
        
        # Make manage.py executable
        os.chmod(os.path.join(project_dir, 'src', 'manage.py'), 0o755)
        
        # Create settings files
        with open(os.path.join(project_dir, 'src', 'core', 'settings', '__init__.py'), 'w') as f:
            f.write('')
        
        with open(os.path.join(project_dir, 'src', 'core', 'settings', 'base.py'), 'w') as f:
            f.write(self._get_base_settings_content(project_name))
        
        with open(os.path.join(project_dir, 'src', 'core', 'settings', 'local.py'), 'w') as f:
            f.write(self._get_local_settings_content())
        
        with open(os.path.join(project_dir, 'src', 'core', 'settings', 'prod.py'), 'w') as f:
            f.write(self._get_prod_settings_content())
        
        # Create core files
        with open(os.path.join(project_dir, 'src', 'core', '__init__.py'), 'w') as f:
            f.write('')
        
        with open(os.path.join(project_dir, 'src', 'core', 'asgi.py'), 'w') as f:
            f.write(self._get_asgi_content(project_name))
        
        with open(os.path.join(project_dir, 'src', 'core', 'wsgi.py'), 'w') as f:
            f.write(self._get_wsgi_content(project_name))
        
        with open(os.path.join(project_dir, 'src', 'core', 'urls.py'), 'w') as f:
            f.write(self._get_urls_content())
        
        # Create apps directory marker
        with open(os.path.join(project_dir, 'src', 'apps', '__init__.py'), 'w') as f:
            f.write('')
        
        # Create requirements.txt
        with open(os.path.join(project_dir, 'requirements.txt'), 'w') as f:
            f.write(self._get_requirements_content())
        
        # Create .env.example
        with open(os.path.join(project_dir, '.env.example'), 'w') as f:
            f.write(self._get_env_example_content())
        
        # Create .gitignore
        with open(os.path.join(project_dir, '.gitignore'), 'w') as f:
            f.write(self._get_gitignore_content())
        
        # Create docker-compose files
        with open(os.path.join(project_dir, 'docker-compose.yml'), 'w') as f:
            f.write(self._get_docker_compose_content())
        
        with open(os.path.join(project_dir, 'docker-compose.prod.yml'), 'w') as f:
            f.write(self._get_docker_compose_prod_content())
        
        # Create Dockerfile
        with open(os.path.join(project_dir, 'Dockerfile'), 'w') as f:
            f.write(self._get_dockerfile_content())
        
        # Create README.md
        with open(os.path.join(project_dir, 'README.md'), 'w') as f:
            f.write(self._get_readme_content(project_name))
        
        # Copy management commands
        os.makedirs(os.path.join(project_dir, 'src', 'core', 'management', 'commands'), exist_ok=True)
        with open(os.path.join(project_dir, 'src', 'core', 'management', '__init__.py'), 'w') as f:
            f.write('')
        with open(os.path.join(project_dir, 'src', 'core', 'management', 'commands', '__init__.py'), 'w') as f:
            f.write('')

    def _create_from_template(self, template, project_dir, project_name):
        # Clone template repository if it's a git URL
        if template.startswith(('http://', 'https://', 'git://')):
            try:
                subprocess.run(
                    ['git', 'clone', template, project_dir],
                    check=True,
                    capture_output=True,
                    text=True
                )
                # Remove .git directory to start fresh
                shutil.rmtree(os.path.join(project_dir, '.git'), ignore_errors=True)
            except subprocess.CalledProcessError as e:
                raise CommandError(f'Error cloning template repository: {e.stderr}')
        else:
            # Use local template directory
            if not os.path.exists(template):
                raise CommandError(f'Template directory {template} does not exist')
            
            # Copy template directory
            for item in os.listdir(template):
                s = os.path.join(template, item)
                d = os.path.join(project_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
        
        # Replace template placeholders with project name
        self._replace_placeholders(project_dir, project_name)

    def _replace_placeholders(self, project_dir, project_name):
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith(('.py', '.txt', '.md', '.yml', '.html', '.js', '.json')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            content = f.read()
                        
                        # Replace placeholders
                        content = content.replace('{{ project_name }}', project_name)
                        content = content.replace('{{project_name}}', project_name)
                        content = content.replace('PROJECT_NAME', project_name)
                        
                        with open(file_path, 'w') as f:
                            f.write(content)
                    except (UnicodeDecodeError, IOError):
                        # Skip binary files
                        pass

    def _get_manage_py_content(self, project_name):
        return f'''#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
'''

    def _get_base_settings_content(self, project_name):
        return f'''"""
Base settings for {project_name} project.
"""

import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    
    # Local apps
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'src', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = 'core.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {{
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    }},
    {{
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    }},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'src', 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'src', 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest framework settings
REST_FRAMEWORK = {{
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}}
'''

    def _get_local_settings_content(self):
        return '''"""
Local development settings.
"""

import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-development-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'src', 'db', 'db.sqlite3'),
    }
}

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Debug toolbar settings
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE
INTERNAL_IPS = ['127.0.0.1']
'''

    def _get_prod_settings_content(self):
        return '''"""
Production settings.
"""

import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# Static and media files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django-error.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
'''

    def _get_asgi_content(self, project_name):
        return f'''"""
ASGI config for {project_name} project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')

application = get_asgi_application()
'''

    def _get_wsgi_content(self, project_name):
        return f'''"""
WSGI config for {project_name} project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')

application = get_wsgi_application()
'''

    def _get_urls_content(self):
        return '''"""
URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
'''

    def _get_requirements_content(self):
        return '''# Core requirements
Django>=4.2.0,<5.0.0
djangorestframework>=3.14.0,<4.0.0
python-dotenv>=1.0.0,<2.0.0

# Development requirements
django-debug-toolbar>=4.2.0,<5.0.0
black>=23.7.0
flake8>=6.1.0
pytest>=7.4.0
pytest-django>=4.5.2

# Production requirements
gunicorn>=21.2.0
psycopg2-binary>=2.9.7
whitenoise>=6.5.0

# API Documentation
drf-yasg>=1.21.7

# Authentication
djangorestframework-simplejwt>=5.3.0

# CORS
django-cors-headers>=4.2.0
'''

    def _get_env_example_content(self):
        return '''# Database Configuration
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=user@example.com
EMAIL_HOST_PASSWORD=password
DEFAULT_FROM_EMAIL=noreply@example.com

# Django Configuration
ALLOWED_HOSTS=localhost,127.0.0.1
'''

    def _get_gitignore_content(self):
        return '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
staticfiles/
mediafiles/
media/

# Environment
.env
.env.prod
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.idea/
.vscode/
*.swp
*.swo
.DS_Store
'''

    def _get_docker_compose_content(self):
        return '''version: '3.8'''