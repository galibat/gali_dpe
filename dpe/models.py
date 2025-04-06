# model de la base de donnée opendata de l'ademe, importée dans le serveur postgres.
# lancer le script dpe_import.py pour importer les données 
# lancer le script dpe_after.py pour adapter la base (création d'indexs, etc)
# -*- coding: utf-8 -*-

from django.db import models
import uuid

class Dpe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    date_etablissement_dpe = models.DateTimeField(blank=True, null=True)
    hashkey = models.CharField(max_length=255, blank=True, null=True)
    version = models.CharField(max_length=255)
    identifiant_dpe = models.CharField(max_length=13, blank=True, null=True)
    desactive = models.BooleanField(blank=True, null=True)
    ancien_dpe_id = models.OneToOneField('self', models.DO_NOTHING, blank=True, null=True, db_index=True, db_column='ancien_dpe_id')
    date_reception_dpe = models.DateTimeField(blank=True, null=True)
    dpe_xml_path = models.CharField(max_length=50, blank=True, null=True)
    version_moteur_used = models.CharField(max_length=32, blank=True, null=True)
    version_xsd_used = models.CharField(max_length=32, blank=True, null=True)
    statut = models.CharField(max_length=10, blank=True, null=True)
    is_dpe_2012 = models.BooleanField(null=True)
    dpe2012_donnees_id = models.UUIDField(blank=True, null=True)
    enum_type_energie_chauffage_principal_id = models.IntegerField(blank=True, null=True)
    enum_type_energie_ecs_principal_id = models.IntegerField(blank=True, null=True)
    xml_hash = models.TextField(blank=True, null=True)
    suppression_en_cours = models.BooleanField(null=True)
    dpe_remplacant_id = models.UUIDField(unique=True, blank=True, null=True)
    generateur_chauffage_principal_id = models.ForeignKey('DpeGenerateurChauffage', models.DO_NOTHING, blank=True, null=True, db_column='generateur_chauffage_principal_id')
    anonymise = models.BooleanField(null=True)
    migre_en_utc = models.BooleanField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(blank=True, null=True)
    generateur_ecs_principal_id = models.ForeignKey('DpeGenerateurEcs', models.DO_NOTHING, blank=True, null=True, db_column='generateur_ecs_principal_id')
    traite_petite_surface = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe'
        
class DpeTAdresse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    adresse_brut = models.CharField(null=True, max_length=255, db_comment=" modèle concerné : tous | description : champs texte brute de l'adresse saisi par le diagnostiqueur ")
    ban_city = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : tous | description : nom de la commune de l'adresse géocodée ban ")
    ban_citycode = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : tous | description : code insee de la commune de  l'adresse géocodée ban ")
    ban_date_appel = models.DateTimeField(blank=True, null=True, db_comment=" modèle concerné : tous | description : date d'appel à la ban ")
    ban_housenumber = models.CharField(max_length=255, blank=True, null=True, db_comment=' modèle concerné : tous | description : Numéro éventuel de l’adresse dans la voie (champ BAN) ')
    ban_id = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : tous | description : identifiant de la BAN referençant l'adresse ")
    ban_label = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : tous | description : label de l'adresse au format ban ")
    ban_postcode = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : tous | description : code postal de la commune de l'adresse géocodée ban ")
    ban_score = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : tous | description : score de match entre le label brut et le résultat de géocodage de la BAN ')
    ban_street = models.CharField(max_length=255, blank=True, null=True, db_comment=' modèle concerné : tous | description : Nom de la voie en minuscules accentuées avec les noms alternatifs éventuels (champ BAN) ')
    ban_type = models.CharField(max_length=255, blank=True, null=True, db_comment=' modèle concerné : tous | description : type de résultat ban :  housenumber/street/locality/municipality ')
    ban_x = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : tous | description : coordonnée x du géolocalisant ban dans le referentiel epsg 2154 lambert 93 ')
    ban_y = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : tous | description : coordonnée x du géolocalisant ban dans le referentiel epsg 2154 lambert 93 ')
    code_postal_brut = models.CharField(null=True, max_length=255, db_comment=" modèle concerné : tous | description : code postal de l'adresse brute saisie par le diagnostiqueur ")
    compl_etage_appartement = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : tous | description : complement d'adresses : etage du logement (cas de l'appartement) sous format entier 0 =RDC  ")
    compl_nom_residence = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : tous | description : complement d'adresses : nom de la residence ")
    compl_ref_batiment = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : tous | description : complement d'adresse : référence du bâtiment ( ex. A,B ,1,2,3,4) ")
    compl_ref_cage_escalier = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : tous | description : complement d'adresses : reference de cage d'escalire ")
    compl_ref_logement = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : tous | description : complement d'adresses : reference du  logement dans le bâtiment  (appartement ex. 10, A13,  3eme gauche) ")
    enum_statut_geocodage_ban_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : tous | description : statut de l'appareillement à la BAN de l'adresse ")
    label_brut = models.CharField(null=True, max_length=255, db_comment=" modèle concerné : tous | description : label complet de l'adresse saisie par le diagnostiqueur (adresse + code postal + nom commune) ")
    nom_commune_brut = models.CharField(null=True, max_length=255, db_comment=' modèle concerné : tous | description : nom de commune brute saisie par le diagnostiqueur ')
    ban_departement = models.CharField(null=True, max_length=255, blank=True)
    ban_erreur = models.BooleanField(null=True)
    ban_region = models.CharField(max_length=255, blank=True, null=True)
    traite_par_batch = models.BooleanField(null=True)
    ban_epci = models.CharField(max_length=255, blank=True, null=True)
    label_brut_avec_complement = models.CharField(max_length=255, blank=True, null=True)
    migre_en_utc = models.BooleanField(null=True)
    date_derniere_modification = models.DateTimeField(null=True)
    is_dpe_2012 = models.BooleanField(null=True)
    ban_id_ban_adresse = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dpe_t_adresse'
        
class CompteurImportDpeCertificat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    numero_certificat = models.TextField(blank=True, null=True)
    nombre_dpe_importes = models.BigIntegerField(null=True)
    alerte_envoyee = models.BooleanField(null=True)
    id_utilisateur_diagnostiqueur = models.UUIDField(blank=True, null=True)
    id_utilisateur_organisme_certificateur = models.UUIDField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compteur_import_dpe_certificat'
        unique_together = (('numero_certificat', 'id_utilisateur_diagnostiqueur', 'id_utilisateur_organisme_certificateur'),)


class DemandeTelechargementAttestation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    id_organisme = models.UUIDField(blank=True, null=True,)
    date_demande = models.DateTimeField(blank=True, null=True)
    date_telechargement = models.DateTimeField(blank=True, null=True)
    statut_telechargement = models.BooleanField(null=True)
    fichier_supprime = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'demande_telechargement_attestation'





class Dpe2012EnumMethodeDpe(models.Model):
    id = models.IntegerField(primary_key=True)
    lib = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'dpe2012_enum_methode_dpe'


class Dpe2012EnumModeleDpe(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(unique=True, max_length=10)
    tr001_modele_dpe_type_id = models.IntegerField()
    modele = models.CharField(blank=True, null=True,max_length=50)
    description = models.CharField(blank=True, null=True,max_length=200)
    fichier_vierge = models.CharField(blank=True, null=True,max_length=50)
    est_efface = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe2012_enum_modele_dpe'


class Dpe2012EnumTypeBatiment(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    libelle = models.CharField(max_length=100)
    est_efface = models.IntegerField()
    ordre = models.IntegerField()
    simulateur = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dpe2012_enum_type_batiment'


class Dpe2012EnumTypeEnergie(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    est_efface = models.IntegerField()
    simu_ordre = models.IntegerField(blank=True, null=True)
    simulateur = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'dpe2012_enum_type_energie'


class DpeAdministratif(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True, related_name='dpeadministratif')
    date_etablissement_dpe = models.DateTimeField(db_comment=" modèle concerné : tous | description : date de l'établissement du dpe ")
    date_visite_diagnostiqueur = models.DateTimeField(db_comment=' modèle concerné : tous | description : date de visite du diagnostiqueur ')
    enum_modele_dpe_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : tous | description : modèle de dpe (3CL logement / tertiaire ou neuf) ')
    dpe_a_remplacer = models.CharField(max_length=13, blank=True, null=True, db_comment=" modèle concerné : tous | description : numéro du DPE à remplacer dans le cas d'une opération de remplacement du DPE ")
    motif_remplacement = models.TextField(blank=True, null=True, db_comment=' modèle concerné : tous | description : motif du remplacement du DPE : texte libre ')
    date_fin_validite_dpe = models.DateTimeField(null=True)
    enum_version_id = models.CharField(max_length=50, blank=True, null=True, db_comment=' modèle concerné : tous | description : version du DPE. Pour gérer toute future évolution du dispositif et du modèle de données sous jacent (ex. modification des tv reseau de chaleur) ')
    dpe_immeuble_associe = models.CharField(max_length=13, blank=True, null=True, db_comment=" modèle concerné : tous | description : numéro du DPE immeuble associé au DPE logement utilisant la méthode de génération des DPE à l'appartement à partir du DPE immeuble ")
    reference_interne_projet = models.CharField(max_length=255, blank=True, null=True)
    migre_en_utc = models.BooleanField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)
    is_dpe_2012 = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_administratif'


class DpeApportEtBesoin(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    apport_interne_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description :  apports internes totaux durant la saison de chauffe Ai (kWh). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    apport_interne_fr = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description :  apports internes totaux durant la saison de froid Ai (kWh). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    apport_solaire_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : apports solaires totaux durant la saison de chauffe As (kWh). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    apport_solaire_fr = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : apports solaires totaux durant la saison de froid As (kWh). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    besoin_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : besoin de chauffage annuel total du logement ou immeuble (kWh) . Pour les DPE immeubles ces données sont à l'immeuble. Pour les dpe appartements à partir de l'immeuble ces données sont à l'appartement ")
    besoin_ch_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : besoin de chauffage total du bâtiment  pour le scénario dépensier  (kWh) (DH21). Pour les DPE immeubles ces données sont à l'immeuble. Pour les dpe appartements à partir de l'immeuble ces données sont à l'appartement ")
    besoin_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : besoin d'ecs annuel total du bâtiment (kWh). Pour les DPE immeubles ces données sont à l'immeuble. Pour les dpe appartements à partir de l'immeuble ces données sont à l'appartement ")
    besoin_ecs_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : besoin d'ecs total du bâtiment  pour le scénario dépensier  (kWh). Pour les DPE immeubles ces données sont à l'immeuble. Pour les dpe appartements à partir de l'immeuble ces données sont à l'appartement ")
    besoin_fr = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : besoin de refroidissement annuel (kWh).Pour les DPE immeubles ces données sont à l'immeuble. Pour les dpe appartements à partir de l'immeuble ces données sont à l'appartement ")
    besoin_fr_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : besoin de refroidissement annuel pour le scénario dépensier (kWh). Pour les DPE immeubles ces données sont à l'immeuble. Pour les dpe appartements à partir de l'immeuble ces données sont à l'appartement ")
    fraction_apport_gratuit_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : fraction des apports gratuits sur la saison de chauffe F. Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    fraction_apport_gratuit_depensier_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : fraction des apports gratuits sur la saison de chauffe F pour le scénario dépensier (DH21). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    nadeq = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : nombre d'adulte équivalent calculés pour le besoin d'ECS. Pour les DPE immeubles ces données sont à l'immeuble. Pour les dpe appartements à partir de l'immeuble ces données sont à l'appartement ")
    pertes_distribution_ecs_recup = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : pertes de distribution d'ECS récupérées(kWh). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    pertes_distribution_ecs_recup_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : pertes de distribution d'ECS récupérées(kWh) pour le scénario dépensier. Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    pertes_generateur_ch_recup = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : pertes des générateurs de chauffage récupérées(kWh). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    pertes_generateur_ch_recup_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : pertes des générateurs de chauffage récupérées(kWh) pour le scénario dépensier. Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    pertes_stockage_ecs_recup = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : pertes de stockage d'ECS récupérées(kWh). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    surface_sud_equivalente = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : surface sud équivalente. Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    v40_ecs_journalier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation en l d'ecs à 40°C sur une journée. Pour les DPE immeubles ces données sont à l'immeuble. Pour les dpe appartements à partir de l'immeuble ces données sont à l'appartement ")
    v40_ecs_journalier_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation en l d'ecs à 40°C sur une journée scénario dépensier. Pour les DPE immeubles ces données sont à l'immeuble. Pour les dpe appartements à partir de l'immeuble ces données sont à l'appartement ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_apport_et_besoin'


class DpeBaieEts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement | description : description textuelle de l'objet ")
    enum_inclinaison_vitrage_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : inclinaison du vitrage ')
    enum_orientation_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : orientation de la baie  ')
    nb_baie = models.FloatField(null=True, db_comment=' modèle concerné : logement | description : nombre de baies ')
    surface_totale_baie = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : surface totale de paroi vitrée pour  ce type de vitrage et sur cette orientation (nombre de baies x surface unitaire). La surface est la surface de la baie dans son ensemble. (vitrage + menuiserie inclus) ')
    ets_id = models.ForeignKey('DpeEts', models.DO_NOTHING, null=True, db_column='ets_id', db_index=True)
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_baie_ets'


class DpeBaieVitree(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    b = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coefficient de réduction des déperditions de la baie vitrée ')
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    double_fenetre = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : est ce qu'il s'agit d'une double fenetre. DANS LE CAS D'UNE DOUBLE FENETRE LES DONNEES DU MODELE SONT FOURNIES POUR LE VITRAGE LE PLUS PERFORMANT OU POUR LA BAIE DANS SON ENSEMBLE A L'EXCEPTION DE Uw2 ET Sw2 QUI SONT LES CARACTERISTIQUES DU DEUXIEME VITRAGE (le moins performant) 0 : non 1 : oui ")
    enum_cfg_isolation_lnc_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : configuration de l'adjacence avec local non chauffé :  local chauffé (non) isolé/local non chauffé (non) isolé/orientation véranda qui permet de calculer le b  ")
    enum_inclinaison_vitrage_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : inclinaison du vitrage ')
    enum_methode_saisie_perf_vitrage_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : methode de saisie des caractéristiques thermiques des vitrage (valeurs forfaitaires ou saisies en direct lorsque issu d'un justificatif) ")
    enum_orientation_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : orientation de la baie  ')
    enum_type_adjacence_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type d'adjacence de la paroi ")
    enum_type_baie_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : type de baie ')
    enum_type_fermeture_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : type de fermeture associé à la baie (volets/persiennes etc..) ')
    enum_type_gaz_lame_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : type de gaz présent dans la lame ')
    enum_type_materiaux_menuiserie_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : type de matériaux des menuiseries ')
    enum_type_vitrage_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : type de vitrage ')
    epaisseur_lame = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : epaisseur de la lame ')
    fe1 = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : fe1 facteur d'ensoleillement  calculé à partir de la table sur les masques proches ")
    fe2 = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : fe2 facteur d'ensoleillement calculé soit à l'aide de la méthode masque lointain homogène ou méthode des masques lointains proches ")
    largeur_dormant = models.FloatField(blank=True, null=True)
    nb_baie = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : nombre de baies ')
    presence_retour_isolation = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : y a-t-il un retour d'isolant de la paroi opaque sur la baie 0 : non 1 : oui ")
    surface_aiu = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : surface aiu : surface des parois du local non chauffé qui donnent sur des locaux chauffés. ')
    surface_aue = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface aue : surface des parois du local non chauffé en contact avec l'extérieur ou le sol ")
    surface_totale_baie = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : surface totale de paroi vitrée pour  ce type de vitrage et sur cette orientation (nombre de baies x surface unitaire). La surface est la surface de la baie dans son ensemble. (vitrage + menuiserie inclus) ')
    sw = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : sw final de la baie: soit saisi directement soit issu des tables forfaitaires ')
    sw_1 = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : Sw de la première fenêtre dans le cas d'une double fenêtre (par défaut la première fenêtre est toujours celle avec le Uw le plus élevé -> plus performante)  ")
    sw_2 = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : Sw de la deuxième fenêtre dans le cas d'une double fenêtre (par défaut la deuxième fenêtre est toujours celle avec le Uw le plus faible -> moins performante)  ")
    sw_saisi = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : facteur solaire de la baie saisi directement (nécessite une justification) ')
    tv_coef_masque_lointain_homogene_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de masque homogène lointain ')
    tv_coef_masque_proche_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficent de masque proche ')
    tv_coef_orientation_id = models.IntegerField(blank=True, null=True)
    tv_coef_reduction_deperdition_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de reduction des deperditions ')
    tv_deltar_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du delta de resistance de la protection mobile. (volets persienne etc..) ')
    tv_sw_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du facteur solaire de la baie sw ')
    tv_ug_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficent de transmission thermique du vitrage ug ')
    tv_ujn_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de transmissiion de la baie jour/nuit Ujn. Dans le cas d'une interpolation/extrapolation prendre la valeur tabulée la plus proche ")
    tv_uw_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficent de transmission thermique de la baie uw. Dans le cas d'une interpolation/extrapolation prendre la valeur tabulée la plus proche ")
    u_menuiserie = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : U final de la menuiserie utilisé dans le calcul : soit Ujn dans le cas d'une baie avec protection solaire soit Uw dans le cas d'une baie sans protection solaire ")
    ug = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Ug final de la baie : soit saisi directement soit issu des tables forfaitaires ')
    ug_saisi = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : coefficient de transmission thermique du vitrage saisi directement (nécessite une justification) ')
    ujn = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Ujn final de la baie : soit saisi directement soit issu des tables forfaitaires ')
    ujn_saisi = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : coefficient de transmission thermique de la baie avec ses protection solaires saisi directement (nécessite une justification) ')
    uw = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Uw final de la baie : soit saisi directement soit issu des tables forfaitaires ')
    uw_1 = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : Uw de la première fenêtre dans le cas d'une double fenêtre (par défaut la première fenêtre est toujours celle avec le Uw le plus élevé -> plus performante) ")
    uw_2 = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : Uw de la deuxième fenêtre dans le cas d'une double fenêtre (par défaut la deuxième fenêtre est toujours celle avec le Uw le plus faible -> moins performante) ")
    uw_saisi = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : coefficient de transmission thermique de la baie saisi directement (nécessite une justification) ')
    vitrage_vir = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : est ce que le vitrage est  à isolation renforcée 0 : non 1 : oui ')
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    enum_type_pose_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : type de pose de la baie ')
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    reference_paroi = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet paroi qui est associé à l'objet baie vitrée. La codification et utilisation des références peut différer entre logiciels mais il devrait être attendu que reference_paroi est la référence d'une paroi de type mur,plancher_haut ou plancher_bas  ")
    reference_lnc = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement | description : reference projet de l'objet  local non chauffé qui peut être associé à la paroi . Dans le cas d'un espace tampon solarisé cette référence est celle de l'espace tampon. ")
    presence_protection_solaire_hors_fermeture = models.IntegerField(blank=True, null=True)
    presence_joint = models.IntegerField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_baie_vitree'


class DpeBaieVitreeDoubleFenetre(models.Model):
    baie_vitree_id = models.OneToOneField(DpeBaieVitree, models.DO_NOTHING, primary_key=True, db_column='baie_vitree_id', db_index=True)
    tv_ug_id = models.IntegerField(blank=True, null=True)
    enum_type_vitrage_id = models.IntegerField(blank=True, null=True)
    enum_inclinaison_vitrage_id = models.IntegerField(blank=True, null=True)
    enum_type_gaz_lame_id = models.IntegerField(blank=True, null=True)
    epaisseur_lame = models.FloatField(blank=True, null=True)
    vitrage_vir = models.IntegerField(blank=True, null=True)
    enum_methode_saisie_perf_vitrage_id = models.IntegerField(blank=True, null=True)
    ug_saisi = models.FloatField(blank=True, null=True)
    tv_uw_id = models.IntegerField(blank=True, null=True)
    enum_type_materiaux_menuiserie_id = models.IntegerField(blank=True, null=True)
    enum_type_baie_id = models.IntegerField(blank=True, null=True)
    uw_saisi = models.FloatField(blank=True, null=True)
    tv_sw_id = models.IntegerField(blank=True, null=True)
    sw_saisi = models.FloatField(blank=True, null=True)
    enum_type_pose_id = models.IntegerField(blank=True, null=True)
    ug = models.FloatField(blank=True, null=True)
    uw = models.FloatField(blank=True, null=True)
    sw = models.FloatField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_baie_vitree_double_fenetre'


class DpeBilanConsommation(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    classe_conso_energie = models.CharField(max_length=255, db_comment=" modèle concerné : tertiaire | description : classe de consommation d'energie suivant le referentiel DPE 2006 (energie primaire) ")
    classe_emission_ges = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : tertiaire | description : classe d'estimation ges suivant le referentiel DPE 2006 ")
    conso_energie_primaire = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : tertiaire | description : consommation d'énergie primaire totale rapportée à la surface (kWhep/m²/an) ")
    emission_ges = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : tertiaire | description : estimation ges totale rapportée à la surface  (kgCO2/m²/an) ')
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_bilan_consommation'


class DpeCaracteristiqueGenerale(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True, related_name='dpecaracteristiquegenerale')
    annee_construction = models.IntegerField(blank=True, null=True)
    appartement_non_visite = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : est ce que l'appartement est un appartement non visité dans le cas d'un DPE appartement généré à partir d'un immeuble. (application de système individuel les moins performants de l'immeuble) ")
    enum_categorie_erp_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : tertiaire | description : categorie d'ERP ")
    enum_methode_application_dpe_log_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : méthode d'application du DPE logement ")
    enum_periode_construction_id = models.IntegerField(blank=True, null=True)
    enum_usage_fonctionnel_batiment_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : tertiaire | description : type d'usage fonctionnel du batiment tertiaire ou batiment recevant du public ")
    hsp = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : hauteur sous plafond moyenne du logement/de l'immeuble ")
    nombre_appartement = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : nombre d'appartements de l'immeuble dans le cas d'un DPE appartement avec usage collectif ou d'un DPE immeuble.  ")
    nombre_niveau_immeuble = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : nombre de niveaux total de l'immeuble ")
    nombre_niveau_logement = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : nombre de niveaux du logement (maison ou appartement)  ')
    nombre_occupant = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : tertiaire | description : nombre d'occupants du bâtiment tertiaire ")
    shon = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : tertiaire | description : surface hors œuvre nette du bâtiment ')
    surface_habitable_immeuble = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface habitable totale de l'immeuble  dans le cas d'un DPE appartement avec usage collectif ou d'un DPE immeuble.  ")
    surface_habitable_logement = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface habitable du logement renseignée sauf dans le cas du dpe à l'immeuble ")
    surface_utile = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : tertiaire | description : surface de référence utile du bâtiment auquelle la consommation est rapportée ')
    surface_tertiaire_immeuble = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface tertiaire totale de l'immeuble  dans le cas  d'un DPE immeuble. La surface tertiaire est prise en compte pour le calcul des besoins dans le cas d'une installation collective mixte tertiaire/residentiel ")
    enum_methode_application_dpe_ter_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : tertiaire | description : methode d'application du DPE tertiaire (facture, vierge ou neuf) ")
    enum_calcul_echantillonnage_id = models.IntegerField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)
    is_dpe_2012 = models.BooleanField(null=True)
    enum_sous_modele_dpe_ter_id = models.ForeignKey('DpeEnumSousModeleDpeTer', models.DO_NOTHING, db_column='enum_sous_modele_dpe_ter_id', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'dpe_caracteristique_generale'


class DpeClimatisation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    besoin_fr = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : besoin de refroidissement annuel.  Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est le besoin  de l'installation à l'immeuble qu'il faut saisir. ")
    cle_repartition_clim = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : clé de répartition pour passer des consommations bâtiments au consommation logement dans le cas DPE appartement calculé à partir du DPE immeuble UNIQUEMENT. Voir section 8.5.4 du document guide pour plus de détail. ')
    conso_fr = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation de refroidissement annuel (kWh).  Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation de l'installation à l'immeuble qu'il faut saisir. ")
    conso_fr_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation de refroidissement annuel pour le scénario dépensier (kWh)  .  Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation de l'installation à l'immeuble qu'il faut saisir. ")
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    eer = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : coefficient d'efficience energétique du système de climatisation final (SEER *0,95) ")
    enum_methode_calcul_conso_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : méthode de calcul de consommation de froid :  simple,  ou cas particuliers installation collective virtualisée ou installation individuelle échantilonnée (dpe immeuble) ')
    enum_methode_saisie_carac_sys_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : methode de saisie du seer : lecture de table forfaitaire ou saisie justifiée ')
    enum_periode_installation_fr_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : période d'installation du système de refroidissement ")
    enum_type_generateur_fr_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : type de générateur de froid  ')
    nombre_logement_echantillon = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : nombre de logements représentés par le logement échantillon dans le cas d'un DPE immeuble avec installation de climatisation  individuelle.  (à ne renseigner que dans ce cas précis) ")
    ref_produit_fr = models.CharField(max_length=255, blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : référence produit  et marque du générateur de froid ')
    surface_clim = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description :  surface climatisée : si le logement n'est pas climatisé dans son ensemble la surface climatisée peut être inférieure à la surface totale du logement.Dans le cas spécifique d'un DPE immeuble avec installation individuelle échantillonée :saisir la surface climatisée par la totalité des logements représentés par le logement moyen surface_clim =  Shmoy*Nblgt.  Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la surface de l'installation à l'immeuble qu'il faut renseigner ")
    tv_seer_id = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient d'efficience énergétique du système de climatisation seer ")
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    emetteur_plancher_fr = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : est ce que l'emetteur de froid est un plancher rafraichissant (utilisé pour le calcul des auxiliaires) A NE PLUS RENSEIGNER : OBSOLETE ")
    enum_type_energie_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description :  type d'énergie consommée par le générateur de froid ")
    reference = models.CharField(max_length=255, blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_climatisation'


class DpeConfortEte(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    aspect_traversant = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : est ce que le logement est traversant 0 : non 1 : oui ')
    brasseur_air = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : est ce que le logement est équipé de brasseurs d'air 0 : non 1 : oui ")
    enum_indicateur_confort_ete_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : indicateur confort été (bon moyen ou  mauvais)  ')
    isolation_toiture = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : as-t-on une isolation de toiture 0 : non 1 : oui ')
    protection_solaire_exterieure = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : as-t-on une protection solair exteriaire sur les facades vitrées (exception nord) 0 : non 1 : oui ')
    inertie_lourde = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : est ce que le logement possède une inerte lourde ou très lourde 0 : non 1 : oui ')
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_confort_ete'


class DpeConsommation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    conso_energie_finale = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : tertiaire | description : consommation d'energie finale du poste de consommation en kWh ")
    conso_energie_primaire = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : tertiaire | description : consommation d'energie primaire du poste de consommation en kWhep ")
    enum_type_energie_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : tertiaire | description : type d'énergie associée à la consommaton ")
    enum_type_usage_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : tertiaire | description :  type d'usage associé à la consommation ")
    frais_annuels_energie = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : tertiaire | description : frais d'energies associés  à la consommation (en euros) ")
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    annee_consommation = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : tertiaire | description : année de relève de la consommation/production electricité ')
    dpe2012_enum_type_energie_id = models.IntegerField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)
    is_dpe_2012 = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_consommation'


class DpeCout(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    cout_5_usages = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coût totale  5 usages (ecs/chauffage/climatisation/eclairage/auxiliaires) (déduit de la production pv autoconsommée) (€) ')
    cout_auxiliaire_distribution_ch = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : coût des auxilliaires de distribution de chauffage  (€) ')
    cout_auxiliaire_distribution_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : coût des auxilliaires de distribution de l'ECS  (€) ")
    cout_auxiliaire_distribution_fr = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : coût  des auxilliaires de distribution de froid  (€) SUPPRIME ')
    cout_auxiliaire_generation_ch = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : coût des auxilliaires de génération de chauffage  (€) ')
    cout_auxiliaire_generation_ch_depensier = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : coût des auxilliaires de génération de chauffage  pour le scénario dépensier (€) ')
    cout_auxiliaire_generation_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : coût des auxillaires de generation de l'ECS  (€) ")
    cout_auxiliaire_generation_ecs_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : coût des auxillaires de generation de l'ECS  pour le scénario dépensier (€) ")
    cout_auxiliaire_ventilation = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coût  des auxilliaires de ventilation  (€) ')
    cout_ch = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coût de chauffage(déduit de la production pv autoconsommée)   (€) ')
    cout_ch_depensier = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coût de chauffage  pour le scénario dépensier (déduit de la production pv autoconsommée) (€) ')
    cout_eclairage = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coût des eclairage  (déduit de la production pv autoconsommée) (€) ')
    cout_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : coût de l'ECS  (déduit de la production pv autoconsommée) (€) ")
    cout_ecs_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : coût de l'ECS pour le scénario dépensier (déduit de la production pv autoconsommée)   (€) ")
    cout_fr = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coût  de refroidissement annuel (déduit de la production pv autoconsommée)  (€) ')
    cout_fr_depensier = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coût de refroidissement pour le scénario dépensier (déduit de la production pv autoconsommée)   (€) ')
    cout_total_auxiliaire = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : coût  des auxilliaires de l'ensemble des auxiliaires  (déduit de la production pv autoconsommée)  (€) ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_cout'


class DpeDeperdition(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    deperdition_baie_vitree = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : deperditions par les baies vitrées (W/K). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    deperdition_enveloppe = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : deperditions par l'enveloppe (GV). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    deperdition_mur = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : deperditions par les murs(W/K). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    deperdition_plancher_bas = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : deperditions par les planchers bas(W/K). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    deperdition_plancher_haut = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : deperditions par les planchers hauts(W/K). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    deperdition_pont_thermique = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : deperditions par les ponts thermiques(W/K). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    deperdition_porte = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : deperditions par les ponts thermiques(W/K). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    deperdition_renouvellement_air = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : deperditions par renouvellement d'air totale (hvent + hperm)(W/K). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    hperm = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : part des deperditions de renouvellement d'air liées à la perméabilité à l'air du bâtiment(W/K). Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    hvent = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : part des deperditions de renouvellement d'air liées au système de(W/K) ventilation. Pour les DPE immeubles et appartement à partir de l'immeuble ces données sont à l'immeuble. ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_deperdition'


class DpeDescriptifEnr(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.TextField(db_comment=" modèle concerné : logement + logement neuf | description : description du système d'ENR ")
    enum_categorie_enr_descriptif_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : catégorie de système ENR ')
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_descriptif_enr'


class DpeEfConso(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    conso_5_usages = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : consommation annuelle  5 usages (ecs/chauffage/climatisation/eclairage/auxiliaires)en energie finale(déduit de la production pv autoconsommée)  (kWhef/an) ')
    conso_5_usages_m2 = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : consommation annuelle  5 usages (ecs/chauffage/climatisation/eclairage/auxiliaires)en energie finale(déduit de la production pv autoconsommée)  (kWhef/m²/an) ')
    conso_auxiliaire_distribution_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle d'auxilliaires de distribution de chauffage en energie finale (kWhef/an) ")
    conso_auxiliaire_distribution_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle d'auxilliaires de distribution d'ECS en energie finale (kWhef/an) ")
    conso_auxiliaire_distribution_fr = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle  d'auxilliaires de distribution de froid en energie finale (kWhef/an) ")
    conso_auxiliaire_generation_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle d'auxilliaires de génération de chauffage en energie finale (kWhef/an) ")
    conso_auxiliaire_generation_ch_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle d'auxilliaires de génération de chauffage en energie finale pour le scénario dépensier (kWhef/an) ")
    conso_auxiliaire_generation_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle d'auxillaires de generation d'ECS en energie finale (kWhef/an) ")
    conso_auxiliaire_generation_ecs_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle d'auxillaires de generation d'ECS en energie finale pour le scénario dépensier (kWhef/an) ")
    conso_auxiliaire_ventilation = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation annuelle  d'auxilliaires de ventilation en energie finale (kWhef/an) ")
    conso_ch = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : consommation annuelle de chauffage en energie finale (déduit de la production pv autoconsommée) (kWhef/an) ')
    conso_ch_depensier = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : consommation annuelle de chauffage en energie finale pour le scénario dépensier(déduit de la production pv autoconsommée)  (kWhef/an) ')
    conso_eclairage = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation annuelle d'eclairage en energie finale (déduit de la production pv autoconsommée) (kWhef/an) ")
    conso_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation annuelle d'ECS en energie finale (déduit de la production pv autoconsommée) (kWhef/an) ")
    conso_ecs_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation annuelle d'ECS en energie finale  pour le scénario dépensier (déduit de la production pv autoconsommée) (kWhef/an) ")
    conso_fr = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : consommation de refroidissement annuel  en energie finale (déduit de la production pv autoconsommée) (kWhef/an) ')
    conso_fr_depensier = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : consommation de refroidissement annuel en energie finale pour le scénario dépensier (déduit de la production pv autoconsommée) (kWhef/an) ')
    conso_totale_auxiliaire = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation annuelle de l'ensemble des auxiliaires en énergie finale(déduit de la production pv autoconsommée)  (kWhef/an) ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_ef_conso'


class DpeEmetteurChauffage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    surface_chauffee = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface chauffée par l'emetteur (sous ensemble de la surface chauffée par l'installation). Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la surface de l'installation à l'immeuble qu'il faut renseigner ")
    tv_rendement_emission_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du rendement d'emission de l'émetteur de chauffage ")
    tv_rendement_distribution_ch_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du rendement de distribution de la distribution associée à l'émission ")
    tv_rendement_regulation_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du rendement de régulation associé à l'émission ")
    enum_type_emission_distribution_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : enumérateur qui couple les notions d'emission et de distribution pour produire une description complète des emetteurs de chauffage ")
    tv_intermittence_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient d'intermittence de l'installation I0 ")
    reseau_distribution_isole = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : est ce que le réseau de distribution est isolé 0 : non 1 : oui ')
    enum_equipement_intermittence_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : type d'équipement d'intermittence associé à la génération ")
    enum_type_regulation_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : type de régulation associée au générateur ')
    enum_type_chauffage_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : type de chauffage : Central ou Divisé ')
    enum_temp_distribution_ch_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : température de distribution de l'installation de chauffage (pour le calcul des auxiliaires de distribution) ")
    enum_lien_generateur_emetteur_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : lien entre le générateur et l'émetteur associé ")
    i0 = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : coefficient d'intermittence de l'installation ")
    rendement_emission = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : Re : rendement d'émission du système de chauffage (0-1) ")
    rendement_distribution = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : Rd : rendement de distribution du système de chauffage    (0-1) ')
    rendement_regulation = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : Rr : rendement de régulation du système de chauffage  (0-1) ')
    installation_chauffage_id = models.ForeignKey('DpeInstallationChauffage', models.DO_NOTHING, db_column='installation_chauffage_id', db_index=True,  null=True, blank=True)
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    enum_periode_installation_emetteur_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : période d'installation des émetteurs de chauffage (utilisé pour le calcul des températures de fonctionnement des systèmes à combustion de type chaudière gaz ou fioul) ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_emetteur_chauffage'


class DpeEmissionGes(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True, related_name='dpeemissionges')
    classe_emission_ges = models.CharField(max_length=255, db_comment=" modèle concerné : logement + logement neuf | description : classe d'estimation ges du DPE 5 usages ")
    emission_ges_5_usages = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : estimation GES totale  5 usages (déduit de la production pv autoconsommée)  (ecs/chauffage/climatisation/eclairage/auxiliaires)(kgCO2/an) ')
    emission_ges_5_usages_m2 = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : estimation GES totale  5 usages rapportée au m² (déduit de la production pv autoconsommée)  (ecs/chauffage/climatisation/eclairage/auxiliaires)(kgCO2/m2/an) ')
    emission_ges_auxiliaire_distribution_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : estimation GES d'auxilliaires de distribution de chauffage  (kgCO2/an) ")
    emission_ges_auxiliaire_distribution_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : estimation GES d'auxilliaires de distribution d'ECS  (kgCO2/an) ")
    emission_ges_auxiliaire_distribution_fr = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : estimation GES  d'auxilliaires de distribution de froid  (kgCO2/an) SUPPRIME ")
    emission_ges_auxiliaire_generation_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : estimation GES d'auxilliaires de génération de chauffage  (kgCO2/an) ")
    emission_ges_auxiliaire_generation_ch_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : estimation GES d'auxilliaires de génération de chauffage  pour le scénario dépensier (kgCO2/an) ")
    emission_ges_auxiliaire_generation_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : estimation GES d'auxillaires de generation d'ECS  (kgCO2/an) ")
    emission_ges_auxiliaire_generation_ecs_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : estimation GES d'auxillaires de generation d'ECS  pour le scénario dépensier (kgCO2/an) ")
    emission_ges_auxiliaire_ventilation = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : estimation GES  d'auxilliaires de ventilation  (kgCO2/an) ")
    emission_ges_ch = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : estimation GES de chauffage (déduit de la production pv autoconsommée)   (kgCO2/an) ')
    emission_ges_ch_depensier = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : estimation GES de chauffage  pour le scénario dépensier(déduit de la production pv autoconsommée)  (kgCO2/an) ')
    emission_ges_eclairage = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : estimation GES d'eclairage  (déduit de la production pv autoconsommée) (kgCO2/an) ")
    emission_ges_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : estimation GES d'ECS (déduit de la production pv autoconsommée)   (kgCO2/an) ")
    emission_ges_ecs_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : estimation GES d'ECS pour le scénario dépensier  (déduit de la production pv autoconsommée)  (kgCO2/an) ")
    emission_ges_fr = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : estimation GES  de refroidissement annuel (déduit de la production pv autoconsommée)  (kgCO2/an) ')
    emission_ges_fr_depensier = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : estimation GES de refroidissement pour le scénario dépensier (déduit de la production pv autoconsommée)    (kgCO2/an) ')
    emission_ges_totale_auxiliaire = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : estimation GES de l'ensemble des auxiliaires (déduit de la production pv autoconsommée)  (kgCO2/an) ")
    date_derniere_modification = models.DateTimeField(null=True)
    is_dpe_2012 = models.BooleanField(null=True)
    ancienne_classe_emission_ges = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dpe_emission_ges'


class DpeEnumBouclageReseauEcs(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_bouclage_reseau_ecs'


class DpeEnumCalculEchantillonnage(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_calcul_echantillonnage'


class DpeEnumCategorieDescriptifSimplifie(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_categorie_descriptif_simplifie'


class DpeEnumCategorieEnrDescriptif(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_categorie_enr_descriptif'


class DpeEnumCategorieErp(models.Model):
    lib = models.TextField(blank=True, null=True)
    groupe_erp = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_categorie_erp'


class DpeEnumCategorieFicheTechnique(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_categorie_fiche_technique'


class DpeEnumCfgInstallationCh(models.Model):
    lib = models.TextField(blank=True, null=True)
    nombre_generateur = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_cfg_installation_ch'


class DpeEnumCfgInstallationEcs(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_cfg_installation_ecs'


class DpeEnumCfgIsolationLnc(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_cfg_isolation_lnc'


class DpeEnumClasseAltitude(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_classe_altitude'


class DpeEnumClasseEtiquette(models.Model):
    id = models.TextField(primary_key=True)
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_classe_etiquette'


class DpeEnumClasseInertie(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_classe_inertie'


class DpeEnumEquipementIntermittence(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_equipement_intermittence'


class DpeEnumInclinaisonPv(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_inclinaison_pv'


class DpeEnumInclinaisonVitrage(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_inclinaison_vitrage'


class DpeEnumIndicateurConfortEte(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_indicateur_confort_ete'


class DpeEnumLienGenerateurEmetteur(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_lien_generateur_emetteur'


class DpeEnumLotTravaux(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_lot_travaux'


class DpeEnumMateriauxStructureMur(models.Model):
    lib = models.TextField(blank=True, null=True)
    hors_methode = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_materiaux_structure_mur'


class DpeEnumMethodeApplicationDpeLog(models.Model):
    lib = models.TextField(blank=True, null=True)
    methode_application_dpe = models.TextField(blank=True, null=True)
    type_batiment = models.TextField(blank=True, null=True)
    type_installation_chauffage = models.TextField(blank=True, null=True)
    type_installation_ecs = models.TextField(blank=True, null=True)
    type_virtualisation_extrapolation = models.TextField(blank=True, null=True)
    declare_surface_immeuble = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    surface_reference = models.TextField(blank=True, null=True)
    niveau_certification_diagnostiqueur = models.TextField(blank=True, null=True)
    enum_modele_dpe_id = models.TextField(blank=True, null=True)
    enum_modele_audit_id = models.TextField(blank=True, null=True)
    type_habilitation_auditeur = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)
    surface_reference_calcul_etiquette = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_methode_application_dpe_log'


class DpeEnumMethodeApplicationDpeTer(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    niveau_certification_diagnostiqueur = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_methode_application_dpe_ter'


class DpeEnumMethodeCalculConso(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_methode_calcul_conso'


class DpeEnumMethodeSaisieCaracSys(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_methode_saisie_carac_sys'


class DpeEnumMethodeSaisieFactCouvSol(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_methode_saisie_fact_couv_sol'


class DpeEnumMethodeSaisiePerfVitrage(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_methode_saisie_perf_vitrage'


class DpeEnumMethodeSaisiePontThermique(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_methode_saisie_pont_thermique'


class DpeEnumMethodeSaisieQ4PaConv(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_methode_saisie_q4pa_conv'


class DpeEnumMethodeSaisieU(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_methode_saisie_u'


class DpeEnumMethodeSaisieU0(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_methode_saisie_u0'


class DpeEnumMethodeSaisieUporte(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_methode_saisie_uporte'


class DpeEnumModeleDpe(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_modele_dpe'


class DpeEnumNumPackTravaux(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_num_pack_travaux'


class DpeEnumOrientation(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_orientation'


class DpeEnumOrientationPv(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_orientation_pv'


class DpeEnumOrigineDonnee(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_origine_donnee'


class DpeEnumPeriodeConstruction(models.Model):
    lib = models.TextField(blank=True, null=True)
    defaut_mur_enum_type_isolation_id = models.TextField(blank=True, null=True)
    defaut_terre_plein_enum_type_isolation_id = models.TextField(blank=True, null=True)
    defaut_plancher_bas_enum_type_isolation_id = models.TextField(blank=True, null=True)
    defaut_plancher_haut_enum_type_isolation_id = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_periode_construction'


class DpeEnumPeriodeInstallationEcsThermo(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_periode_installation_ecs_thermo'


class DpeEnumPeriodeInstallationEmetteur(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_periode_installation_emetteur'


class DpeEnumPeriodeInstallationFr(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_periode_installation_fr'


class DpeEnumPeriodeIsolation(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_periode_isolation'


class DpeEnumPictoGesteEntretien(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_picto_geste_entretien'


class DpeEnumPositionEtageLogement(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_position_etage_logement'


class DpeEnumQualiteComposant(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_qualite_composant'


class DpeEnumSecteur(models.Model):
    id = models.IntegerField(primary_key=True)
    lib = models.CharField(max_length=100)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_secteur'


class DpeEnumSousModeleDpeTer(models.Model):
    id = models.IntegerField(primary_key=True)
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_sous_modele_dpe_ter'


class DpeEnumStatutGeocodageBan(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_statut_geocodage_ban'


class DpeEnumTempDistributionCh(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_temp_distribution_ch'


class DpeEnumTypeAdjacence(models.Model):
    lib = models.TextField(blank=True, null=True)
    local_non_chauffe = models.TextField(blank=True, null=True)
    type_paroi_autorise = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    calcul_ue_plancher_bas = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_adjacence'


class DpeEnumTypeBaie(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_baie'


class DpeEnumTypeChauffage(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_chauffage'


class DpeEnumTypeDoublage(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_doublage'


class DpeEnumTypeEmissionDistribution(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_emission_distribution'


class DpeEnumTypeEnergie(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_energie'


class DpeEnumTypeEnr(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_enr'


class DpeEnumTypeFermeture(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_fermeture'


class DpeEnumTypeGazLame(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_gaz_lame'


class DpeEnumTypeGenerateurCh(models.Model):
    lib = models.TextField(blank=True, null=True)
    calcul_combustion = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    enum_type_energie_id = models.TextField(blank=True, null=True)
    hors_methode = models.TextField(blank=True, null=True)
    rpn_sup_rpint = models.TextField(blank=True, null=True)
    position_probable_volume_chauffe = models.TextField(blank=True, null=True)
    categorie_open_data = models.TextField(blank=True, null=True)
    periode_installation_min = models.TextField(blank=True, null=True)
    periode_installation_max = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_generateur_ch'


class DpeEnumTypeGenerateurEcs(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    enum_type_energie_id = models.TextField(blank=True, null=True)
    hors_methode = models.TextField(blank=True, null=True)
    position_probable_volume_chauffe = models.TextField(blank=True, null=True)
    categorie_open_data = models.TextField(blank=True, null=True)
    periode_installation_min = models.TextField(blank=True, null=True)
    periode_installation_max = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_generateur_ecs'


class DpeEnumTypeGenerateurFr(models.Model):
    lib = models.TextField(blank=True, null=True)
    periode_installation_min = models.TextField(blank=True, null=True)
    periode_installation_max = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_generateur_fr'


class DpeEnumTypeInstallation(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_installation'


class DpeEnumTypeInstallationSolaire(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_installation_solaire'


class DpeEnumTypeIsolation(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_isolation'


class DpeEnumTypeJustificatif(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_justificatif'


class DpeEnumTypeLiaison(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_liaison'


class DpeEnumTypeMateriauxMenuiserie(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_materiaux_menuiserie'


class DpeEnumTypePlancherBas(models.Model):
    lib = models.TextField(blank=True, null=True)
    hors_methode = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_plancher_bas'


class DpeEnumTypePlancherHaut(models.Model):
    lib = models.TextField(blank=True, null=True)
    hors_methode = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_plancher_haut'


class DpeEnumTypePorte(models.Model):
    lib = models.TextField(blank=True, null=True)
    nature_de_la_menuiserie = models.TextField(blank=True, null=True)
    type_de_porte = models.TextField(blank=True, null=True)
    hors_methode = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_porte'


class DpeEnumTypePose(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_pose'


class DpeEnumTypeRegulation(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_regulation'


class DpeEnumTypeStockageEcs(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_stockage_ecs'


class DpeEnumTypeUsage(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_usage'


class DpeEnumTypeVentilation(models.Model):
    lib = models.TextField(blank=True, null=True)
    periode_construction = models.TextField(blank=True, null=True)
    categorie_open_data = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_ventilation'


class DpeEnumTypeVitrage(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_type_vitrage'


class DpeEnumTypologieLogement(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_typologie_logement'


class DpeEnumUsageFonctionnelBatiment(models.Model):
    lib = models.TextField(blank=True, null=True)
    categorie_tertiaire = models.TextField(blank=True, null=True)
    type_erp = models.TextField(blank=True, null=True)
    enum_secteur_id = models.IntegerField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_usage_fonctionnel_batiment'


class DpeEnumUsageGenerateur(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_usage_generateur'


class DpeEnumVersion(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    lib = models.TextField(blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)
    arrete_methode = models.TextField(blank=True, null=True)
    arrete_reseau_chaleur = models.TextField(blank=True, null=True)
    arrete_prix_energie = models.TextField(blank=True, null=True)
    arrete_contenu_co2_energie = models.TextField(blank=True, null=True)
    date_application_debut = models.TextField(blank=True, null=True)
    date_application_fin = models.TextField(blank=True, null=True)
    version_xsd_min = models.TextField(blank=True, null=True)
    version_xsd_max = models.TextField(blank=True, null=True)
    controle_coherence = models.TextField(blank=True, null=True)
    version_controle_coherence_min = models.TextField(blank=True, null=True)
    version_controle_coherence_max = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_version'


class DpeEnumZoneClimatique(models.Model):
    lib = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_enum_zone_climatique'


class DpeEpConso(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True, related_name='dpeepconso')
    ep_conso_5_usages = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : consommation annuelle  5 usages (ecs/chauffage/climatisation/eclairage/auxiliaires)en energie primaire (déduit de la production pv autoconsommée) (kWhep/an) ')
    ep_conso_5_usages_m2 = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : consommation annuelle  5 usages (ecs/chauffage/climatisation/eclairage/auxiliaires)en energie primaire (déduit de la production pv autoconsommée) (kWhep/m²/an) ')
    ep_conso_auxiliaire_distribution_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle d'auxilliaires de distribution de chauffage en energie primaire (kWhep/an) ")
    ep_conso_auxiliaire_distribution_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle d'auxilliaires de distribution d'ECS en energie primaire (kWhep/an) ")
    ep_conso_auxiliaire_distribution_fr = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle  d'auxilliaires de distribution de froid en energie primaire (kWhep/an) SUPPRIME ")
    ep_conso_auxiliaire_generation_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle d'auxilliaires de génération de chauffage en energie primaire (kWhep/an) ")
    ep_conso_auxiliaire_generation_ch_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle d'auxilliaires de génération de chauffage en energie primaire pour le scénario dépensier (kWhep/an) ")
    ep_conso_auxiliaire_generation_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle d'auxillaires de generation d'ECS en energie primaire (kWhep/an) ")
    ep_conso_auxiliaire_generation_ecs_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation annuelle d'auxillaires de generation d'ECS en energie primaire pour le scénario dépensier (kWhep/an) ")
    ep_conso_auxiliaire_ventilation = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation annuelle  d'auxilliaires de ventilation en energie primaire (kWhep/an) ")
    ep_conso_ch = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : consommation annuelle de chauffage en energie primaire(déduit de la production pv autoconsommée)  (kWhep/an) ')
    ep_conso_ch_depensier = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : consommation annuelle de chauffage en energie primaire pour le scénario dépensier (déduit de la production pv autoconsommée) (kWhep/an) ')
    ep_conso_eclairage = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation annuelle d'eclairage en energie primaire (déduit de la production pv autoconsommée) (kWhep/an) ")
    ep_conso_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation annuelle d'ECS en energie primaire (déduit de la production pv autoconsommée) (kWhep/an) ")
    ep_conso_ecs_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation annuelle d'ECS en energie primaire  pour le scénario dépensier (déduit de la production pv autoconsommée) (kWhep/an) ")
    ep_conso_fr = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : consommation de refroidissement annuel en énergie primaire  (déduit de la production pv autoconsommée) (kWhep/an) ')
    ep_conso_fr_depensier = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : consommation de refroidissement annuel en énergie primaire pour le scénario dépensier (déduit de la production pv autoconsommée)  (kWhep/an) ')
    ep_conso_totale_auxiliaire = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation annuelle de l'ensemble des auxiliaires en energie primaire (déduit de la production pv autoconsommée) (kWhep/an) ")
    classe_bilan_dpe = models.CharField(max_length=255, blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Classe du DPE issu de la synthèse du double seuil  sur les consommations énergie primaire et les émissions de CO2 sur les 5 usages  (ecs/chauffage/climatisation/eclairage/auxiliaires) ')
    date_derniere_modification = models.DateTimeField(null=True)
    is_dpe_2012 = models.BooleanField(null=True)
    ancienne_classe_bilan_dpe = models.TextField(blank=True, null=True)
    nouvelle_classe_energie_dpe = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dpe_ep_conso'


class DpeEts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    bver = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : coefficient de reduction des déperditions de l'espace tampon solarisé ")
    coef_transparence_ets = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : coefficient de transparence de l'espace tampon solarisé T (déterminé à partir des parois vitrées de l'espace tampon solarisé) ")
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement | description : description textuelle de l'objet ")
    enum_cfg_isolation_lnc_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : configuration de l'adjacence avec local non chauffé :  local chauffé (non) isolé/local non chauffé (non) isolé/orientation véranda qui permet de calculer le b  ")
    tv_coef_reduction_deperdition_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de reduction des deperditions ')
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    tv_coef_transparence_ets_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de transparence de l'espace tampon solarisé ")
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_ets'


class DpeGenerateurChauffage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    conso_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation d'energie annuelle du générateur de chauffage en energie finale kWh (exprimée en kWh PCI pour les combustibles). Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation du générateur à l'immeuble qu'il faut saisir. ")
    conso_ch_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation d'énergie annuelle du générateur de chauffage pour le scénario dépensier (scénario DH21) en energie finale kWh (exprimée en kWh PCI pour les combustibles). Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation du générateur à l'immeuble qu'il faut saisir. ")
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    enum_methode_saisie_carac_sys_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : méthode de saisie des performances du système de chauffage ')
    enum_type_energie_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description :  type d'énergie consommée par le générateur de chauffage ")
    enum_type_generateur_ch_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : type de generateur de chauffage ')
    enum_usage_generateur_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : usages assurés par le générateur (chauffage/ecs/chauffage+ecs) ')
    n_radiateurs_gaz = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : nombre de radiateurs gaz ')
    pn = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : puissance nominale du générateur à combustion (W) ')
    position_volume_chauffe = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : est ce que le générateur est positionné dans le volume chauffé. (pour le calcul des pertes de génération récupérables) ')
    presence_regulation_combustion = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : présence d'un organe de régulation pour le système de chauffage à combustion 0 : non 1 : oui ")
    presence_ventouse = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : présence d'un système de ventouse ou avec un ventilateur pour l'évacuation des fumées d'un système à combustion 0 : non 1 : oui ")
    priorite_generateur_cascade = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, db_comment=' modèle concerné : logement | description : ordre de priorité du générateur en cascade (ordonné de manière croissante 1 : générateur principal , 2: genérateur secondaire etc…) ')
    pveilleuse = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : puissance de la veilleuse du générateur à combustion  (W) ')
    qp0 = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : pertes à l'arret du générateur à combustion. Dans le cas d'un générateur virtualisé pour DPE appartement avec chauffage collectif saisir Qp0 correspondant à Pe = a*Pn(collectif) (W) ")
    ref_produit_generateur_ch = models.CharField(max_length=255, blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : référence produit  et marque du générateur de chauffage ')
    rendement_generation = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : Rg : rendement de génération du système de chauffage pour tous les générateurs sauf thermodynamique. Pour les générateurs à combustion il faut saisir le rendement sur PCI (0-1,5) ')
    rpint = models.FloatField(blank=True, null=True)
    rpn = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : rendement de génération à pleine charge du générateur à combustion (0-1,5) ')
    scop = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : scop du générateur thermodynamique (en remplacement du Rg pour les générateurs thermodynamique) (0-20) ')
    temp_fonc_100 = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : température de fonctionnement à 100% de charge (°C) ')
    temp_fonc_30 = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : température de fonctionnement à 30% de charge (°C) ')
    tv_generateur_combustion_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul des paramètres du générateur à combustion Rpn,Rpint,Qp0,Pveil ')
    tv_rendement_generation_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul  des rendements de générations forfaitaires des générateurs autres qu'à combustion ")
    tv_reseau_chaleur_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : id de la ligne de la table utilisée pour le calcul du contenu CO2 des réseaux de chaleurs (OBSOLETE et remplacé par identifiant_reseau_chaleur à partir du 18 janvier 2022 et la prise en compte du nouvel arrêté réseau de chaleur).  ')
    tv_scop_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul  du coefficient de performance du système thermodynamique (SCOP) ')
    tv_temp_fonc_100_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul  de la température à 100% de charge du système à combustion(SUPPRIME) ')
    tv_temp_fonc_30_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul  de la température à 30% de charge du système à combustion(SUPPRIME) ')
    installation_chauffage_id = models.ForeignKey('DpeInstallationChauffage', models.DO_NOTHING, db_column='installation_chauffage_id', db_index=True,  null=True, blank=True)
    enum_lien_generateur_emetteur_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : lien entre le générateur et l'émetteur associé ")
    identifiant_reseau_chaleur = models.CharField(max_length=5, blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : identifiant réseau de chaleur ou de froid utilisé (utilisé à partir du 18 janvier 2022) ')
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    dpe2012_enum_type_energie_id = models.IntegerField(blank=True, null=True)
    reference_generateur_mixte = models.CharField(max_length=255, blank=True, null=True)
    date_arrete_reseau_chaleur = models.DateTimeField(blank=True, null=True)
    migre_en_utc = models.BooleanField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)
    is_dpe_2012 = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_generateur_chauffage'


class DpeGenerateurEcs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, db_column='id')
    conso_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation d'energie annuelle du générateur d'ECS  (kWh) (Exprimé en kWh PCI pour les combustibles ).   Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation du générateur à l'immeuble qu'il faut saisir. ")
    conso_ecs_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation d'énergie annuelle du générateur d'ECS pour le scénario dépensier en énergie finale (kWh) (Exprimé en kWh PCI pour les combustibles ). Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation du générateur à l'immeuble qu'il faut saisir. ")
    cop = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : COP du chauffe-eau thermodynamique (inclus le rendement de stockage) (0-20) ')
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    enum_methode_saisie_carac_sys_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : méthode de saisie des performances du système d'ECS ")
    enum_periode_installation_ecs_thermo_id = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, db_comment=' modèle concerné : logement | description : periode installation du système thermodynamique ')
    enum_type_energie_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description :  type d'énergie consommée par le générateur d'ECS ")
    enum_type_generateur_ecs_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type de generateur d'ecs ")
    enum_type_stockage_ecs_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : Type de stockage d'ECS (intégré à la production ou indépendant) ")
    enum_usage_generateur_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : usages assurés par le générateur (chauffage/ecs/chauffage+ecs) ')
    pn = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : puissance nominale du générateur à combustion. Dans le cas d'un générateur virtualisé pour DPE appartement avec ECS collective saisir Pe = a*Pn(collectif) (W) ")
    position_volume_chauffe = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : est ce que le générateur est positionné dans le volume chauffé. (pour le calcul des pertes de génération récupérables) ')
    presence_ventouse = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : présence d'un système de ventouse ou avec un ventilateur pour l'évacuation des fumées d'un système à combustion 0 : non 1 : oui ")
    pveilleuse = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : puissance de la veilleuse du générateur à combustion (W) ')
    qp0 = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : pertes à l'arret du générateur à combustion. Dans le cas d'un générateur virtualisé pour DPE appartement avec ECS collective saisir Qp0 correspondant à Pe = a*Pn(collectif) ")
    ratio_besoin_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : ratio du besoin ecs de l'installation affecté au générateur. Ce ratio est de 1 pour les installations classiques et de 0,5 pour les installations d'ECS avec deux générateurs ")
    ref_produit_generateur_ecs = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : référence produit  et marque du générateur d'ECS ")
    rendement_generation = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : Rg : rendement de génération dans le cas où le rendement de stockage est séparé du rendement de génération (ballon éléctrique ou ballon séparé de la production) (0-1,5) ')
    rendement_generation_stockage = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : RgxRs : rendement de génération x rendement de stockage pour les systèmes pour lesquels le ballon est intégré au système de production ou réseau de chaleur   (0-1,5) ')
    rendement_stockage = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : Rs : rendement de stockage dans le cas où le rendement de stockage est séparé du rendement de génération (ballon éléctrique ou ballon séparé de la production) sinon égal à 1 (0-1) ')
    rpn = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : rendement de génération à pleine charge du générateur à combustion (0-1,5) ')
    tv_generateur_combustion_id = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul des paramètres du générateur à combustion Rpn,Rpint,Qp0,Pveil ')
    tv_pertes_stockage_id = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul des pertes de stockage pour les ballons éléctriques ')
    tv_reseau_chaleur_id = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du contenu CO2 des réseaux de chaleurs (OBSOLETE et remplacé par identifiant_reseau_chaleur à partir du 18 janvier 2022 et la prise en compte du nouvel arrêté réseau de chaleur).  ')
    tv_scop_id = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul  du coefficient de performance du système thermodynamique (SCOP) ')
    volume_stockage = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : volume de stockage associé au générateur d'ECS ")
    installation_ecs_id = models.ForeignKey('DpeInstallationEcs', models.DO_NOTHING, db_column='installation_ecs_id', db_index=True,  null=True, blank=True)
    identifiant_reseau_chaleur = models.CharField(max_length=5, blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : identifiant réseau de chaleur ou de froid utilisé (utilisé à partir du 18 janvier 2022) ')
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    position_volume_chauffe_stockage = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : est ce que le ballon de stockage est positionné dans le volume chauffé. (pour le calcul des pertes de stockage récupérables) ')
    dpe2012_enum_type_energie_id = models.IntegerField(blank=True, null=True)
    reference_generateur_mixte = models.CharField(max_length=255, blank=True, null=True)
    date_arrete_reseau_chaleur = models.DateTimeField(blank=True, null=True)
    migre_en_utc = models.BooleanField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)
    is_dpe_2012 = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_generateur_ecs'


class DpeGeolocalisation(models.Model):
    administratif_id = models.OneToOneField(DpeAdministratif, models.DO_NOTHING, primary_key=True, editable=True, db_column='administratif_id', related_name='geolocalisation')
    idpar = models.CharField(max_length=255, blank=True, null=True, db_comment=' modèle concerné : tous | description : identifiant de parcelle cadastrale (14 caractères) ')
    immatriculation_copropriete = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : tous | description : numéro d'immatriculation de la copropriété au registre des copropriétés (9 caractères XX0000000) ")
    adresse_bien_id = models.ForeignKey(DpeTAdresse, models.DO_NOTHING, db_column='adresse_bien_id', to_field='id', blank=True, null=True, db_index=True, related_name='geolocalisations')
    rpls_log_id = models.CharField(max_length=8, blank=True, null=True)
    id_batiment_rnb = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)
    is_dpe_2012 = models.BooleanField(null=True)
    provenance_rnb = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dpe_geolocalisation'


class DpeInertie(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    enum_classe_inertie_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : classe d'inertie globale du bâtiment ")
    inertie_paroi_verticale_lourd = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : est ce que les parois verticales sont considérées comme lourdes 0 : non 1 : oui ')
    inertie_plancher_bas_lourd = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : est ce que le plancher bas est considéré comme lourd 0 : non 1 : oui ')
    inertie_plancher_haut_lourd = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : est ce que le plancher haud est considéré comme lourd 0 : non 1 : oui ')
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_inertie'


class DpeInstallationChauffage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    besoin_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : Besoin de chauffage total de l'installation (kWh) ")
    besoin_ch_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : Besoin de chauffage total de l'installation pour le scénario dépensier (DH21) (kWh) ")
    cle_repartition_ch = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : clé de répartition pour passer des consommations bâtiments au consommation logement dans le cas DPE appartement calculé à partir du DPE immeuble UNIQUEMENT. Voir section 8.5.4 du document guide pour plus de détail ')
    coef_ifc = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : coefficient d'individualisation des frais de chauffage dans le cas d'un DPE appartement calculé à partir d'un DPE immeuble ")
    conso_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation d'energie annuelle de l'installation de chauffage  en energie finale kWh. Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation de l'installation à l'immeuble qu'il faut saisir. ")
    conso_ch_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation d'energie annuelle de l'installation de chauffage pour le scénario dépensier (scénario DH21) en energie finale kWh. Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation de l'installation à l'immeuble qu'il faut saisir. ")
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    enum_cfg_installation_ch_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : configuration de l'installation de chauffage ")
    enum_methode_calcul_conso_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : méthode de calcul de consommation de chauffage :  simple,  ou cas particuliers installation collective virtualisée ou installation individuelle échantilonnée (dpe immeuble) ')
    enum_methode_saisie_fact_couv_sol_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : méthode de saisie du facteur de couverture solaire pour le chauffage (saisi en direct justifié ou calculé à partir de la table) ')
    enum_type_installation_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type d'installation de chauffage (collective ou individuelle ou  collective multi batiment ")
    fch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : Facteur de couverture solaire pour l'installation de chauffage ")
    fch_saisi = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : Facteur de couverture solaire pour l'installation de chauffage(saisi) ")
    nombre_logement_echantillon = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : nombre de logements représentés par le logement échantillon dans le cas d'un DPE immeuble avec installation de chauffage  individuelle.  (à ne renseigner que dans ce cas précis) ")
    production_ch_solaire = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : Production de chauffage solaire (kWh) ')
    ratio_virtualisation = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : ratio de virtualisation de l'installation collective lorsque l'on rapporte des usages collectifs à un appartement (a =  Shabappartement/Shabtotale) ")
    surface_chauffee = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface chauffée par l'installation de chauffage(surface du logement ou de l'immeuble). Dans le cas spécifique d'un DPE immeuble avec installation individuelle échantillonée :saisir la surface chauffée de  la totalité des logements représentés par le logement moyen surface_habitable=  Shmoy*Nblgt. Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la surface de l'installation à l'immeuble qu'il faut renseigner ")
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    tv_facteur_couverture_solaire_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du facteur de couverture solaire ')
    nombre_niveau_installation_ch = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : nombre de niveaux desservis par l'installation de chauffage (très souvent égal au nombre de niveaux du bâtiment) ")
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    rdim = models.FloatField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)
    is_dpe_2012 = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_installation_chauffage'


class DpeInstallationEcs(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    besoin_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : besoin d'ECS annuel pour l'ensemble de l'installation (kWh). Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation de l'installation à l'immeuble qu'il faut saisir. ")
    besoin_ecs_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : besoin d'ECS annuel pour l'ensemble de l'installation dans le cas du scénario dépensier (kWh).  Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation de l'installation à l'immeuble qu'il faut saisir. ")
    conso_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation d'energie annuelle de l'installation d'ECS  en energie finale kWh. Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation de l'installation à l'immeuble qu'il faut saisir. ")
    conso_ecs_depensier = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : consommation d'energie annuelle de l'installation d'ECS pour le scénario dépensier en energie finale kWh. Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation de l'installation à l'immeuble qu'il faut saisir. ")
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    enum_bouclage_reseau_ecs_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type de bouclage du réseau d'ECS pour la prise en compte des consommations d'auxiliaires de distribution ")
    enum_cfg_installation_ecs_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : code de configuration de l'installation d'ECS (installation simple, avec solaire ou avec plusieurs systèmes d'ECS)  ")
    enum_methode_calcul_conso_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : méthode de calcul de consommation d'ECS :  simple, ou cas particuliers installation collective virtualisée ou installation individuelle échantilonnée (dpe immeuble) ")
    enum_methode_saisie_fact_couv_sol_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : méthode de saisie du facteur de couverture solaire pour l'ECS (saisi en direct justifié ou calculé à partir de la table) ")
    enum_type_installation_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : code du type d'installation d'ECS (collective ou individuelle) ")
    enum_type_installation_solaire_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type d'installation solaire (ECS+Chauffage , ECS solaire seule etc…) ")
    fecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : facteur de couverture solaire de l'ECS ")
    fecs_saisi = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : facteur de couverture solaire pour l'ECS saisi directement lorsque celui-ci peut être justifié ")
    nombre_logement = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : nombre de logements desservis par l'installation d'ECS. Dans le cas d'un DPE immeuble avec installation individuelle échantillonée : saisir le nombre de logements qui sont équipés de ce type d'installation d'ECS.  ")
    production_ecs_solaire = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : production d'ecs solaire annuelle (kWh). Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation de l'installation à l'immeuble qu'il faut saisir. ")
    ratio_virtualisation = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : ratio de virtualisation de l'installation collective lorsque l'on rapporte des usages collectifs à un appartement (a =  Shabappartement/Shabtotale) ")
    rendement_distribution = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : rendement de distribution de l'installation d'ECS  (0-1) ")
    surface_habitable = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface habitable correspondant au(x) logement(x) desservi(s) par l'installation d'ECS.(surface habitable du logement ou de la totalité des logements de l'immeuble) Dans le cas spécifique d'un DPE immeuble avec installation individuelle échantillonée :saisir la surface  de  la totalité des logements représentés par le logement moyen surface_habitable=  Shmoy*Nblgt. Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la surface de l'installation à l'immeuble qu'il faut renseigner ")
    tv_facteur_couverture_solaire_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du facteur de couverture solaire ')
    tv_rendement_distribution_ecs_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du rendement de distribution de l'installation d'ECS ")
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    reseau_distribution_isole = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : est ce que le réseau de distribution est isolé 0 : non 1 : oui ')
    nombre_niveau_installation_ecs = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : nombre de niveaux desservis par l'installation d'ECS (très souvent égal au nombre de niveaux du bâtiment) ")
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    cle_repartition_ecs = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : clé de répartition pour passer des consommations bâtiments au consommation logement dans le cas DPE appartement calculé à partir du DPE immeuble UNIQUEMENT. Voir section 8.5.4 du document guide pour plus de détail ')
    rdim = models.FloatField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)
    is_dpe_2012 = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_installation_ecs'


class DpeLogementVisite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.TextField(db_comment=' modèle concerné : logement + logement neuf | description : description du logement visité ')
    enum_position_etage_logement_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : position du logement dans l'immeuble en terme d'étage ")
    enum_typologie_logement_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : typologie de logement (T1… T6) ')
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    surface_habitable_logement = models.FloatField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_logement_visite'


class DpeMasqueLointainNonHomogene(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    tv_coef_masque_lointain_non_homogene_id = models.IntegerField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_masque_lointain_non_homogene'


class DpeMeteo(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    batiment_materiaux_anciens = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : est ce que le bâtiment est principalement composé de matériaux anciens pour ses murs  0 : non 1 : oui ')
    enum_classe_altitude_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : classe d'altitude du logement ")
    enum_zone_climatique_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : zone climatique du logement ')
    altitude = models.FloatField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)
    is_dpe_2012 = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_meteo'


class DpeMur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    b = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coefficient de réduction des déperditions du mur ')
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    enum_cfg_isolation_lnc_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : configuration de l'adjacence avec local non chauffé :  local chauffé (non) isolé/local non chauffé (non) isolé/orientation véranda qui permet de calculer le b  ")
    enum_materiaux_structure_mur_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : matériaux de structure  de la paroi  ')
    enum_methode_saisie_u0_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : methode de saisie de U0 (inclus les justifications à produire en cas de saisie directe) ')
    enum_methode_saisie_u_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : methode de saisie du U (inclus les justifications à produire en cas de saisie directe) ')
    enum_orientation_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : orientation du mur  ')
    enum_periode_isolation_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : periode d'isolation à saisir si différent de la période de construction (cas d'une rénovation de la paroi) ")
    enum_type_adjacence_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type d'adjacence de la paroi ")
    enum_type_isolation_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type d'isolation du mur (ITI/ITE…..) ")
    epaisseur_isolation = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : epaisseur de l'isolation (si plusieurs isolant différents sommer leurs épaisseurs) (cm) ")
    epaisseur_structure = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : epaisseur de la partie structure de la paroi (sans l'isolation intérieure ou extérieure) (cm) ")
    paroi_ancienne = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : la paroi est une paroi ancienne sur laquelle a été appliquée un enduit isolant (Renduit=0,7m².K.W-1)  0 : non 1 : oui. (Attention ! nom de propriété pas tout à fait explicite) ')
    resistance_isolation = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : resistance isolation ')
    surface_aiu = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : surface aiu : surface des parois du local non chauffé qui donnent sur des locaux chauffés. ')
    surface_aue = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface aue : surface des parois du local non chauffé en contact avec l'extérieur ou le sol ")
    surface_paroi_opaque = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Surface de paroi opaque  (sans baies vitrées sans portes) ')
    surface_paroi_totale = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Surface de paroi opaque + paroi vitrée de la paroi + surface des portes ')
    tv_coef_reduction_deperdition_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de reduction des deperditions ')
    tv_umur0_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du Umur0 ')
    tv_umur_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de transmission thermique umur ')
    umur = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Coefficient de transmission thermique du mur ')
    umur0 = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : Coefficient de transmission thermique du mur non isolé final (avec pris en compte de l'enduit) ")
    umur0_saisi = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : Coefficient de transmission thermique du mur non isolé Saisi en direct par l'utilisateur (à justifier) ")
    umur_saisi = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : Coefficient de transmission thermique du mur saisi en direct par le diagnostiqueur(à justifier)  ')
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    enum_type_doublage_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type de doublage intérieur du mur.(précision de la nature du doublage ou de l'epaisseur de la lame d'air en cas de doublage indéterminé.) ")
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    reference_lnc = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement | description : reference projet de l'objet  local non chauffé qui peut être associé à la paroi . Dans le cas d'un espace tampon solarisé cette référence est celle de l'espace tampon. ")
    enduit_isolant_paroi_ancienne = models.IntegerField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_mur'


class DpePackTravaux(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    conso_5_usages_apres_travaux = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : consommation 5 usages après travaux (kWh/m²/an) ')
    cout_pack_travaux_max = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : fourchette haute de l'estimation des coûts du pack travaux(€) ")
    cout_pack_travaux_min = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : fourchette basse de l'estimation des coûts du pack travaux(€) ")
    enum_num_pack_travaux_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : numéro du pack travaux (1,2,1+2) ')
    descriptif_travaux_id = models.UUIDField(default=uuid.uuid4)
    emission_ges_5_usages_apres_travaux = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : emissions C02 5 usages après travaux (kgCO2/m²/an) ')
    date_derniere_modification = models.DateTimeField(null=True)
    
    class Meta:
        managed = False
        db_table = 'dpe_pack_travaux'


class DpePanneauxPv(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    surface_totale_capteurs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface totale de capteurs photovoltaïque. Dans le cas d'une installation collective de PV pour un DPE appartement, la surface est celle proratisé ")
    ratio_virtualisation = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : ratio de virtualisation de l'installation PV collective lorsque l'on rapporte des usages collectifs à un appartement (a =  Shabappartement/Shabtotale) ")
    nombre_module = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : nombre de modules photovoltaïque standards posés.  ')
    tv_coef_orientation_pv_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient d'orientation des panneaux photovoltaïques ")
    enum_inclinaison_pv_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : inclinaison des panneaux photovoltaïques ')
    enum_orientation_pv_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : orientation des panneaux photovoltaïques ')
    production_elec_enr_id = models.ForeignKey('DpeProductionElecEnr', models.DO_NOTHING, blank=True, null=True, db_column='production_elec_enr_id', db_index=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_panneaux_pv'


class DpePlancherBas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    b = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coefficient de réduction des déperditions du planchers_bas ')
    calcul_ue = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : est ce que le plancher bas est passé par le calcul du Ue 0 : non 1 : oui ')
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    enum_cfg_isolation_lnc_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : configuration de l'adjacence avec local non chauffé :  local chauffé (non) isolé/local non chauffé (non) isolé/orientation véranda qui permet de calculer le b  ")
    enum_methode_saisie_u0_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : methode de saisie de U0 (inclus les justifications à produire en cas de saisie directe) ')
    enum_methode_saisie_u_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : methode de saisie du U (inclus les justifications à produire en cas de saisie directe) ')
    enum_periode_isolation_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : periode d'isolation à saisir si différent de la période de construction (cas d'une rénovation de la paroi) ")
    enum_type_adjacence_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type d'adjacence de la paroi ")
    enum_type_isolation_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type d'isolation du plancher bas (ITI/ITE…..) ")
    enum_type_plancher_bas_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : type de plancher bas ')
    epaisseur_isolation = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : epaisseur de l'isolation (si plusieurs isolant différents sommer leurs épaisseurs) ")
    perimetre_ue = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : périmètredu plancher lorsqu'il est en contact avec un terre plein/sous sol non chauffé ou vide sanitaire (à renseigner lorsque calcul du Ue) ")
    resistance_isolation = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : resistance isolation ')
    surface_aiu = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : surface aiu : surface des parois du local non chauffé qui donnent sur des locaux chauffés. ')
    surface_aue = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface aue : surface des parois du local non chauffé en contact avec l'extérieur ou le sol ")
    surface_paroi_opaque = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Surface de paroi opaque  ')
    tv_coef_reduction_deperdition_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul de coefficient de reduction des déperditions ')
    tv_upb0_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de transmission thermique upb0 ')
    tv_upb_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de transmission thermique upb ')
    ue = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : Ue coefficient remplaçant Upb dans le cas sur terre plein ')
    upb = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : Coefficient de transmission thermique du planchers_bas Upb ')
    upb0 = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Coefficient de transmission thermique du planchers bas non isolé final  ')
    upb0_saisi = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : Coefficient de transmission thermique du planchers bas non isolé Saisi en direct par l'utilisateur (à justifier) ")
    upb_final = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : Coefficient de transmission thermique du planchers_bas (Ue ou Upb en fonction du type d'adjacence) ")
    upb_saisi = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : Coefficient de transmission thermique du planchers_bas saisi en direct par le diagnostiqueur(à justifier)  ')
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    surface_ue = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : surface de plancher qui est en contact avec un terre plein/sous sol non chauffé ou vide sanitaire (à renseigner lorsque calcul du Ue) ')
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    reference_lnc = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement | description : reference projet de l'objet  local non chauffé qui peut être associé à la paroi . Dans le cas d'un espace tampon solarisé cette référence est celle de l'espace tampon. ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_plancher_bas'


class DpePlancherHaut(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    b = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coefficient de réduction des déperditions du planchers_hauts ')
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    enum_cfg_isolation_lnc_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : configuration de l'adjacence avec local non chauffé :  local chauffé (non) isolé/local non chauffé (non) isolé/orientation véranda qui permet de calculer le b  ")
    enum_methode_saisie_u0_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : methode de saisie de U0 (inclus les justifications à produire en cas de saisie directe) ')
    enum_methode_saisie_u_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : methode de saisie du U (inclus les justifications à produire en cas de saisie directe) ')
    enum_periode_isolation_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : periode d'isolation à saisir si différent de la période de construction (cas d'une rénovation de la paroi) ")
    enum_type_adjacence_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type d'adjacence de la paroi ")
    enum_type_isolation_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type d'isolation du plancher haut (ITI/ITE…..) ")
    enum_type_plancher_haut_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : type de plancher haut ')
    epaisseur_isolation = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : epaisseur de l'isolation (si plusieurs isolant différents sommer leurs épaisseurs) ")
    resistance_isolation = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : resistance isolation ')
    surface_aiu = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : surface aiu : surface des parois du local non chauffé qui donnent sur des locaux chauffés. ')
    surface_aue = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface aue : surface des parois du local non chauffé en contact avec l'extérieur ou le sol ")
    surface_paroi_opaque = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Surface de paroi opaque  ')
    tv_coef_reduction_deperdition_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de reduction des deperditions ')
    tv_uph0_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de transmission thermique uph0 ')
    tv_uph_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de transmission thermique uph ')
    uph = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Coefficient de transmission thermique du planchers_hauts uph ')
    uph0 = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Coefficient de transmission thermique du planchers hauts non isolé final  ')
    uph0_saisi = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : Coefficient de transmission thermique du planchers hauts non isolé Saisi en direct par l'utilisateur (à justifier) ")
    uph_saisi = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : Coefficient de transmission thermique du planchers_hauts saisi en direct par le diagnostiqueur(à justifier)  ')
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    reference_lnc = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement | description : reference projet de l'objet  local non chauffé qui peut être associé à la paroi . Dans le cas d'un espace tampon solarisé cette référence est celle de l'espace tampon. ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_plancher_haut'


class DpePontThermique(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    enum_type_liaison_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : type de liaison de pont thermique ')
    k = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : valeur du pont thermique ')
    l = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : longueur du pont thermique ')
    tv_pont_thermique_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul de la valeur du pont thermique k  ')
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    enum_methode_saisie_pont_thermique_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : methode de saisie des ponts thermiques ')
    k_saisi = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : valeur du pont thermique saisie ')
    pourcentage_valeur_pont_thermique = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : pourcentage de prise en compte de la valeur du pont thermique (dans le cas des pont thermiques refend/mur et plancher intermediaire/mur cette valeur est à 0,5 au lieu de 1) ')
    reference_1 = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels. Pour les ponts thermique il est laissé la possibilité d'avoir 2 références correspondant aux référence de chacun des deux objets concernés par le pont thermique ")
    reference_2 = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels. Pour les ponts thermique il est laissé la possibilité d'avoir 2 références correspondant aux référence de chacun des deux objets concernés par le pont thermique ")
    reference = models.CharField(max_length=255, blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_pont_thermique'


class DpePorte(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    b = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coefficient de transmission thermique de la porte final : soit saisi directement soit issu des tables de valeurs forfaitaires ')
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    enum_cfg_isolation_lnc_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : configuration de l'adjacence avec local non chauffé :  local chauffé (non) isolé/local non chauffé (non) isolé/orientation véranda qui permet de calculer le b  ")
    enum_methode_saisie_uporte_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : méthode de saisie du U de la porte ')
    enum_type_adjacence_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : type d'adjacence de la paroi ")
    enum_type_porte_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : type de porte ')
    surface_aiu = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : surface aiu : surface des parois du local non chauffé qui donnent sur des locaux chauffés. ')
    surface_aue = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface aue : surface des parois du local non chauffé en contact avec l'extérieur ou le sol ")
    surface_porte = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : surface totale de portes déclaré (nb_porte x surface unitaire de porte dans le cas de plusieurs portes) ')
    tv_coef_reduction_deperdition_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de reduction des deperditions ')
    tv_uporte_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du coefficient de transfert thermique de la porte ')
    uporte = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : coefficient de transmission thermique de la porte final : soit saisi directement soit issu des tables de valeurs forfaitaires ')
    uporte_saisi = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : coefficient de transmission thermique de la porte saisi directement (nécessite une justification) ')
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    nb_porte = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : nombre de portes ')
    largeur_dormant = models.FloatField(blank=True, null=True)
    presence_retour_isolation = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : y a-t-il un retour d'isolant de la paroi opaque sur la porte 0 : non 1 : oui ")
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    reference_paroi = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet paroi qui est associé à l'objet porte. La codification et utilisation des références peut différer entre logiciels mais il devrait être attendu que reference_paroi est la référence d'une paroi de type mur,plancher_haut ou plancher_bas  ")
    enum_type_pose_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : type de pose de la porte ')
    reference_lnc = models.CharField(max_length=255, blank=True, null=True, db_comment=' modèle concerné : logement | description : référence commune pour un générateur mixte chauffage ECS. Cette référence est identique pour les deux parties du générateur (chauffage et ECS)  et est utilisé pour faire le lien entre les deux. ')
    presence_joint = models.IntegerField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_porte'


class DpeProductionElecEnr(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    conso_elec_ac = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : éléctricité photovoltaique autoconsommée (kWh) ')
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : description textuelle de l'objet ")
    enum_type_enr_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : enumérateur listant les systèmes de production d'éléctricité d'origine renouvelables présents dans le bâtiment  ")
    presence_production_pv = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : est ce qu'il y a de la production de photovoltaique renouvelable 0 : non 1 : oui ")
    production_pv = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : production d'éléctricité photovoltaique (kWh) ")
    taux_autoproduction = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : taux d'autoproduction Tap de la production d'éléctricité d'origne renouvelable ")
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_production_elec_enr'


class DpeProductionElectricite(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    conso_elec_ac = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement | description : éléctricité photovoltaique autoconsommée(kWhep/an) ')
    production_pv = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : production d'éléctricité photovoltaique(kWhep/an) ")
    conso_elec_ac_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : éléctricité photovoltaique autoconsommée pour l'usage chauffage (les consommations finales sont déduites de cette valeur) (kWhep/an) ")
    conso_elec_ac_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : éléctricité photovoltaique autoconsommée pour l'usage ecs (les consommations finales sont déduites de cette valeur) (kWhep/an) ")
    conso_elec_ac_fr = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : éléctricité photovoltaique autoconsommée pour l'usage climatisation (les consommations finales sont déduites de cette valeur) (kWhep/an) ")
    conso_elec_ac_eclairage = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : éléctricité photovoltaique autoconsommée pour l'usage eclairage (les consommations finales sont déduites de cette valeur) (kWhep/an) ")
    conso_elec_ac_auxiliaire = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : éléctricité photovoltaique autoconsommée pour l'usage auxiliaire (les consommations finales sont déduites de cette valeur) (kWhep/an) ")
    conso_elec_ac_autre_usage = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : éléctricité photovoltaique autoconsommée pour les autres usages de l'éléctricité  (kWhep/an) ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_production_electricite'


class DpeQualiteIsolation(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    qualite_isol_enveloppe = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : qualité d'isolation de l'enveloppe ")
    qualite_isol_menuiserie = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : qualité d'isolation des menuiseries ")
    qualite_isol_mur = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : qualité d'isolation des murs ")
    qualite_isol_plancher_bas = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : qualité de l'isolation des planchers ")
    ubat = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : Ubat(W/m²K) ')
    qualite_isol_plancher_haut_toit_terrasse = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : qualité d'isolation de la toiture/planchers hauts partie toit terrasse ")
    qualite_isol_plancher_haut_comble_amenage = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : qualité d'isolation de la toiture/planchers hauts partie comble aménagé ")
    qualite_isol_plancher_haut_comble_perdu = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement | description : qualité d'isolation de la toiture/planchers hauts partie comble perdue ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_qualite_isolation'


class DpeRepartitionChauffage(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    cle_repartition_ch = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement_neuf | description : clé de répartition de chauffage à appliquer au logement ')
    surface_baie_est_ouest = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement_neuf | description : surface des baies du logement orientées est ou ouest ')
    surface_baie_nord = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement_neuf | description : surface des baies du logement orientées nord ')
    surface_baie_sud = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement_neuf | description : surface des baies du logement orientées sud ')
    surface_plancher_bas = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement_neuf | description : surface des planchers bas du logement ')
    surface_plancher_haut = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement_neuf | description : surface des planchers hauts du logement ')
    surface_paroi_verticale_ext = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement_neuf | description : surface des parois verticales donnant sur l'extérieur ")
    coef_ifc = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement_neuf | description : coefficient d'individualisation des frais de chauffage dans le cas d'un DPE appartement calculé à partir d'un DPE immeuble ")
    deperdition_totale_logement = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement_neuf | description : calcul de deperdition logement pour de la clé de répartition de chauffage  ')
    deperdition_totale_batiment = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement_neuf | description : calcul de deperdition batiment pour de la clé de répartition de chauffage  ')
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_repartition_chauffage'


class DpeRepartitionEcs(models.Model):
    dpe_id = models.OneToOneField(Dpe, models.DO_NOTHING, db_column='dpe_id', primary_key=True)
    besoin_ecs_batiment = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement_neuf | description : besoin d'ECS du bâtiment calculé pour la clé de répartition d'ECS  ")
    besoin_ecs_logement = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement_neuf | description : besoin d'ECS du logement calculé pour la clé de répartition d'ECS ")
    cle_repartition_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement_neuf | description : clé de répartition de l'ECS ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_repartition_ecs'


class DpeSortieParEnergie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    conso_5_usages = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation totale en énergie finale pour l'énergie considérée (kWhef/an) ")
    conso_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation de chauffage en énergie finale pour l'énergie considérée (kWhef/an) ")
    conso_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : consommation d'ECS en énergie finale pour l'énergie considérée (kWhef/an) ")
    cout_5_usages = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : coût totale pour l'énergie considérée (€) ")
    cout_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : coût lié au chauffage pour l'énergie considérée (€) ")
    cout_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : coût  lié à l'ECS pour l'énergie considérée (€) ")
    emission_ges_5_usages = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : estimation GES totale pour l'énergie considérée (kgCO2/an) ")
    emission_ges_ch = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : estimation GES de chauffage pour l'énergie considérée (kgCO2/an) ")
    emission_ges_ecs = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : estimation GES d'ECS pour l'énergie considérée (kgCO2/an) ")
    enum_type_energie_id = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : type d'énergie ")
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_sortie_par_energie'





class DpeTvCoefMasqueLointainHomogene(models.Model):
    enum_orientation_id = models.TextField(blank=True, null=True)
    orientation = models.TextField(blank=True, null=True)
    hauteur_alpha = models.TextField(blank=True, null=True)
    fe2 = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_coef_masque_lointain_homogene'


class DpeTvCoefMasqueLointainNonHomoge(models.Model):
    secteur = models.TextField(blank=True, null=True)
    enum_orientation_id = models.TextField(blank=True, null=True)
    orientation = models.TextField(blank=True, null=True)
    omb = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_coef_masque_lointain_non_homoge'


class DpeTvCoefMasqueProche(models.Model):
    type_masque_proche = models.TextField(blank=True, null=True)
    avancee = models.TextField(blank=True, null=True)
    enum_orientation_id = models.TextField(blank=True, null=True)
    orientation = models.TextField(blank=True, null=True)
    fe1 = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_coef_masque_proche'


class DpeTvCoefOrientationPv(models.Model):
    enum_inclinaison_pv_id = models.TextField(blank=True, null=True)
    inclinaison_pv = models.TextField(blank=True, null=True)
    enum_orientation_pv_id = models.TextField(blank=True, null=True)
    orientation_pv = models.TextField(blank=True, null=True)
    coef_orientation_pv = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_coef_orientation_pv'


class DpeTvCoefReductionDeperdition(models.Model):
    enum_type_adjacence_id = models.TextField(blank=True, null=True)
    type_adjacence = models.TextField(blank=True, null=True)
    zone_climatique = models.TextField(blank=True, null=True)
    uvue = models.TextField(blank=True, null=True)
    enum_cfg_isolation_lnc_id = models.TextField(blank=True, null=True)
    cfg_isolation_lnc = models.TextField(blank=True, null=True)
    aiu_aue_min = models.TextField(blank=True, null=True)
    aiu_aue_max = models.TextField(blank=True, null=True)
    b = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_coef_reduction_deperdition'


class DpeTvCoefTransparenceEts(models.Model):
    enum_type_materiaux_menuiserie_id = models.TextField(blank=True, null=True)
    type_materiaux_menuiserie = models.TextField(blank=True, null=True)
    enum_type_vitrage_id = models.TextField(blank=True, null=True)
    type_vitrage = models.TextField(blank=True, null=True)
    vitrage_vir = models.TextField(blank=True, null=True)
    coef_transparence_ets = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_coef_transparence_ets'


class DpeTvDebitsVentilation(models.Model):
    enum_type_ventilation_id = models.TextField(blank=True, null=True)
    type_ventilation = models.TextField(blank=True, null=True)
    qvarep_conv = models.TextField(blank=True, null=True)
    qvasouf_conv = models.TextField(blank=True, null=True)
    smea_conv = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_debits_ventilation'


class DpeTvDeltar(models.Model):
    enum_type_fermeture_id = models.TextField(blank=True, null=True)
    type_fermeture = models.TextField(blank=True, null=True)
    deltar = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_deltar'


class DpeTvFacteurCouvertureSolaire(models.Model):
    enum_zone_climatique_id = models.TextField(blank=True, null=True)
    zone_climatique = models.TextField(blank=True, null=True)
    enum_type_installation_solaire_id = models.TextField(blank=True, null=True)
    type_installation_solaire = models.TextField(blank=True, null=True)
    type_batiment = models.TextField(blank=True, null=True)
    usage = models.TextField(blank=True, null=True)
    facteur_couverture_solaire = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_facteur_couverture_solaire'


class DpeTvGenerateurCombustion(models.Model):
    enum_type_generateur_ch_id = models.TextField(blank=True, null=True)
    enum_type_generateur_ecs_id = models.TextField(blank=True, null=True)
    type_generateur = models.TextField(blank=True, null=True)
    critere_pn = models.TextField(blank=True, null=True)
    pn = models.TextField(blank=True, null=True)
    rpn = models.TextField(blank=True, null=True)
    rpint = models.TextField(blank=True, null=True)
    qp0_perc = models.TextField(blank=True, null=True)
    pveil = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_generateur_combustion'


class DpeTvIntermittence(models.Model):
    enum_methode_application_dpe_log_id = models.TextField(blank=True, null=True)
    configuration_chauffage = models.TextField(blank=True, null=True)
    enum_type_installation_id = models.TextField(blank=True, null=True)
    enum_type_chauffage_id = models.TextField(blank=True, null=True)
    type_chauffage = models.TextField(blank=True, null=True)
    enum_equipement_intermittence_id = models.TextField(blank=True, null=True)
    equipement_intermittence = models.TextField(blank=True, null=True)
    enum_type_regulation_id = models.TextField(blank=True, null=True)
    type_regulation = models.TextField(blank=True, null=True)
    enum_type_emission_distribution_id = models.TextField(blank=True, null=True)
    type_emission_simple = models.TextField(blank=True, null=True)
    enum_classe_inertie_id = models.TextField(blank=True, null=True)
    inertie = models.TextField(blank=True, null=True)
    comptage_individuel = models.TextField(blank=True, null=True)
    i0 = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_intermittence'


class DpeTvPertesStockage(models.Model):
    enum_type_generateur_ecs_id = models.TextField(blank=True, null=True)
    type_generateur_ecs = models.TextField(blank=True, null=True)
    volume_ballon = models.TextField(blank=True, null=True)
    cr = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_pertes_stockage'


class DpeTvPontThermique(models.Model):
    enum_type_liaison_id = models.TextField(blank=True, null=True)
    type_liaison = models.TextField(blank=True, null=True)
    isolation_mur = models.TextField(blank=True, null=True)
    isolation_plancher = models.TextField(blank=True, null=True)
    presence_retour_isolation = models.TextField(blank=True, null=True)
    enum_type_pose_id = models.TextField(blank=True, null=True)
    type_pose = models.TextField(blank=True, null=True)
    largeur_dormant = models.TextField(blank=True, null=True)
    k = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_pont_thermique'


class DpeTvQ4PaConv(models.Model):
    enum_periode_construction_id = models.TextField(blank=True, null=True)
    periode_construction = models.TextField(blank=True, null=True)
    enum_methode_application_dpe_log_id = models.TextField(blank=True, null=True)
    presence_joints_menuiserie = models.TextField(blank=True, null=True)
    isolation_surfaces = models.TextField(blank=True, null=True)
    type_habitation = models.TextField(blank=True, null=True)
    q4pa_conv = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_q4pa_conv'


class DpeTvRendementDistributionCh(models.Model):
    enum_type_emission_distribution_id = models.TextField(blank=True, null=True)
    reseau_distribution = models.TextField(blank=True, null=True)
    reseau_distribution_isole = models.TextField(blank=True, null=True)
    rd = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_rendement_distribution_ch'


class DpeTvRendementDistributionEcs(models.Model):
    enum_type_installation_id = models.TextField(blank=True, null=True)
    type_installation = models.TextField(blank=True, null=True)
    configuration_logement = models.TextField(blank=True, null=True)
    type_reseau_collectif = models.TextField(blank=True, null=True)
    rd = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_rendement_distribution_ecs'


class DpeTvRendementEmission(models.Model):
    enum_type_emission_distribution_id = models.TextField(blank=True, null=True)
    type_emission = models.TextField(blank=True, null=True)
    re = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_rendement_emission'


class DpeTvRendementGeneration(models.Model):
    enum_type_generateur_ch_id = models.TextField(blank=True, null=True)
    type_generateur_ch = models.TextField(blank=True, null=True)
    rg = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_rendement_generation'


class DpeTvRendementRegulation(models.Model):
    enum_type_emission_distribution_id = models.TextField(blank=True, null=True)
    type_emission_regulation = models.TextField(blank=True, null=True)
    rr = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_rendement_regulation'


class DpeTvReseauChaleur2020(models.Model):
    departement = models.TextField(blank=True, null=True)
    hash_reseau = models.TextField(blank=True, null=True)
    nom_reseau = models.TextField(blank=True, null=True)
    localisation = models.TextField(blank=True, null=True)
    chaud_ou_froid = models.TextField(blank=True, null=True)
    contenu_co2 = models.TextField(blank=True, null=True)
    taux_enr = models.TextField(blank=True, null=True)
    est_vertueux = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_reseau_chaleur_2020'


class DpeTvReseauChaleur2021(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    departement = models.TextField(blank=True, null=True)
    nom_reseau = models.TextField(blank=True, null=True)
    localisation = models.TextField(blank=True, null=True)
    contenu_co2 = models.TextField(blank=True, null=True)
    contenu_co2_acv = models.TextField(blank=True, null=True)
    taux_enr = models.TextField(blank=True, null=True)
    methode_calcul_taux = models.TextField(blank=True, null=True)
    nouveau_reseau_2020_2021 = models.TextField(blank=True, null=True)
    correspondance_tv_reseau_chaleur_id_2020 = models.TextField(blank=True, null=True)
    correspondance_hash_reseau_2020 = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_reseau_chaleur_2021'


class DpeTvReseauChaleur2022(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    departement = models.TextField(blank=True, null=True)
    nom_reseau = models.TextField(blank=True, null=True)
    localisation = models.TextField(blank=True, null=True)
    contenu_co2 = models.TextField(blank=True, null=True)
    contenu_co2_acv = models.TextField(blank=True, null=True)
    taux_enr = models.TextField(blank=True, null=True)
    methode_calcul_taux = models.TextField(blank=True, null=True)
    nouveau_reseau_2021_2022 = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_reseau_chaleur_2022'


class DpeTvReseauChaleur2023(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    departement = models.TextField(blank=True, null=True)
    nom_reseau = models.TextField(blank=True, null=True)
    localisation = models.TextField(blank=True, null=True)
    contenu_co2 = models.TextField(blank=True, null=True)
    contenu_co2_acv = models.TextField(blank=True, null=True)
    taux_enr = models.TextField(blank=True, null=True)
    methode_calcul_taux = models.TextField(blank=True, null=True)
    nouveau_reseau_2022_2023 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_reseau_chaleur_2023'


class DpeTvScop(models.Model):
    enum_zone_climatique_id = models.TextField(blank=True, null=True)
    zone_climatique = models.TextField(blank=True, null=True)
    enum_generateur_ch_id = models.TextField(blank=True, null=True)
    enum_generateur_ecs_id = models.TextField(blank=True, null=True)
    type_generateur = models.TextField(blank=True, null=True)
    enum_type_emission_ditribution_id = models.TextField(blank=True, null=True)
    type_emetteur = models.TextField(blank=True, null=True)
    scop_ou_cop = models.TextField(blank=True, null=True)
    scop = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_scop'


class DpeTvSeer(models.Model):
    enum_periode_installation_fr_id = models.TextField(blank=True, null=True)
    periode_installation_fr = models.TextField(blank=True, null=True)
    enum_zone_climatique_id = models.TextField(blank=True, null=True)
    zone_climatique = models.TextField(blank=True, null=True)
    seer_ou_eer = models.TextField(blank=True, null=True)
    seer = models.TextField(blank=True, null=True)
    eer = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_seer'


class DpeTvSw(models.Model):
    enum_type_baie_id = models.TextField(blank=True, null=True)
    type_baie = models.TextField(blank=True, null=True)
    enum_type_materiaux_menuiserie_id = models.TextField(blank=True, null=True)
    type_materiaux_menuiserie = models.TextField(blank=True, null=True)
    enum_type_pose_id = models.TextField(blank=True, null=True)
    type_pose = models.TextField(blank=True, null=True)
    vitrage_vir = models.TextField(blank=True, null=True)
    enum_type_vitrage_id = models.TextField(blank=True, null=True)
    type_vitrage = models.TextField(blank=True, null=True)
    sw = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_sw'


class DpeTvTempFonc100(models.Model):
    enum_temp_distribution_ch_id = models.TextField(blank=True, null=True)
    temp_distribution_ch = models.TextField(blank=True, null=True)
    periode_emetteurs = models.TextField(blank=True, null=True)
    temp_fonc_100 = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_temp_fonc_100'


class DpeTvTempFonc30(models.Model):
    enum_temp_distribution_ch_id = models.TextField(blank=True, null=True)
    temp_distribution_ch = models.TextField(blank=True, null=True)
    periode_emetteurs = models.TextField(blank=True, null=True)
    enum_type_generateur_ch_id = models.TextField(blank=True, null=True)
    type_chaudiere = models.TextField(blank=True, null=True)
    temp_fonc_30 = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_temp_fonc_30'


class DpeTvTypeGenerateurCh(models.Model):
    lib = models.TextField(blank=True, null=True)
    calcul_combustion = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    enum_type_energie_id = models.TextField(blank=True, null=True)
    hors_methode = models.TextField(blank=True, null=True)
    rpn_sup_rpint = models.TextField(blank=True, null=True)
    position_probable_volume_chauffe = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_type_generateur_ch'


class DpeTvTypeGenerateurEcs(models.Model):
    lib = models.TextField(blank=True, null=True)
    variables_requises = models.TextField(blank=True, null=True)
    variables_interdites = models.TextField(blank=True, null=True)
    enum_type_energie_id = models.TextField(blank=True, null=True)
    hors_methode = models.TextField(blank=True, null=True)
    position_probable_volume_chauffe = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_type_generateur_ecs'


class DpeTvUe(models.Model):
    number_2s_p = models.TextField(db_column='2s_p', blank=True, null=True)  # Field renamed because it wasn't a valid Python identifier.
    upb = models.TextField(blank=True, null=True)
    type_adjacence_plancher = models.TextField(blank=True, null=True)
    ue = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_ue'


class DpeTvUg(models.Model):
    enum_type_gaz_lame_id = models.TextField(blank=True, null=True)
    type_gaz_lame = models.TextField(blank=True, null=True)
    enum_inclinaison_vitrage_id = models.TextField(blank=True, null=True)
    inclinaison_vitrage = models.TextField(blank=True, null=True)
    vitrage_vir = models.TextField(blank=True, null=True)
    epaisseur_lame = models.TextField(blank=True, null=True)
    enum_type_vitrage_id = models.TextField(blank=True, null=True)
    type_vitrage = models.TextField(blank=True, null=True)
    ug = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_ug'


class DpeTvUjn(models.Model):
    deltar = models.TextField(blank=True, null=True)
    uw = models.TextField(blank=True, null=True)
    ujn = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_ujn'


class DpeTvUmur(models.Model):
    enum_periode_construction_id = models.TextField(blank=True, null=True)
    periode_construction = models.TextField(blank=True, null=True)
    enum_zone_climatique_id = models.TextField(blank=True, null=True)
    zone_climatique = models.TextField(blank=True, null=True)
    effet_joule = models.TextField(blank=True, null=True)
    umur = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_umur'


class DpeTvUmur0(models.Model):
    enum_materiaux_structure_mur_id = models.TextField(blank=True, null=True)
    materiaux_structure_mur = models.TextField(blank=True, null=True)
    epaisseur_structure = models.TextField(blank=True, null=True)
    umur0 = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_umur0'


class DpeTvUpb(models.Model):
    enum_periode_construction_id = models.TextField(blank=True, null=True)
    periode_construction = models.TextField(blank=True, null=True)
    enum_zone_climatique_id = models.TextField(blank=True, null=True)
    zone_climatique = models.TextField(blank=True, null=True)
    effet_joule = models.TextField(blank=True, null=True)
    upb = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_upb'


class DpeTvUpb0(models.Model):
    enum_type_plancher_bas_id = models.TextField(blank=True, null=True)
    type_plancher_bas = models.TextField(blank=True, null=True)
    upb0 = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_upb0'


class DpeTvUph(models.Model):
    enum_periode_construction_id = models.TextField(blank=True, null=True)
    periode_construction = models.TextField(blank=True, null=True)
    enum_zone_climatique_id = models.TextField(blank=True, null=True)
    zone_climatique = models.TextField(blank=True, null=True)
    effet_joule = models.TextField(blank=True, null=True)
    type_toiture = models.TextField(blank=True, null=True)
    uph = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_uph'


class DpeTvUph0(models.Model):
    enum_type_plancher_haut_id = models.TextField(blank=True, null=True)
    type_plancher_haut = models.TextField(blank=True, null=True)
    uph0 = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_uph0'


class DpeTvUporte(models.Model):
    enum_type_porte_id = models.TextField(blank=True, null=True)
    type_porte = models.TextField(blank=True, null=True)
    uporte = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_uporte'


class DpeTvUvue(models.Model):
    enum_type_adjacence_id = models.TextField(blank=True, null=True)
    type_adjacence = models.TextField(blank=True, null=True)
    uvue = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_uvue'


class DpeTvUw(models.Model):
    enum_type_baie_id = models.TextField(blank=True, null=True)
    type_baie = models.TextField(blank=True, null=True)
    enum_type_materiaux_menuiserie_id = models.TextField(blank=True, null=True)
    type_materiaux_menuiserie = models.TextField(blank=True, null=True)
    ug = models.TextField(blank=True, null=True)
    uw = models.TextField(blank=True, null=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_tv_uw'


class DpeVentilation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    dpe_id = models.ForeignKey(Dpe, models.DO_NOTHING, db_column='dpe_id', db_index=True,  null=True, blank=True)
    conso_auxiliaire_ventilation = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : Consommation des auxilliaires de ventilation.  Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la consommation de l'installation à l'immeuble qu'il faut saisir. ")
    description = models.TextField(blank=True, null=True, db_comment=" modèle concerné : logement | description : description textuelle de l'objet ")
    enum_methode_saisie_q4pa_conv_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : code de la methode de saisie du q4paconv ')
    enum_type_ventilation_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : code du type de ventilation  ')
    hperm = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : déperdition thermique par renouvellement d'air due au vent ")
    hvent = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : déperdition thermique par renouvellement d'air due au système de ventilation ")
    plusieurs_facade_exposee = models.IntegerField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : est ce qu'il y a plusieurs facades exposées au vent 0 : non 1 : oui ")
    pvent_moy = models.FloatField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : puissance de la ventilation moyenne soit saisie soit calculée avec la méthode proposée ')
    q4pa_conv = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : q4pa conv final soit issue d'une saisie de mesure  à l'étanchéité à l'air soit d'une valeur forfaitaire. valeur conventionnelle de la perméabilité sous 4Pa (m3/(h.m2)) ")
    q4pa_conv_saisi = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : q4paconv saisi directement quand la valeur est donnée par une mesure d'étanchéité à l'air. valeur conventionnelle de la perméabilité sous 4Pa (m3/(h.m2)) ")
    ref_produit_ventilation = models.CharField(max_length=255, blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : référence produit  et marque du système de ventilation ')
    surface_ventile = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : surface ventilée. Dans le cas d'une seule ventilation c'est la surface habitable totale. Dans le cas d'un DPE immeuble ou d'un DPE appartement à partir de l'immeuble c'est la surface de l'installation à l'immeuble qu'il faut renseigner ")
    tv_debits_ventilation_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul des débits de ventilations ')
    tv_q4pa_conv_id = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement | description : id de la ligne de la table utilisée pour le calcul du q4pa conventionnel. valeur conventionnelle de la perméabilité sous 4Pa (m3/(h.m2)) ')
    ventilation_post_2012 = models.IntegerField(blank=True, null=True, db_comment=' modèle concerné : logement + logement neuf | description : est ce que le système de ventilation est postérieur à 2012 0 : non 1 : oui ')
    reference = models.CharField(max_length=255, blank=True, null=True, db_comment=" modèle concerné : logement + logement neuf | description : reference projet de l'objet (cette référence permet de faire d'éventuels liens entre objets). La codification et utilisation des références peut différer entre logiciels  ")
    cle_repartition_ventilation = models.FloatField(blank=True, null=True, db_comment=" modèle concerné : logement | description : clé de répartition pour passer des consommations bâtiments au consommation logement dans le cas DPE appartement calculé à partir du DPE immeuble UNIQUEMENT. Voir section 8.5.4 du document guide pour plus de détail. Pour la ventilation il s'agit du rapport surface habitable logement / surface habitable immeuble ")
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_ventilation'


class SeuilPetiteSurface(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    etiquette = models.TextField()
    surface_min = models.FloatField(blank=True, null=True)
    surface_max = models.FloatField(blank=True, null=True)
    pente_cep = models.FloatField()
    pente_ges = models.FloatField()
    ordonnee_origine_cep = models.FloatField()
    ordonnee_origine_ges = models.FloatField()
    altitude = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'seuil_petite_surface'


class ThematiqueContact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    objet = models.TextField()
    demande_ademe = models.BooleanField()
    email_destinataire = models.TextField(blank=True, null=True)
    email_destinataire_cci = models.TextField(blank=True, null=True)
    texte_informatif = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'thematique_contact'


class DpeBaieVitreeMasque(models.Model):
    id = models.BigAutoField(primary_key=True)
    baie_vitree_id = models.ForeignKey(DpeBaieVitree, models.DO_NOTHING, db_column='baie_vitree_id', blank=True, null=True, db_index=True)
    masque_id = models.ForeignKey(DpeMasqueLointainNonHomogene, models.DO_NOTHING,  db_column='masque_id', blank=True, null=True, db_index=True)
    date_derniere_modification = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'dpe_baie_vitree_masque'
        
