# dpe/management/commands/import_dpe.py

import json
from pathlib import Path
from django.core.management.base import BaseCommand
from dpe.utils.dpe_xml_json import dpe_file_xml_to_json
from dpe.utils.dpe_db_json import dpe_db_to_json
from dpe.utils.dpe_analyse import DPEMoteurAnalyse


class TerminalColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'

class Command(BaseCommand):
    help = "Importe un fichier XML DPE dans la base existante"

    def add_arguments(self, parser):

        parser.add_argument("ademe", type=str, help="Chemin vers la base ADEME PostgreSQL ou SQLite")

    def handle(self, *args, **options):
        ademe = Path(options["ademe"])

        # 3. DB → JSON
        print(f"{TerminalColor.OKCYAN}📥 Extraction JSON depuis la base...{TerminalColor.ENDC}")
        json2_content = dpe_db_to_json(ademe)
        dpe = DPEMoteurAnalyse(json2_content)
        dpe.add_connaissance("Demandeur", "Demandeur", "Ligne de commande")
        result = dpe.execute_analyse()
            
        print(dpe.to_json())
