import os
import shutil
import fnmatch
from pathlib import Path
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Clean Python compiled files and cache directories'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Cleaning Python compiled files and cache directories...'))
        
        # Clean .pyc files
        count_pyc = 0
        for root, _, files in os.walk(Path(__file__).resolve().parent.parent.parent.parent.parent):
            for file in fnmatch.filter(files, "*.pyc"):
                os.remove(os.path.join(root, file))
                count_pyc += 1
        
        # Clean __pycache__ directories
        count_pycache = 0
        for root, dirs, _ in os.walk(Path(__file__).resolve().parent.parent.parent.parent.parent):
            for dir in fnmatch.filter(dirs, "__pycache__"):
                shutil.rmtree(os.path.join(root, dir))
                count_pycache += 1
        
        self.stdout.write(self.style.SUCCESS(f'Removed {count_pyc} .pyc files'))
        self.stdout.write(self.style.SUCCESS(f'Removed {count_pycache} __pycache__ directories'))
