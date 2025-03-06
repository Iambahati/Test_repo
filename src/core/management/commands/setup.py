from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Run initial setup commands (env_setup and init)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--env',
            default='local',
            choices=['local', 'prod'],
            help='Environment to setup (local or prod)'
        )
    
    def handle(self, *args, **options):
        self.stdout.write('🚀 Starting project setup...\n')
        try:
            # Run env_setup first
            self.stdout.write('📝 Setting up environment...')
            try:
                if options['env'] == 'prod':
                    call_command('env_setup', env=options['env'])
                    self.stdout.write('🔒 Setting up production environment...')
                else:
                    self.stdout.write('🔧 Setting up local environment...')
                    call_command('env_setup')
                self.stdout.write(self.style.SUCCESS('✅ Environment setup complete'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Environment setup failed: {str(e)}'))
                raise
            
            # Then run init
            self.stdout.write('🔧 Initializing project db directory ...')
            try:
                call_command('init')
                self.stdout.write(self.style.SUCCESS('✅ Project db initialized'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Project db  initialization failed: {str(e)}'))
                raise
            
            # Install project dependencies
            self.stdout.write('📦 Installing project dependencies...')
            try:
                call_command('pip', 'install')
                self.stdout.write(self.style.SUCCESS('✅ Dependencies installed'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'❌ Dependencies installation failed: {str(e)}'))
                raise
            
            self.stdout.write(self.style.SUCCESS('✨ Setup completed successfully!'))
        except Exception:
            self.stdout.write(self.style.ERROR('❌ Setup failed'))
            raise