
# dpe_xml_json.py
from django.conf import settings
import sys
import json
import os
import subprocess
    
def dpe_xml_to_json(data_xml):
    """Converti un XML en format JSon, compatible open3cl

    Args:
        data_xml (_type_): chaine de texte xml du DPE

    Returns:
        _type_: chaine de texte JSON du DPE, compatible open3cl
    """
    
    if not data_xml:
        print (f'Erreur dpe_xml_to_json : contenur XML vide')
        return None
    
    # conversion du fichier xml en json en utilisant le script nodejs d'opel3cl, contenu xml envoyé en STDIN
    try:
        # Écrire les données JSON dans le fichier temporaire
        script_path = os.path.join(settings.OPEN3CL_DIR, 'test', 'xml_to_json.js')
        if not os.path.isfile(script_path):
            print (f'Script Open3CL xml_to_jsonnon non trouvé : {script_path}')
            return None
        
        process = subprocess.Popen(
            ['node', script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(input=data_xml.encode('utf-8'), timeout=30)
        
        # décodaage du contenu et retourne le contenu json
        json_content = stdout.decode('utf-8')
        
        if json_content:
            return json_content
        else :
            print (f'Erreur xml_to_json a retourné une chaine vide {stderr}')
    # appel à dpe_file_xml_to_json ou autre
    except Exception as e:
        print(f"❌ Erreur dpe_xml_to_json : {e}")
        return None

    return None

def dpe_file_xml_to_json(xml_path):
    if not os.path.isfile(xml_path):
        print (f'fichier XML non trouvé : {xml_path}')
        return None
    with open(xml_path, 'r', encoding='utf-8') as f:
        xml_content = f.read()
        jsoncontent = dpe_xml_to_json(xml_content)
        
        return jsoncontent
    
    return None