import os 
import subprocess
import platform
from pathlib import Path
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Builds the Docker image for the project'
    
    def check_docker_installed(self):
        """Check if Docker is installed on the system"""
        try:
            # Use shell=True on Windows to handle command exec
            shell = platform.system().lower() == 'windows'
            subprocess.run(['docker', '--version'], check=True, capture_output=True, shell=shell)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def add_arguments(self, parser):
        parser.add_argument('--env', type=str, help='Environment to use (local or prod)', default='local')

    def handle(self, *args, **options):
        # Check for Docker installation first
        if not self.check_docker_installed():
            self.stdout.write(self.style.ERROR('Docker is not installed. Please install Docker first.'))
            return

        env = options['env']
        prj_root_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
        docker_compose_file =   prj_root_dir / ('docker-compose.prod.yml' if env != 'prod' else 'docker-compose.yml')
    
        
        if not os.path.exists(docker_compose_file):
            self.stdout.write(self.style.ERROR(f"File {docker_compose_file} not found."))
            return
        
        self.stdout.write(self.style.SUCCESS(f"Building Docker image using {docker_compose_file}..."))
        
        try:
            # Use shell=True on Windows to handle command execution
            shell = platform.system().lower() == 'windows'
            # Use 'docker compose' instead of 'docker-compose' for newer Docker versions
            docker_cmd = ['docker', 'compose'] if shell else ['docker-compose']
            
            process = subprocess.run(
                [*docker_cmd, '-f', docker_compose_file, 'build'],
                check=True,
                capture_output=True,
                text=True,
                shell=shell
            )
            self.stdout.write(process.stdout)
            self.stdout.write(self.style.SUCCESS('Docker images built successfully!'))
        except subprocess.CalledProcessError as e:
            self.stdout.write(self.style.ERROR(f'Error building Docker images: {e.stderr}'))