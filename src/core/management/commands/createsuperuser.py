from django.core.management.base import BaseCommand
import inquirer
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from apps.users.models import CustomUser

class Command(BaseCommand):
    help = 'Create a superuser interactively with a pretty CLI interface'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Let\'s create a superuser!\n')

        # Check if superuser exists
        if CustomUser.objects.filter(is_superuser=True).exists():
            if not self.confirm_create_another():
                return

        questions = [
            inquirer.Text('full_name',
                         message="What's your full name?",
                         validate=lambda _, x: len(x) >= 3),
            inquirer.Text('email',
                         message="What's your email?",
                         validate=self.validate_email),
            inquirer.Password('password',
                            message="Enter your password",
                            validate=lambda _, x: len(x) >= 8),
            inquirer.Password('confirm_password',
                            message="Confirm your password",
                            validate=lambda _, x: len(x) >= 8),
        ]

        try:
            answers = inquirer.prompt(questions)
            
            if not answers:
                self.stdout.write(self.style.ERROR('❌ Superuser creation cancelled'))
                return

            if answers['password'] != answers['confirm_password']:
                self.stdout.write(self.style.ERROR('❌ Passwords don\'t match'))
                return

            user = CustomUser.objects.create_superuser(
                email=answers['email'],
                password=answers['password'],
                full_name=answers['full_name'],
            )

            self.stdout.write(self.style.SUCCESS(f'''
                ✨ Superuser created successfully!
                🔑 Email: {user.email}
                👤 Name: {user.full_name}
            '''))

        except KeyboardInterrupt:
            self.stdout.write('\n❌ Superuser creation cancelled')
            return

    def validate_email(self, answers, email):
        try:
            validate_email(email)
            if CustomUser.objects.filter(email=email).exists():
                raise ValidationError('Email already exists')
            return True
        except ValidationError:
            return False

    def confirm_create_another(self):
        question = [
            inquirer.Confirm('continue',
                           message='A superuser already exists. Create another one?',
                           default=False)
        ]
        answer = inquirer.prompt(question)
        return answer['continue'] if answer else False