from .base import *

# Security and Performance Settings
DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database Configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv('DB_NAME'),
        "USER": os.getenv('DB_USER'),
        "PASSWORD": os.getenv('DB_USER_PASSWORD'),
        "HOST": os.getenv('DB_HOST'),
        "PORT": os.getenv('DB_PORT'),
    }
}

# Static and Media Files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Security Enhancements
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}
