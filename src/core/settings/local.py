from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost']

# Additional development appps
INSTALLED_APPS += [
    'django_extensions',
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'src' / 'db' / 'db.sqlite3',
    }
}
