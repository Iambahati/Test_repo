import secrets
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create environment configuration from template'
    
    def handle(self, *args, **options):
        env = options['env']
        prj_root_dir = Path(__file__).resolve().parent.parent.parent.parent
        env_file = prj_root_dir / ('.env.prod' if env == 'prod' else '.env')
        env_example = prj_root_dir / '.env.example'
        
        if env_file.exists():
            self.stdout.write(f"{env_file} already exists")
            return
        
        if not env_example.exists():
            raise CommandError(f"Error {env_example} not found")
        
        # Copy .env.example to .env
        env_file.write_text(env_example.read_text())
        
        # Generate secret key
        secret_key = secrets.token_urlsafe(32)
        
        # Determine Django settings module
        django_settings = 'core.settings.prod' if env == 'prod' else 'core.settings.local'
        
        # Append additional settings
        with env_file.open('a') as f:
            f.write(f'\nSECRET_KEY={secret_key}\n')
            f.write(f'DJANGO_SETTINGS_MODULE={django_settings}\n')
            f.write('DEBUG=True\n')
        
        self.stdout.write(self.style.SUCCESS(f'Environment configuration created: {env_file}'))
