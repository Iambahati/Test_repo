import os
from pathlib import Path
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Initialize the project, create directory structure and prepare initial setup"
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Initializing project..."))
        
        # Calculate path relative to this command file
        prj_root_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        db_path = prj_root_dir / 'db'
        
        # Create db directory if it doesn't exist
        os.makedirs(db_path, exist_ok=True)
        self.stdout.write(self.style.SUCCESS(f'Created directory: {db_path}'))
        
        # Run initial migrations
        try:
            call_command('makemigrations')
            self.stdout.write(self.style.SUCCESS("Created initial migrations"))
        except Exception as e:
            raise CommandError(f"Error creating initial migrations: {e}")