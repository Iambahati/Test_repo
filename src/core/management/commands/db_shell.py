from django.core.management.base import BaseCommand
from django.apps import apps
from django.db.models import Count, Q
from ptpython.repl import embed
import sys
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from rich.panel import Panel
from datetime import datetime
import inspect

class Command(BaseCommand):
    help = 'Enhanced interactive database shell with all models pre-imported'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-banner',
            action='store_true',
            help='Skip the welcome banner'
        )

    def create_banner(self, console):
        return Panel(
            """Django DB Shell
Interactive Database Shell with Models
Type help() for assistance""",
            style="bold green",
            subtitle=f"Session started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            width=60
        )

    def get_model_stats(self, model):
        """Get detailed statistics for a model"""
        return {
            'count': model.objects.count(),
            'fields': [f.name for f in model._meta.fields],
            'relationships': [f.name for f in model._meta.get_fields() if f.is_relation],
            'table': model._meta.db_table
        }

    def create_helper_functions(self, models, console):
        def help():
            """Display comprehensive help information"""
            console.print("\n📚 Available Commands:", style="bold cyan")
            console.print("• help() - Show this help message")
            console.print("• inspect_model(model_name) - Show detailed model information")
            console.print("• list_models() - Show all available models")
            console.print("• search(model, **kwargs) - Search objects with given criteria")
            
            console.print("\n🔍 Common Queries:", style="bold cyan")
            console.print("• Model.objects.all()")
            console.print("• Model.objects.filter(field=value)")
            console.print("• Model.objects.get(id=1)")
            console.print("• Model.objects.values('field').annotate(count=Count('id'))")
            
            console.print("\n💡 Example:", style="bold yellow")
            if models:
                console.print(f">>> {list(models.keys())[0]}.objects.all()\n")

        def inspect_model(model_name):
            """Display detailed information about a specific model"""
            if model_name not in models:
                console.print(f"❌ Model '{model_name}' not found!", style="bold red")
                return
            
            model = models[model_name]
            stats = self.get_model_stats(model)
            
            table = Table(title=f"📋 Model: {model_name}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Table Name", stats['table'])
            table.add_row("Total Records", str(stats['count']))
            table.add_row("Fields", ", ".join(stats['fields']))
            table.add_row("Relationships", ", ".join(stats['relationships']))
            
            console.print(table)

        def list_models():
            """Display all available models and their counts"""
            table = Table(title="📚 Available Models")
            table.add_column("Model", style="cyan")
            table.add_column("Count", style="yellow")
            table.add_column("Table", style="green")
            
            for name, model in models.items():
                stats = self.get_model_stats(model)
                table.add_row(name, str(stats['count']), stats['table'])
            
            console.print(table)

        def search(model, **kwargs):
            """Generic search function for any model"""
            if isinstance(model, str):
                model = models.get(model)
            if not model:
                console.print("❌ Invalid model!", style="bold red")
                return
            
            try:
                results = model.objects.filter(**kwargs)
                console.print(f"🔍 Found {results.count()} results", style="bold green")
                return results
            except Exception as e:
                console.print(f"❌ Error: {str(e)}", style="bold red")

        return {
            'help': help,
            'inspect_model': inspect_model,
            'list_models': list_models,
            'search': search
        }

    def handle(self, *args, **options):
        console = Console()
        
        if not options['no_banner']:
            console.print(self.create_banner(console))

        # Get all models
        models = {model.__name__: model for model in apps.get_models()}
        
        # Create helper functions
        helpers = self.create_helper_functions(models, console)
        
        # Prepare namespace with models and helpers
        namespace = {**models, **helpers}
        
        # Welcome message
        console.print("\n🚀 Start typing queries! (type 'help()' for assistance)", style="bold blue")
        
        # Start REPL
        embed(globals=namespace, locals=namespace)
