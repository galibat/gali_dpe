import inspect
import json
import os
import time
from datetime import datetime
#from typing import List, Dict, Any

from dpe.utils.dpe import get_float, get_int, get_text, get_date, sha256_file_hex, find_all_elements, delete_dpe, to_date, get_bool, get_nested, dpe_conso_lettre
from dpe.models import *

from django.forms.models import model_to_dict
from dpe.serializers import DpeAnomalieSerializer, DpeAnalyseSerializer

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
        self.dpe_id = None
        self.ademe = ademe
        self.connaissances = {}
        self.anomalies = []
        self.erreurs = []
        self.analyse = None

    def to_dict(self):
        return {
            'ademe': self.ademe,
            'dpe_id': self.dpe_id,
            'connaissances': self.connaissances,
            'analyse': DpeAnalyseSerializer(self.dpe_analyse).data if self.dpe_analyse else None,
            'anomalies': DpeAnomalieSerializer(self.anomalies, many=True).data if self.anomalies else None,
            'erreurs': self.erreurs,
        }

    def add_connaissance(self, code, titre, valeur1, valeur2=None) :
        info = {"titre" : titre, "valeur1" : valeur1, "valeur2":valeur2  }
        self.connaissances[code] = info

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False, default=str)
    
    def load_analyse_from_db (self):
      self.anomalies = []
      self.dpe_analyse = DpeAnalyse.objects.filter(ademe=self.ademe).first()
      if self.dpe_analyse:
          self.dpe_anomalies = DpeAnomalie.objects.filter(analyse_id=self.dpe_analyse)
          for dpe_anomalie in self.dpe_anomalies:
              self.anomalies.append(dpe_anomalie)
              
    def delete_analyse_in_db (self):
        if self.ademe:
            analyses = DpeAnalyse.objects.filter(ademe=self.ademe)
            for analyse in analyses:
                DpeAnomalie.objects.filter(analyse_id=analyse).delete()
                analyse.delete()

    def create_analyse_db(self):
        """_summary_
        Créer une analyse vide en base de donnée et retourne son id.
        """
        self.dpe_analyse = None
        if self.ademe:
            self.dpe_id = get_text(self.dpe, 'id')
            self.dpe_analyse = DpeAnalyse(
                dpe_id = Dpe(id=self.dpe_id),
                ademe = self.ademe,
                version_analyse = get_version_analyse()
            )
            self.dpe_analyse.save()
            return str(self.dpe_analyse.id)
        else :
            return None
    
    def add_anomalie(self, datas):
        """Ajoute une analyse à la db
        Args:
            datas (_type_): _description_
        """
        

        if not self.dpe_analyse:
            print ("dpe_analyse vide")
            return

        anomalie = DpeAnomalie(analyse_id=self.dpe_analyse)

        # On parcourt les champs du modèle sauf la clé primaire
        for field in DpeAnomalie._meta.get_fields():
            name = field.name
            if name == "analyse_id":
                continue  # Déjà défini via analyse_id

            # Vérifie si le champ est présent dans datas (dict ou objet)
            if isinstance(datas, dict) and name in datas:
                setattr(anomalie, name, datas[name])
            elif hasattr(datas, name):
                setattr(anomalie, name, getattr(datas, name))
        anomalie.save()
        self.anomalies.append(anomalie)
        
    def execute_analyse(self) :
        
        self.erreurs = []
        self.anomalies = []
        # vérification des données d'entrée
        if not self.connaissances:
            self.connaissances = {}

        if isinstance(self.dpe, str):
            try:
                self.dpe = json.loads(self.dpe)
            except json.JSONDecodeError as e:
                print(f"Erreur de décodage JSON : {e}")
                return None
    
        if not self.dpe:
            self.erreurs.append('Pas de DPE fourni')
            return None
            
        if not self.ademe:
            self.ademe = get_text(self.dpe, 'identifiant_dpe')
        
        if not self.ademe:
            self.erreurs.append("Impossible de trouver le numéro ademe")
            return None
        
        print (f'Analyse du DPE {self.ademe}')
        
        # préparation de la sauvegarde
        self.delete_analyse_in_db()
        if not self.create_analyse_db():
            self.erreurs.append("Erreur lors de la création de l'analyse en db")
            return None
        
        # Trouver toutes les fonctions qui commencent par "check_" et les executer
        for name in sorted(dir(self)):
            if name.startswith("check_") and callable(getattr(self, name)):
                method = getattr(self, name)
                try:
                    result = method()
                    if result:
                        if isinstance(result, list):
                            for anomalie in result:
                                self.add_anomalie(anomalie)
                        else:
                            self.add_anomalie(result)
                except Exception as e:
                    self.erreurs.append(f"{name} → {str(e)}")
        
      
        return self.anomalies            

 
    
    # Contrôles administratif
    def check_admin_date_etablissement_dpe(self):
        value = get_text(self.dpe, 'administratif.date_etablissement_dpe')
        if value is None:
            return {
                "code": "DATE_ETABLISSEMENT_OK",
                "titre": "La date d'établissement est valide",
                "commentaire": f"administratif.diagnostiqueur.numero_certification_diagnostiqueur est vide",
                "incoherence": 0.6,
                "severite": 4
            }
        else :
            return {
                "code": "DATE_ETABLISSEMENT_OK",
                "titre": "La date d'établissement est valide",
                "commentaire": f"Date établissement = {value}",
                "severite": 1
            }
            
    def check_admin_diagnostiqueur_numero_certification(self):
        value = get_text(self.dpe, 'administratif.diagnostiqueur.numero_certification_diagnostiqueur')
        if value is None:
            return {
                "code": "DIAGNOSTIQUEUR_CERTIF_VIDE",
                "titre": "Le numero de certification du diagnostiqueur n'est pas indiqué",
                "commentaire": f"administratif.diagnostiqueur.numero_certification_diagnostiqueur est vide",
                "incoherence": 0.6,
                "severite": 4
            }
        else :
            return {
                "code": "DIAGNOSTIQUEUR_CERTIF_OK",
                "titre": "Le numero de certification du diagnostiqueur est indiqué",
                "commentaire": f"Numéro de certification = {value}",
                "severite": 1
            }
            
    # Contrôles description batiment
    def check_batiment_surface(self):
        value = get_float(self.dpe, 'logement.caracteristique_generale.surface_habitable_logement')
        if value is None:
            return {
                "code": "SURFACE_VIDE",
                "titre": "Surface habitable absente",
                "commentaire": f"logement.caracteristique_generale.surface_habitable_logement est vide",
                "incoherence": 0.6,
                "severite": 4
            }
        elif value < 9:
            return {
                "code": "SURFACE_FAIBLE",
                "titre": "Surface habitable très faible",
                "commentaire": f"Surface mesurée = {value}",
                "incoherence": 0.9,
                "severite": 4
            }
        elif value > 1000:
            return {
                "code": "SURFACE_ABERRANTE",
                "titre": "Surface anormalement élevée",
                "commentaire": f"Surface mesurée = {value}",
                "incoherence": 0.1,
                "severite": 2
            }
        else : 
            return {
                "code": "SURFACE_OK",
                "titre": "Surface habitable valide",
                "commentaire": f"Surface habitable = {value}",
                "severite": 1
            }
    
 
    

    

    
    
    
    