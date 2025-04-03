# dpe/management/commands/import_dpe.py

from django.core.management.base import BaseCommand
from dpe.utils.export_dpe_json import export_dpe
from pathlib import Path

class Command(BaseCommand):
    help = "Exporte un DPE en json"

    def add_arguments(self, parser):
        parser.add_argument("ademe", type=str)

    def handle(self, *args, **options):
        ademe = Path(options["ademe"])
        
        print (export_dpe(ademe))
        
    