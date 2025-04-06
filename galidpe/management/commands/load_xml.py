# dpe/management/commands/load_xml.py

from django.core.management.base import BaseCommand
from dpe.utils.load_xml import import_dpe_json
from dpe.utils.dpe import file_xml_to_json
from dpe.utils.export_dpe_json import export_dpe
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
        
        json_content = file_xml_to_json(xml_path)
        import_dpe_json(json_content, ademe)
        
        anomalies = export_dpe(ademe)
        
        
        
