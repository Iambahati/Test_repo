import re
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from pathlib import Path


class Command(BaseCommand):
    help = 'Create new Django app(s) in the src/apps directory (comma-separated)'
    
    def add_arguments(self, parser):
        parser.add_argument('app_names', type=str, help='Comma-separated name(s) of the app(s) to create')
        
    def handle(self, *args, **options):
        app_names = [name.strip().lower() for name in options['app_names'].split(',')]
        
        src_dir = Path(__file__).resolve().parent.parent.parent.parent
        core_dir = src_dir / 'core'
        settings_path = core_dir / 'settings' / 'base.py'
        
        if not settings_path.exists():
            raise CommandError(f"Error: {settings_path} file not found. Are you in the root directory of the project?")
        
        for app_name in app_names:
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', app_name):
                raise CommandError(f"'{app_name}' is not a valid Django app name")
            
            app_path = src_dir / 'apps' / app_name
            if app_path.exists():
                raise CommandError(f"App '{app_name}' already exists")
            
            app_path.mkdir(parents=True, exist_ok=True)
            call_command('startapp', app_name, str(app_path))
            
            # Update apps.py
            with open(app_path / 'apps.py', 'w') as f:
                f.write(f'''from django.apps import AppConfig\n
class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.apps.{app_name}'
''')
            
            # Update INSTALLED_APPS
            with open(settings_path, 'r+') as f:
                content = f.read()
                if f'"apps.{app_name}"' not in content:
                    installed_apps_end = content.find('INSTALLED_APPS = [') + content[content.find('INSTALLED_APPS = ['):].find(']')
                    content = content[:installed_apps_end] + f'    "apps.{app_name}",\n' + content[installed_apps_end:]
                    f.seek(0)
                    f.write(content)
                    f.truncate()
            
                
            self.stdout.write(self.style.SUCCESS(f"Created Django app '{app_name}' and added it to INSTALLED_APPS"))
