import subprocess
import sys
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Manage project dependencies'
    
    def add_arguments(self, parser):
        parser.add_argument('action', choices=['freeze', 'install'],
                          help='Action to perform (freeze: list dependencies, install: install from requirements.txt)')
    
    def handle(self, *args, **options):
        try:
            root_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
            action = options['action']
            
            if action == 'freeze':
                result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], 
                             check=True, capture_output=True, text=True, cwd=root_dir)
                requirements_file = root_dir / 'requirements.txt'
                requirements_file.write_text(result.stdout)
                self.stdout.write(self.style.SUCCESS('Project dependencies listed'))
            
            elif action == 'install':
                requirements_file = root_dir / 'requirements.txt'
                if not requirements_file.exists():
                    raise CommandError('requirements.txt not found')
                    
                subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                             check=True, cwd=root_dir)
                self.stdout.write(self.style.SUCCESS('Dependencies installed successfully'))
                
        except subprocess.CalledProcessError as e:
            raise CommandError(f"Error managing dependencies: {e}")