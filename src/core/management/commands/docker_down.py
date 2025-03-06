import os
import subprocess
import platform
from pathlib import Path

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Stop Docker containers'

    def add_arguments(self, parser):
        parser.add_argument(
            '--env',
            default='local',
            help='Environment to use (local or prod)'
        )
    
    def check_docker_installed(self):
        """Check if Docker is installed on the system"""
        try:
            # Use shell=True on Windows to handle command exec
            shell = platform.system().lower() == 'windows'
            subprocess.run(['docker', '--version'], check=True, capture_output=True, shell=shell)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def handle(self, *args, **options):
        # Check for Docker installation first
        if not self.check_docker_installed():
            self.stdout.write(self.style.ERROR('Docker is not installed. Please install Docker first.'))
            return

        env = options['env']
        prj_root_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        docker_compose_file =   prj_root_dir / ('docker-compose.prod.yml' if env != 'prod' else 'docker-compose.yml')
        
        if not os.path.exists(docker_compose_file):
            self.stdout.write(self.style.ERROR(f'Error: {docker_compose_file} not found'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Stopping Docker containers using {docker_compose_file}...'))
        
        try:
            process = subprocess.run(
                ['docker-compose', '-f', docker_compose_file, 'down'],
                check=True,
                capture_output=True,
                text=True
            )
            self.stdout.write(process.stdout)
            self.stdout.write(self.style.SUCCESS('Docker containers stopped successfully!'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Error stopping Docker containers: {e.stderr}'))
