# mongo_models.py

from mongoengine import Document, StringField, DictField, DateTimeField, IntField, FloatField, ListField, BooleanField, EmbeddedDocument, EmbeddedDocumentField, connect

class MG_DPE(Document):
    ademe = StringField(required=True, unique=True) # identifiant unique du DPE
    adresse = StringField(required=False) # adresse complete du logement
    code_postal = StringField()
    ville = StringField()
    reference = StringField(required=False) # reference du logement
    prorietaire = StringField(required=False) # reference du logement
    dpe_id = StringField(required=False) # identifiant du DPE dans la base ADEME
    donnees = DictField(required=True) # données du DPE
    infos = DictField(required=True) # informations supplémentaires sur le DPE

    meta = {
        'collection': 'dpe',
        'indexes': [
            {'fields': ['ademe'], 'unique': True},
            {'fields': ['code_postal']},
            {'fields': ['ville']},
            {'fields': ['dpe_id'], 'unique': False},
            {'fields': ['reference'], 'unique': False},
            {'fields': ['prorietaire'], 'unique': False},
            {'fields': ['adresse'], 'default_language': 'french'},  # index full-text
        ]
    }

class MG_TravauxResult(Document):
    ademe = StringField(required=True, unique=True) # identifiant unique du DPE
    model_travaux = StringField(required=False) # modèle de travaux
    inputs = DictField(required=False) # données d'entrée pour le modèle de travaux
    results = DictField(required=False) # résultats du modèle de travaux
    date_analyse = DateTimeField(required=False) # date de l'analyse

    meta = {
        'collection': 'dpe',
        'indexes': [
            {'fields': ['ademe'], 'unique': True},
            {'fields': ['model_travaux'], 'unique': False},
            {'fields': ['date_analyse'], 'unique': False},
        ]
    }