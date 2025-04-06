import sys
import json
import subprocess
import os
import shutil
import time
from datetime import datetime, timedelta
import tempfile
from django.utils import timezone
from django.conf import settings
import logging
# Configurer le logger pour Django
logger = logging.getLogger(__name__)

def executer_moteur_dpe(dpe_data):
    """
    Exécute le script open3cl_run.js pour analyser le contenu json du dpe.
    copie le fichier open3cl_run.js dans le dossier Open3cl si besoin.
    """
    # Chemin cible vers le fichier dans le répertoire de build
    script_path = os.path.join(settings.OPEN3CL_DIR, 'test', 'open3cl_run.js')

    # Replacer le fichier si DEBUG
    if settings.DEBUG and os.path.isfile(script_path):
        os.remove(script_path)

    # Si le fichier n'existe pas encore, on le copie depuis le dossier du script Python
    if not os.path.isfile(script_path):
        current_path = os.path.dirname(os.path.abspath(__file__))  # dossier du fichier Python actuel
        src_file = os.path.join(current_path, 'open3cl_run.js')
        shutil.copyfile(src_file, script_path)
    
    
    process = subprocess.Popen(
        ['node', script_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate(input=dpe_data.encode('utf-8'), timeout=30)
    
    # décodaage du contenu et retourne le contenu json
    json_content = stdout.decode('utf-8')

    return stdout.decode('utf-8'), stderr.decode('utf-8'), process.returncode

