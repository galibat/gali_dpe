# core/management/commands/reset_managed_tables.py

from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection

class Command(BaseCommand):
    help = "Supprime et recrée toutes les tables Django managées dans la base courante"

    def handle(self, *args, **kwargs):
        models = [m for m in apps.get_models() if m._meta.managed]
        with connection.cursor() as cursor:
            self.stdout.write("Suppression des tables managées...")
            for model in reversed(models):
                table = model._meta.db_table
                cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE;')
                self.stdout.write(f"  ↳ {table} supprimée.")
        self.stdout.write("Tables supprimées. Recréez-les avec : python manage.py migrate")
