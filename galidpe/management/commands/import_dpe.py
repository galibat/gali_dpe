# dpe/management/commands/import_dpe.py

from django.core.management.base import BaseCommand
from dpe.import_dpe_xml import import_dpe
from pathlib import Path

class Command(BaseCommand):
    help = "Importe un fichier XML DPE dans la base existante"

    def add_arguments(self, parser):
        parser.add_argument("xml_file", type=str)
        parser.add_argument("ademe", type=str)

    def handle(self, *args, **options):
        xml_path = Path(options["xml_file"])
        ademe = Path(options["ademe"])
        if not xml_path.exists():
            self.stderr.write(f"Fichier non trouvé : {xml_path}")
            return

        
        import_dpe(xml_path, ademe)
        self.stdout.write(self.style.SUCCESS("Import terminé avec succès"))
    