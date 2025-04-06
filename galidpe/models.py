from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models

# Create your models here.
########################### A ajouter car pas dans la base d'origine Ademe
class GaliDpeDiagnostiqueur(models.Model):
    usr_logiciel_id = models.CharField(max_length=100, blank=True, null=True)
    version_logiciel = models.CharField(max_length=100, blank=True, null=True)
    version_moteur_calcul = models.CharField(max_length=100, blank=True, null=True)
    nom_diagnostiqueur = models.CharField(max_length=100, blank=True, null=True)
    prenom_diagnostiqueur = models.CharField(max_length=100, blank=True, null=True)
    mail_diagnostiqueur = models.CharField(max_length=100, blank=True, null=True)
    telephone_diagnostiqueur = models.CharField(max_length=100, blank=True, null=True)
    adresse_diagnostiqueur = models.CharField(max_length=100, blank=True, null=True)
    entreprise_diagnostiqueur = models.CharField(max_length=100, blank=True, null=True)
    numero_certification_diagnostiqueur =models.CharField(max_length=100, blank=True, null=True)
    organisme_certificateur = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'galidpe_diagnostiqueur'




class GaliDpeInfo(models.Model):
    dpe_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    ademe = models.CharField(max_length=13, blank=True, null=True, db_index=True, unique=True)
    date_etablissement_dpe = models.DateTimeField(blank=True, null=True, db_index=True)
    ug = models.CharField(max_length=100, blank=True, null=True, db_index=True, db_comment="Identifiant de gestion")

    surface_habitable_logement = models.FloatField(blank=True, null=True)
    conso_val = models.FloatField(blank=True, null=True)
    ges_val = models.FloatField(blank=True, null=True)
    conso_lettre = models.CharField(max_length=1, blank=True, null=True)
    ges_lettre = models.CharField(max_length=1, blank=True, null=True)
    classe = models.CharField(max_length=1, blank=True, null=True)

    adresse = models.CharField(max_length=255, blank=True, null=True)
    cp = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=255, blank=True, null=True)

    depot_source = models.CharField(max_length=1000, blank=True, null=True, db_comment="Chemin d'origine du DPE")

    diagnostiqueur = models.ForeignKey('GaliDpeDiagnostiqueur', models.SET_NULL, null=True, blank=True)
    commentaire_travaux = models.CharField(max_length=1000, blank=True, null=True)

    # Champ full-text
    tsv = SearchVectorField(null=True, editable=False)  # indexé en GIN via Meta.indexes

    class Meta:
        managed = True
        db_table = 'galidpe_info'
        indexes = [
            GinIndex(fields=["tsv"], name="idx_galidpeinfo_tsv"),
        ]

        
class GaliDpeAnalyse(models.Model):
    ademe = models.CharField(max_length=13, blank=True, null=True, db_index=True, unique=True)

    version_analyse = models.IntegerField(db_index=True, db_comment="Version du moteur d'analyse")
    commentaires = models.JSONField(blank=True, null=True)
    anomalies = models.JSONField(blank=True, null=True)
    erreurs = models.JSONField(blank=True, null=True)
    connaissances = models.JSONField(blank=True, null=True)
    
    classification = models.CharField(max_length=100, blank=True, null=True, db_index=True, db_comment="Classification manuelle")
    a_ignorer = models.BooleanField(default=False, db_index=True, db_comment="Ignorer ce DPE")
    
    precision_min = models.FloatField(null=True, blank=True)
    precision_avg = models.FloatField(null=True, blank=True)
    precision_max = models.FloatField(null=True, blank=True)
    incoherence_min = models.FloatField(null=True, blank=True)
    incoherence_avg = models.FloatField(null=True, blank=True)
    incoherence_max = models.FloatField(null=True, blank=True)
    fiabilite_admin_min = models.FloatField(null=True, blank=True)
    fiabilite_admin_avg = models.FloatField(null=True, blank=True)
    fiabilite_admin_max = models.FloatField(null=True, blank=True)
    severite_max = models.IntegerField(db_index=True, null=True, blank=True)
    a_corriger = models.BooleanField(default=False, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = True
        db_table = 'galidpe_analyse'
    
class GaliDpeJson(models.Model):
    dpe_info = models.ForeignKey(GaliDpeInfo, models.CASCADE, db_index=True,  null=True, blank=True)
    dpe_id =  models.CharField(max_length=100, blank=True, null=True, db_index=True)
    ademe =  models.CharField(max_length=100, blank=True, null=True, db_index=True)
    version = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    json = models.JSONField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = True
        db_table = 'galidpe_json'