# dpe_analyse.py
# Moteur d'analyse de fiabilité d'un DPE
# Utilise le DPE en format JSON2 en entrée
import inspect
import json
import os
import time
from datetime import datetime
#from typing import List, Dict, Any

from galidpe.utils.dpe import get_float, get_int, get_text, get_date, sha256_file_hex, find_all_elements, delete_dpe, to_date, get_bool, get_nested, dpe_conso_lettre
from galidpe.models import *
from dpe.models import *

from django.forms.models import model_to_dict
from galidpe.serializers import GaliDpeAnalyseSerializer

# severite : 
# 1 : Info : donne une information
# 2 : A vérifier
# 3  : Anomalie non critique
# 4  : Anomalie critique
# 5  : Urgent / invalide

def get_liste_controle ():
    return [
        {"code": "DIAGNOSTIQUEUR_CERTIF_VIDE", "titre": "Le numero de certification du diagnostiqueur n'est pas indiqué"},
        {"code": "DIAGNOSTIQUEUR_CERTIF_OK", "titre": "Le numero de certification du diagnostiqueur est indiqué"},
    ]

def get_version_analyse():
    # retourne la version du moteur d'analyse en utilisant la date de modification de ce fichier
    # Timestamp de référence : 1er juillet 2021 à minuit UTC
    reference_timestamp = datetime(2021, 7, 1, 0, 0).timestamp()
    chemin_fichier = __file__
    modif_timestamp = os.path.getmtime(chemin_fichier)
    version = int(modif_timestamp - reference_timestamp)
    return version

class DPEMoteurAnalyse:
    def __init__(self, dpe: dict, ademe: str = None):
        self.dpe = dpe
        self.ademe = ademe
        self.analyse = GaliDpeAnalyse(ademe = self.ademe,version_analyse = get_version_analyse())
        self.dpe_info = None

    def to_dict(self):
        return {
            'ademe': self.ademe,
            'dpe_info': GaliDpeInfo(self.dpe_info).data if self.dpe_info else None,
            'analyse': GaliDpeAnalyseSerializer(self.analyse).data if self.analyse else None,
            'dpe': self.dpe
        }
  
    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False, default=str)
 
    def add_anomalie(self, datas):
        if not self.analyse : 
            return
        if not self.analyse.anomalies:
            self.analyse.anomalies = []
        self.analyse.anomalies.append(datas)
    
    def add_commentaire(self, datas):
        if not self.analyse : 
            return
        if not self.analyse.commentaires:
            self.analyse.commentaires = []
        self.analyse.commentaires.append(datas)
    
    def add_erreur(self, datas):
        if not self.analyse : 
            return
        if not self.analyse.erreurs:
            self.analyse.erreurs = []
        self.analyse.erreurs.append(datas)

    def add_connaissance(self, code, titre, valeur1, valeur2=None) :
        if not self.analyse : 
            return
        if not self.analyse.connaissances:
            self.analyse.connaissances = {}
        info = {"titre" : titre, "valeur1" : valeur1, "valeur2":valeur2  }
        self.analyse.connaissances[code] = info

    
    def load_analyse_from_db (self):
      self.anomalies = []
      self.analyse = GaliDpeAnalyse.objects.filter(ademe=self.ademe).first()
              
    def delete_analyse_in_db (self):
        if self.ademe:
            GaliDpeAnalyse.objects.filter(ademe=self.ademe).delete()
        GaliDpeAnalyse.objects.filter(ademe=None).delete()

    def create_analyse_db(self):
        """_summary_
        Créer une analyse vide en base de donnée et retourne son id.
        """
        self.dpe_analyse = None
        if self.ademe:
            self.dpe_analyse = GaliDpeAnalyse(
                ademe = self.ademe,
                version_analyse = get_version_analyse()
            )
            self.dpe_analyse.save()
            return str(self.dpe_analyse.id)
        else :
            return None


    def execute_analyse(self) :
        if not self.analyse : 
            print("Erreur de structure lors de l'analyse")
            return
        
        # vérification des données d'entrée
        if not self.analyse.connaissances:
            self.analyse.connaissances = {}

        if isinstance(self.dpe, str):
            try:
                self.dpe = json.loads(self.dpe)
            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON : {e}")
                return None
    
        if not self.dpe:
            self.add_erreur('Pas de DPE fourni')
            return None
            
        if not self.ademe:
            self.ademe = get_text(self.dpe, 'identifiant_dpe')
        
        self.analyse.ademe = self.ademe
        if not self.ademe:
            self.add_erreur("Impossible de trouver le numéro ademe")
            return None
        
        print (f'Analyse du DPE {self.ademe}')
        
        # préparation de la sauvegarde
        self.delete_analyse_in_db()

        # Trouver toutes les fonctions qui commencent par "check_" et les executer
        for name in sorted(dir(self)):
            if name.startswith("check_") and callable(getattr(self, name)):
                method = getattr(self, name)
                try:
                    method()
                except Exception as e:
                    self.add_erreur(f"{name} → {str(e)}")
        
        self.analyse.save()
    
    # Contrôles administratif
    def check_admin_date_etablissement_dpe(self):
        value = get_text(self.dpe, 'administratif.date_etablissement_dpe')
        if value is None:
            self.add_anomalie({
                "code": "DE00",
                "titre": "La date d'établissement est vide",
                "commentaire": f"administratif.date_etablissement_dpe est vide",
                "incoherence": 0.6,
                "severite": 1
            })
        else :
            self.add_commentaire({
                "code": "DEOK",
                "titre": "La date d'établissement est valide",
                "commentaire": f"Date établissement = {value}",

            })
            
    # Contrôles description batiment
    def check_batiment_surface(self):
        value = get_float(self.dpe, 'logement.caracteristique_generale.surface_habitable_logement')
        if value is None:
            self.add_anomalie({
                "code": "SH00",
                "titre": "Surface habitable absente",
                "commentaire": f"logement.caracteristique_generale.surface_habitable_logement est vide",
                "incoherence": 0.6,
                "severite": 4
            })
        elif value < 9:
            self.add_anomalie({
                "code": "SHLO",
                "titre": "Surface habitable très faible",
                "commentaire": f"Surface mesurée = {value}. La surface d'un logement loué doit être >= 9 m²",
                "incoherence": 0.9,
                "severite": 4
            })
        elif value > 1000:
            self.add_anomalie({
                "code": "SHHI",
                "titre": "Surface anormalement élevée",
                "commentaire": f"Surface mesurée = {value}",
                "incoherence": 0.1,
                "severite": 2
            })
        else : 
            self.add_commentaire( {
                "code": "SHOK",
                "titre": "Surface habitable valide",
                "commentaire": f"Surface habitable = {value}",
            })
    
 
    

    

    
    
    
    