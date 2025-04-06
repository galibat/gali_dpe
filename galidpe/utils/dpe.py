# utils/xml_utils.py
import decimal
import hashlib
import json
from decimal import Decimal
from datetime import date, datetime, time
from django.utils import timezone
from dpe.models import *
import hashlib
from pathlib import Path
from django.utils.dateparse import parse_date
from django.db.models import ForeignKey, OneToOneField
from django.db import transaction
import logging



logger = logging.getLogger("dpe")
logging.basicConfig(level=logging.INFO)

def get_nested(data, path, default=None):
    """
    Recherche la valeur dans un dictionnaire JSON en suivant un chemin
    'foo.bar.baz', renvoie default si absent.
    """
    if not data:
        return None

    keys = path.split('.')
    cur = data
    for k in keys:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def get_text(data, path, max_length=None, default=None):
    val = get_nested(data, path, default=None)
    if val is None:
        return default
    val_str = str(val)[:max_length] if max_length else str(val)
    if val_str == "{'@xsi:nil': 'true'}" : return None
    return val_str

def get_bool(data, path, default=None):
    val = get_nested(data, path, default=None)
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default
    
def get_int(data, path, default=None):
    val = get_nested(data, path, default=None)
    if val is None:
        return default
    try:
        return int(val)
    except (ValueError, TypeError):
        return default


def get_float(data, path, default=None):
    val = get_nested(data, path, default=None)
    try:
        return float(val)
    except (ValueError, TypeError):
        return default


def get_date(data, path, default=None):
    """
    Tente de parser au format YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS.
    """
    val = get_text(data, path, default=None)
    if not val:
        return default
    try:
        return to_date(val)  # django.utils.dateparse
    except ValueError:
        return default


def find_all_elements(data, path):
    """
    Renvoie une liste d'éléments (dictionnaires) dans le JSON.
    Par ex: find_all_elements(data, 'logement.enveloppe.mur_collection.mur')
    retourne la liste data['dpe']['logement']['enveloppe']['mur_collection']['mur']
    si c'est une liste. Sinon, retourne [].
    """
    lst = get_nested(data, path, default=[])
    if isinstance(lst, dict):
        # si c'est un dict, on considère qu'il n'y a qu'un seul élément => le mettre dans une liste
        return [lst]
    if not isinstance(lst, list):
        return []
    return lst


def sha256_file_hex(filepath):
    """
    Exemple de fonction de hachage si on souhaite
    reproduire le même comportement que xml
    """
    if not filepath:
        return None
    p = Path(filepath)
    if not p.is_file():
        return None
    hasher = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()



# chemin : utils/conversion.py

from datetime import datetime, time
from django.utils import timezone

def to_date(text):
    """
    Convertit une chaîne de date (ou datetime) en datetime timezone-aware pour Django.
    Accepte formats simples : 'YYYY-MM-DD', 'YYYY-MM-DD HH:MM:SS', ISO.
    """
    if not text:
        return None

    text = text.strip()
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(text, fmt)
            if fmt == "%Y-%m-%d":
                dt = datetime.combine(dt.date(), time.min)

            # Si la datetime est naïve → timezone-aware
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt, timezone.get_current_timezone())

            return dt
        except ValueError:
            continue

    return None


# EXPORT JSON
from datetime import date, datetime
from decimal import Decimal

def date_json(d):  # ou ton format personnalisé
    return d.strftime("%Y-%m-%d")

def datetime_json(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def clean_and_serialize(obj, parent_key=None):
    if isinstance(obj, dict):
        cleaned = {}
        for k, v in obj.items():
            new_val = clean_and_serialize(v, parent_key=k)
            # On ne supprime que None et les dictionnaires vides, 
            # mais on conserve les listes vides.
            if new_val not in [None, {}]:
                # Forcer string pour les clés enum_
                if k.startswith("enum_"):
                    cleaned[k] = str(new_val)
                else:
                    cleaned[k] = new_val
        return cleaned

    elif isinstance(obj, list):
        return [clean_and_serialize(item, parent_key=parent_key) for item in obj if item is not None]

    else:
        # Feuille : conversion par type
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return datetime_json(obj)
        if isinstance(obj, date):
            return date_json(obj)
        return obj

def to_dpe_json(dpe_data):
    cleaned_data = clean_and_serialize(dpe_data)
    return json.dumps(cleaned_data, ensure_ascii=False, indent=2)


  



# chemin : utils/deletion.py

# chemin : utils/deletion.py

# chemin : utils/deletion.py

from django.db.models import ForeignKey, OneToOneField
from django.db import transaction

def delete_with_dependents(obj, _visited=None, _level=0, logger=None):
    """
    Supprime récursivement un objet Django et ses dépendances liées via FK/OneToOneField.
    
    Paramètres :
    - obj : instance Django à supprimer
    - _visited : ensemble des objets déjà traités
    - _level : profondeur d'appel récursif (pour indentation)
    - logger : instance logging.Logger ou None (par défaut = silencieux)
    """
    indent = "  " * _level
    def log(msg): 
        if logger:
            logger.info(msg)

    if _visited is None:
        _visited = set()

    key = (obj.__class__, obj.pk)
    if key in _visited or obj.pk is None:
        log(f"{indent}⏩ Déjà visité ou sans PK : {obj.__class__.__name__} ({obj.pk})")
        return
    _visited.add(key)

    log(f"{indent}🔍 Analyse de : {obj.__class__.__name__} ({obj.pk})")

    for rel in obj._meta.related_objects:
        if not isinstance(rel.field, (ForeignKey, OneToOneField)):
            continue

        accessor_name = rel.get_accessor_name()
        related = getattr(obj, accessor_name, None)

        if related is None:
            continue

        rel_model = rel.related_model.__name__
        log(f"{indent}→ Relation : {rel_model}.{rel.field.name} ({'OneToOne' if rel.one_to_one else 'ForeignKey'})")

        if not rel.one_to_many:
            if related.pk:
                log(f"{indent}  ↪ Objet lié trouvé : {related.__class__.__name__} ({related.pk})")
                delete_with_dependents(related, _visited, _level + 1, logger)
        else:
            related_set = list(related.all())
            log(f"{indent}  ↪ {len(related_set)} objet(s) lié(s) trouvé(s)")
            for related_obj in related_set:
                delete_with_dependents(related_obj, _visited, _level + 1, logger)

    log(f"{indent}🗑️ Suppression de : {obj.__class__.__name__} ({obj.pk})")
    obj.delete()

    
def delete_dpe(ademe):
    """Effacer un DPE et ses données liés dans les autres tables."""
    list_dpe = Dpe.objects.filter(identifiant_dpe=ademe)

    for dpe in list_dpe:
        with transaction.atomic():
            print (f'Effacement DPE  {ademe}')
            delete_with_dependents(dpe, logger=None)
    return
    list_dpe = Dpe.objects.filter(identifiant_dpe=ademe)

    for dpe in list_dpe:
        dpe.delete()
        adm = DpeAdministratif.objects.filter(dpe_id=dpe).first()
        if adm:
            geolocalisation = DpeGeolocalisation.objects.filter(administratif=adm).first()
            if geolocalisation:
                geolocalisation.delete()
                DpeTAdresse.objects.filter(id=geolocalisation.adresse_bien.id).delete()
            adm.delete()
        
        DpeCaracteristiqueGenerale.objects.filter(dpe_id=dpe).delete()
        
        DpeInfos.objects.filter(dpe_id=dpe).delete()

        DpeInertie.objects.filter(dpe_id=dpe).delete()
        
        DpeMur.objects.filter(dpe_id=dpe).delete()
        
        # Suppression du DPE lui-même
#        if dpe.id != '3fdd7a1d-ac2f-4266-aa2f-923612803849':
        
        
def dpe_conso_lettre(DPE_index, surface = 40):
    if not isinstance(DPE_index, (decimal.Decimal, float, int)):
        try:
            # Convertir le paramètre 'DPE_index' en Decimal s'il est une chaîne
            DPE_index = DPE_index.replace(',', '.')  # Remplacer la virgule par un point si nécessaire
            DPE_index = decimal.Decimal(DPE_index)
        except:
            return 'N'
    
    if DPE_index == 0:
        return 'N'
    if DPE_index <= 70:
        return 'A'
    elif DPE_index <= 110:
        return 'B'
    elif DPE_index <= 180:
        return 'C'
    elif DPE_index <= 250:
        return 'D'
    elif DPE_index <= 330:
        return 'E'
    elif DPE_index <= 420:
        return 'F'
    else:
        return 'G'
    
def dpe_ges_lettre(DPE_index, surface = 40):
    if not isinstance(DPE_index, (decimal.Decimal, float, int)):
        try:
            # Convertir le paramètre 'DPE_index' en Decimal s'il est une chaîne
            DPE_index = DPE_index.replace(',', '.')  # Remplacer la virgule par un point si nécessaire
            DPE_index = decimal.Decimal(DPE_index)
        except:
            return 'N'
    if DPE_index == 0:
        return 'N'

    if DPE_index <= 6:
        return 'A'
    elif DPE_index <= 11:
        return 'B'
    elif DPE_index <= 30:
        return 'C'
    elif DPE_index <= 50:
        return 'D'
    elif DPE_index <= 70:
        return 'E'
    elif DPE_index <= 100:
        return 'F'
    else:
        return 'G'