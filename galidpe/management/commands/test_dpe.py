# dpe/management/commands/import_dpe.py

import json
from pathlib import Path
from django.core.management.base import BaseCommand
from dpe.utils.dpe_xml_json import dpe_file_xml_to_json
from dpe.utils.dpe_json_db import dpe_json_to_db
from dpe.utils.dpe_db_json import dpe_db_to_json
from dpe.utils.open3cl import executer_moteur_dpe

def json_leaf_diff(d1, d2, path=""):
    """
    Compare deux structures JSON récursivement et retourne
    un dict des différences sur les feuilles uniquement.
    """
    diffs = {}

    if isinstance(d1, dict) and isinstance(d2, dict):
        keys = set(d1.keys()) | set(d2.keys())
        for key in keys:
            v1 = d1.get(key)
            v2 = d2.get(key)
            subpath = f"{path}.{key}" if path else key
            diffs.update(json_leaf_diff(v1, v2, subpath))
    elif isinstance(d1, list) and isinstance(d2, list):
        max_len = max(len(d1), len(d2))
        for i in range(max_len):
            try:
                v1 = d1[i]
            except IndexError:
                v1 = None
            try:
                v2 = d2[i]
            except IndexError:
                v2 = None
            subpath = f"{path}[{i}]"
            diffs.update(json_leaf_diff(v1, v2, subpath))
    elif d1 != d2:
        # On considère que ce sont des feuilles
        diffs[path] = {"old": d1, "new": d2}

    return diffs


def format_leaf_diff_text(d1, d2):
    """
    Retourne un texte décrivant les différences finales entre d1 et d2.
    Seules les feuilles dont la valeur change sont mentionnées.
    """
    diffs = json_leaf_diff(d1, d2)
    output_lines = []
    for key, diff in diffs.items():
        output_lines.append(f"Pour '{key}' : ancienne valeur = {diff['old']}, nouvelle valeur = {diff['new']}")
    return "\n".join(output_lines)

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
        parser.add_argument("xml_file", type=str, help="Chemin vers le fichier DPE XML")
        parser.add_argument("ademe", type=str, help="Chemin vers la base ADEME PostgreSQL ou SQLite")

    def handle(self, *args, **options):
        xml_path = Path(options["xml_file"])
        ademe = Path(options["ademe"])
        output_dir = xml_path.parent

        print(f"{TerminalColor.OKBLUE}🔍 Chargement du fichier XML : {xml_path}{TerminalColor.ENDC}")
        if not xml_path.exists():
            print(f"{TerminalColor.FAIL}❌ Fichier non trouvé : {xml_path}{TerminalColor.ENDC}")
            return

        # 1. XML → JSON
        print(f"{TerminalColor.OKCYAN}📤 Conversion XML → JSON...{TerminalColor.ENDC}")
        try:
            json1_content = dpe_file_xml_to_json(xml_path)
            (json1_moteur, msg_error, code_error) = executer_moteur_dpe(json1_content)
            if msg_error:
                print(f"{TerminalColor.FAIL}{msg_error}{TerminalColor.ENDC}")
            with open(output_dir / "json1_content-sortiemoteur.json", "w", encoding="utf-8") as f:
                f.write(json1_moteur)

            if isinstance(json1_content, str):
                json1_content = json.loads(json1_content)

            with open(output_dir / "json1_content-xml2json.json", "w", encoding="utf-8") as f:
                json.dump(json1_content, f, ensure_ascii=False, indent=2)
                
                
        except Exception as e:
            print(f"{TerminalColor.FAIL}❌ Erreur XML → JSON : {e}{TerminalColor.ENDC}")
            return

        # 2. Insertion dans la base
        print(f"{TerminalColor.OKCYAN}🛢️  Insertion en base de données...{TerminalColor.ENDC}")
        dpe_json_to_db(json1_content, ademe)

        # 3. DB → JSON
        print(f"{TerminalColor.OKCYAN}📥 Extraction JSON depuis la base...{TerminalColor.ENDC}")
        json2_content = dpe_db_to_json(ademe)

        with open(output_dir / "json2_content-dpe_db_to_json.json", "w", encoding="utf-8") as f:
            f.write(json2_content)
    
        # 4. Exécution du moteur
        print(f"{TerminalColor.OKCYAN}⚙️  Exécution du moteur DPE...{TerminalColor.ENDC}")
        (json2_moteur, msg_error, code_error) = executer_moteur_dpe(json2_content)
        if msg_error:
            print(f"{TerminalColor.FAIL}{msg_error}{TerminalColor.ENDC}")
            
        with open(output_dir / "json3_content-moteur.json", "w", encoding="utf-8") as f:
            f.write(json2_moteur)

