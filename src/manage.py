import os
import sys
from pathlib import Path
import secrets

from django.core.management.commands.runserver import Command as runserver
from dotenv import load_dotenv

# port_number =

def main():
    """Run administrative tasks."""
    # Load .env file first
    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(BASE_DIR / '.env')
    
    # Get settings module from .env or use default
    settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'core.settings.local')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()