# dpe_json_db.py
# permet d'importer un DPE depuis un fichier JSON dans la base de données dpe ademe et galidpe
# dpe_json_to_db_ademe => vers db ademe
# dpe_json_to_db_json => vers db dpe_info et en option, conserver le json

import json
import uuid

from .dpe import get_float, get_int, get_text, get_date, sha256_file_hex, find_all_elements, delete_dpe, to_date, get_bool, get_nested, dpe_conso_lettre
from .models import *
from dpe.models import *

def dpe_json_to_db_ademe (data: str, num_ademe: str, xml_path = None, extended=True, delete_if_exist=True):
    """
    Importe les données DPE depuis un fichier JSON (et non plus XML).
    """

    print(f"Import ademe {num_ademe}")
      #Effacer le DPE si présent dans la base
    if delete_if_exist:
        delete_dpe(num_ademe)
        delete_dpe('')
        
    if isinstance(data, str):
        data = json.loads(data)
    # Récupération d'un DPE existant ou création
    dpe = Dpe.objects.filter(identifiant_dpe=num_ademe).first()
    if dpe:
        print(f"DPE existant, réutilisation de l'ID : {dpe.id}")
    else:
        dpe = Dpe()
        dpe.save()
        print(f"Nouveau DPE, ID : {dpe.id}")

    # Effacement des précédents
    #effacer_dpe_ademe('')
    #effacer_dpe_ademe(ademe)
    # Mise à jour des champs du Dpe
    dpe.date_etablissement_dpe = get_date(data, 'administratif.date_etablissement_dpe')
    dpe.version = get_text(data, 'administratif.date_etablissement_dpe')
    dpe.hashkey = get_text(data, 'hashkey')  # ou data.get('hashkey')
    dpe.identifiant_dpe = num_ademe

    dpe_a_remplacer = get_text(data, 'administratif.dpe_a_remplacer')
    if dpe_a_remplacer:
        ancien_dpe = Dpe.objects.filter(identifiant_dpe=dpe_a_remplacer).first()
        if ancien_dpe:
            ancien_dpe.desactive = 1
            ancien_dpe.dpe_remplacant_id = dpe.id
            ancien_dpe.save()
            dpe.ancien_dpe_id = str(ancien_dpe.id)

    dpe.date_reception_dpe = dpe.date_etablissement_dpe
    dpe.dpe_xml_path = xml_path  # on garde le champ, mais c'est du JSON
    dpe.version_moteur_used = get_text(data, 'administratif.diagnostiqueur.version_moteur_calcul')
    dpe.version_xsd_used = get_text(data, 'administratif.enum_version_id')
    dpe.statut = 1
    dpe.anonymise = 0
    dpe.migre_en_utc = 1
    dpe.is_dpe_2012 = 0
    dpe.xml_hash = sha256_file_hex(xml_path)
    dpe.save()

    # DpeAdministratif
    dpe_adm = DpeAdministratif(
        dpe_id=dpe,
        date_etablissement_dpe=get_date(data, 'administratif.date_etablissement_dpe'),
        date_visite_diagnostiqueur=get_date(data, 'administratif.date_visite_diagnostiqueur'),
        enum_modele_dpe_id=get_int(data, 'administratif.enum_modele_dpe_id'),
        dpe_a_remplacer=get_text(data, 'administratif.dpe_a_remplacer'),
        motif_remplacement=get_text(data, 'administratif.motif_remplacement'),
        date_fin_validite_dpe=get_date(data, 'administratif.date_fin_validite_dpe'),
        enum_version_id=get_text(data, 'administratif.enum_version_id'),
        dpe_immeuble_associe=get_text(data, 'administratif.dpe_immeuble_associe'),
        reference_interne_projet=get_text(data, 'administratif.reference_interne_projet'),
        date_derniere_modification=get_date(data, 'administratif.date_etablissement_dpe'),
    )
    dpe_adm.save()

    
    # DpeCaracteristiqueGenerale
    caracteristique_generale = DpeCaracteristiqueGenerale(
        dpe_id=dpe,
        # logement
        annee_construction=get_int(data, 'logement.caracteristique_generale.annee_construction'),
        enum_periode_construction_id=get_int(data, 'logement.caracteristique_generale.enum_periode_construction_id'),
        enum_methode_application_dpe_log_id=get_int(data, 'logement.caracteristique_generale.enum_methode_application_dpe_log_id'),
        enum_calcul_echantillonnage_id=get_int(data, 'logement.caracteristique_generale.enum_calcul_echantillonnage_id'),
        surface_habitable_logement=get_float(data, 'logement.caracteristique_generale.surface_habitable_logement'),
        nombre_niveau_immeuble=get_int(data, 'logement.caracteristique_generale.nombre_niveau_immeuble'),
        nombre_niveau_logement=get_int(data, 'logement.caracteristique_generale.nombre_niveau_logement'),
        hsp=get_float(data, 'logement.caracteristique_generale.hsp'),
        surface_habitable_immeuble=get_float(data, 'logement.caracteristique_generale.surface_habitable_immeuble'),
        surface_tertiaire_immeuble=get_float(data, 'logement.caracteristique_generale.surface_tertiaire_immeuble'),
        nombre_appartement=get_int(data, 'logement.caracteristique_generale.nombre_appartement'),
        appartement_non_visite=get_int(data, 'logement.caracteristique_generale.appartement_non_visite'),

        # tertiaire
        enum_categorie_erp_id=get_int(data, 'tertiaire.caracteristique_generale.enum_categorie_erp_id'),
        enum_usage_fonctionnel_batiment_id=get_int(data, 'tertiaire.caracteristique_generale.enum_usage_fonctionnel_batiment_id'),

        nombre_occupant=get_int(data, 'tertiaire.caracteristique_generale.nombre_occupant'),
        shon=get_text(data, 'tertiaire.caracteristique_generale.shon'),
        surface_utile=get_text(data, 'tertiaire.caracteristique_generale.surface_utile'),
        enum_methode_application_dpe_ter_id=get_int(data, 'tertiaire.caracteristique_generale.enum_methode_application_dpe_ter_id'),
        enum_sous_modele_dpe_ter_id=get_int(data, 'tertiaire.caracteristique_generale.enum_sous_modele_dpe_ter_id'),
    )
    caracteristique_generale.save()

    # DpeTAdresse
    adresse_bien = DpeTAdresse(
        adresse_brut=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.adresse_brut'),
        ban_city=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_city'),
        ban_citycode=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_citycode'),
        ban_date_appel=get_date(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_date_appel'),
        ban_housenumber=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_housenumber'),
        ban_id=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_id'),
        ban_label=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_label'),
        ban_postcode=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_postcode'),
        ban_score=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_score'),
        ban_street=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_street'),
        ban_type=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_type'),
        ban_x=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_x'),
        ban_y=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_y'),
        code_postal_brut=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.code_postal_brut'),
        compl_etage_appartement=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.compl_etage_appartement'),
        compl_nom_residence=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.compl_nom_residence'),
        compl_ref_batiment=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.compl_ref_batiment'),
        compl_ref_cage_escalier=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.compl_ref_cage_escalier'),
        compl_ref_logement=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.compl_ref_logement'),
        enum_statut_geocodage_ban_id=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.enum_statut_geocodage_ban_id'),
        label_brut=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.label_brut'),
        nom_commune_brut=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.nom_commune_brut'),
        ban_departement=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_departement'),
        ban_erreur=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_erreur'),
        ban_region=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_region'),
        traite_par_batch=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.traite_par_batch'),
        ban_epci=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_epci'),
        label_brut_avec_complement=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.label_brut_avec_complement'),
        migre_en_utc=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.migre_en_utc'),
        date_derniere_modification=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.date_derniere_modification'),
        is_dpe_2012=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.is_dpe_2012'),
        ban_id_ban_adresse=get_text(data, 'administratif.geolocalisation.adresses.adresse_bien.ban_id_ban_adresse'),
    )
    adresse_bien.save()

    geolocalisation = DpeGeolocalisation(
        administratif=dpe_adm,
        idpar=get_text(data, 'administratif.geolocalisation.idpar'),
        immatriculation_copropriete=get_text(data, 'administratif.geolocalisation.immatriculation_copropriete'),
        rpls_log_id=get_text(data, 'administratif.geolocalisation.rpls_log_id'),
        id_batiment_rnb=get_text(data, 'administratif.geolocalisation.id_batiment_rnb'),
        adresse_bien=adresse_bien
    )
    geolocalisation.save()

    meteo = DpeMeteo(
        dpe_id=dpe,
        enum_zone_climatique_id=get_int(data, 'logement.meteo.enum_zone_climatique_id'),
        batiment_materiaux_anciens=get_int(data, 'logement.meteo.batiment_materiaux_anciens'),
        enum_classe_altitude_id=get_int(data, 'logement.meteo.enum_classe_altitude_id'),
        altitude=get_float(data, 'logement.meteo.altitude'),
    )
    meteo.save()

    inertie = DpeInertie(
        dpe_id=dpe,
        enum_classe_inertie_id=get_int(data, 'logement.enveloppe.inertie.enum_classe_inertie_id'),
        inertie_paroi_verticale_lourd=get_int(data, 'logement.enveloppe.inertie.inertie_paroi_verticale_lourd'),
        inertie_plancher_bas_lourd=get_int(data, 'logement.enveloppe.inertie.inertie_plancher_bas_lourd'),
        inertie_plancher_haut_lourd=get_int(data, 'logement.enveloppe.inertie.inertie_plancher_haut_lourd'),
    )
    inertie.save()

    # Parcours des murs (ex-collection)
    elements = find_all_elements(data, 'logement.enveloppe.mur_collection.mur')
    for element in elements:
        mur = DpeMur(
            dpe_id=dpe,
            description=get_text(element, 'donnee_entree.description'),
            reference=get_text(element, 'donnee_entree.reference'),
            reference_lnc=get_text(element, 'donnee_entree.reference_lnc'),
            tv_coef_reduction_deperdition_id=get_int(element, 'donnee_entree.tv_coef_reduction_deperdition_id'),
            surface_aiu=get_float(element, 'donnee_entree.surface_aiu'),
            surface_aue=get_float(element, 'donnee_entree.surface_aue'),
            enum_cfg_isolation_lnc_id=get_int(element, 'donnee_entree.enum_cfg_isolation_lnc_id'),
            enum_type_adjacence_id=get_int(element, 'donnee_entree.enum_type_adjacence_id'),
            enum_orientation_id=get_int(element, 'donnee_entree.enum_orientation_id'),
            surface_paroi_totale=get_float(element, 'donnee_entree.surface_paroi_totale'),
            surface_paroi_opaque=get_float(element, 'donnee_entree.surface_paroi_opaque'),
            umur0_saisi=get_float(element, 'donnee_entree.umur0_saisi'),
            tv_umur0_id=get_int(element, 'donnee_entree.tv_umur0_id'),
            epaisseur_structure=get_float(element, 'donnee_entree.epaisseur_structure'),
            enum_materiaux_structure_mur_id=get_int(element, 'donnee_entree.enum_materiaux_structure_mur_id'),
            enum_methode_saisie_u0_id=get_int(element, 'donnee_entree.enum_methode_saisie_u0_id'),
            enduit_isolant_paroi_ancienne=get_int(element, 'donnee_entree.enduit_isolant_paroi_ancienne'),
            umur_saisi=get_float(element, 'donnee_entree.umur_saisi'),
            enum_type_doublage_id=get_int(element, 'donnee_entree.enum_type_doublage_id'),
            enum_type_isolation_id=get_int(element, 'donnee_entree.enum_type_isolation_id'),
            enum_periode_isolation_id=get_int(element, 'donnee_entree.enum_periode_isolation_id'),
            resistance_isolation=get_float(element, 'donnee_entree.resistance_isolation'),
            epaisseur_isolation=get_float(element, 'donnee_entree.epaisseur_isolation'),
            tv_umur_id=get_int(element, 'donnee_entree.tv_umur_id'),
            enum_methode_saisie_u_id=get_int(element, 'donnee_entree.enum_methode_saisie_u_id'),
            b=get_float(element, 'donnee_intermediaire.b'),
            umur=get_float(element, 'donnee_intermediaire.umur'),
            umur0=get_float(element, 'donnee_intermediaire.umur0'),
        )
        mur.save()
        
     # Parcours des plancher_bas (ex-collection)
    elements = find_all_elements(data, 'logement.enveloppe.plancher_bas_collection.plancher_bas')
    for element in elements:
        plancher = DpePlancherBas(
            dpe_id=dpe,
            description=get_text(element, 'donnee_entree.description'),
            reference=get_text(element, 'donnee_entree.reference'),
            reference_lnc=get_text(element, 'donnee_entree.reference_lnc'),
            tv_coef_reduction_deperdition_id=get_int(element, 'donnee_entree.tv_coef_reduction_deperdition_id'),
            surface_aiu=get_float(element, 'donnee_entree.surface_aiu'),
            surface_aue=get_float(element, 'donnee_entree.surface_aue'),
            enum_cfg_isolation_lnc_id=get_int(element, 'donnee_entree.enum_cfg_isolation_lnc_id'),
            enum_type_adjacence_id=get_int(element, 'donnee_entree.enum_type_adjacence_id'),
            surface_paroi_opaque=get_float(element, 'donnee_entree.surface_paroi_opaque'),
            upb0_saisi=get_float(element, 'donnee_entree.upb0_saisi'),
            tv_upb0_id=get_int(element, 'donnee_entree.tv_upb0_id'),
            enum_type_plancher_bas_id=get_int(element, 'donnee_entree.enum_type_plancher_bas_id'),
            enum_methode_saisie_u0_id=get_int(element, 'donnee_entree.enum_methode_saisie_u0_id'),
            upb_saisi=get_float(element, 'donnee_entree.upb_saisi'),
            enum_type_isolation_id=get_int(element, 'donnee_entree.enum_type_isolation_id'),
            enum_periode_isolation_id=get_int(element, 'donnee_entree.enum_periode_isolation_id'),
            resistance_isolation=get_float(element, 'donnee_entree.resistance_isolation'),
            tv_upb_id=get_int(element, 'donnee_entree.tv_upb_id'),
            enum_methode_saisie_u_id=get_int(element, 'donnee_entree.enum_methode_saisie_u_id'),
            calcul_ue=get_bool(element, 'donnee_entree.calcul_ue'),
            perimetre_ue=get_float(element, 'donnee_entree.perimetre_ue'),
            surface_ue=get_float(element, 'donnee_entree.surface_ue'),
            ue=get_float(element, 'donnee_entree.ue'),
            b=get_float(element, 'donnee_intermediaire.b'),
            upb=get_float(element, 'donnee_intermediaire.upb'),
            upb_final=get_float(element, 'donnee_intermediaire.upb_final'),
            upb0=get_float(element, 'donnee_intermediaire.upb0'),
        )
        plancher.save()
    
    
    # Parcours des plancher_haut (ex-collection)
    elements = find_all_elements(data, 'logement.enveloppe.plancher_haut_collection.plancher_haut')
    for element in elements:
        plafond = DpePlancherHaut(
            dpe_id=dpe,
            description=get_text(element, 'donnee_entree.description'),
            reference=get_text(element, 'donnee_entree.reference'),
            reference_lnc=get_text(element, 'donnee_entree.reference_lnc'),
            tv_coef_reduction_deperdition_id=get_int(element, 'donnee_entree.tv_coef_reduction_deperdition_id'),
            surface_aiu=get_float(element, 'donnee_entree.surface_aiu'),
            surface_aue=get_float(element, 'donnee_entree.surface_aue'),
            enum_cfg_isolation_lnc_id=get_int(element, 'donnee_entree.enum_cfg_isolation_lnc_id'),
            enum_type_adjacence_id=get_int(element, 'donnee_entree.enum_type_adjacence_id'),
            surface_paroi_opaque=get_float(element, 'donnee_entree.surface_paroi_opaque'),
            uph0_saisi=get_float(element, 'donnee_entree.uph0_saisi'),
            tv_uph0_id=get_int(element, 'donnee_entree.tv_uph0_id'),
            enum_type_plancher_haut_id=get_int(element, 'donnee_entree.enum_type_plancher_haut_id'),
            enum_methode_saisie_u0_id=get_int(element, 'donnee_entree.enum_methode_saisie_u0_id'),
            uph_saisi=get_float(element, 'donnee_entree.uph_saisi'),
            enum_type_isolation_id=get_int(element, 'donnee_entree.enum_type_isolation_id'),
            enum_periode_isolation_id=get_int(element, 'donnee_entree.enum_periode_isolation_id'),
            resistance_isolation=get_float(element, 'donnee_entree.resistance_isolation'),
            epaisseur_isolation=get_float(element, 'donnee_entree.epaisseur_isolation'),
            tv_uph_id=get_int(element, 'donnee_entree.tv_uph_id'),
            enum_methode_saisie_u_id=get_int(element, 'donnee_entree.enum_methode_saisie_u_id'),
            b=get_float(element, 'donnee_intermediaire.b'),
            uph=get_float(element, 'donnee_intermediaire.uph'),
            uph0=get_float(element, 'donnee_intermediaire.uph0'),
        )
        plafond.save()

    # Parcours des baie_vitree (ex-collection)
    elements_baies = find_all_elements(data, 'logement.enveloppe.baie_vitree_collection.baie_vitree')
    for element in elements_baies:
        baie = DpeBaieVitree(
            dpe_id=dpe,
            description=get_text(element, 'donnee_entree.description'),
            reference=get_text(element, 'donnee_entree.reference'),
            reference_paroi=get_text(element, 'donnee_entree.reference_paroi'),
            reference_lnc=get_text(element, 'donnee_entree.reference_lnc'),
            tv_coef_reduction_deperdition_id=get_int(element, 'donnee_entree.tv_coef_reduction_deperdition_id'),
            surface_aiu=get_float(element, 'donnee_entree.surface_aiu'),
            surface_aue=get_float(element, 'donnee_entree.surface_aue'),
            enum_cfg_isolation_lnc_id=get_int(element, 'donnee_entree.enum_cfg_isolation_lnc_id'),
            enum_type_adjacence_id=get_int(element, 'donnee_entree.enum_type_adjacence_id'),
            surface_totale_baie=get_float(element, 'donnee_entree.surface_totale_baie'),
            nb_baie=get_float(element, 'donnee_entree.nb_baie'),
            tv_ug_id=get_float(element, 'donnee_entree.tv_ug_id'),
            enum_type_vitrage_id=get_int(element, 'donnee_entree.enum_type_vitrage_id'),
            enum_inclinaison_vitrage_id=get_int(element, 'donnee_entree.enum_inclinaison_vitrage_id'),
            enum_type_gaz_lame_id=get_int(element, 'donnee_entree.enum_type_gaz_lame_id'),
            epaisseur_lame=get_float(element, 'donnee_entree.epaisseur_lame'),
            vitrage_vir=get_bool(element, 'donnee_entree.vitrage_vir'),
            enum_methode_saisie_perf_vitrage_id=get_int(element, 'donnee_entree.enum_methode_saisie_perf_vitrage_id'),
            ug_saisi=get_float(element, 'donnee_entree.ug_saisi'),
            tv_uw_id=get_float(element, 'donnee_entree.tv_uw_id'),
            enum_type_materiaux_menuiserie_id=get_int(element, 'donnee_entree.enum_type_materiaux_menuiserie_id'),
            enum_type_baie_id=get_int(element, 'donnee_entree.enum_type_baie_id'),
            uw_saisi=get_float(element, 'donnee_entree.uw_saisi'),
            double_fenetre=get_bool(element, 'donnee_entree.double_fenetre'),
            uw_1=get_float(element, 'donnee_entree.uw_1'),
            sw_1=get_float(element, 'donnee_entree.sw_1'),
            uw_2=get_float(element, 'donnee_entree.uw_2'),
            sw_2=get_float(element, 'donnee_entree.sw_2'),
            tv_deltar_id=get_int(element, 'donnee_entree.tv_deltar_id'),
            tv_ujn_id=get_int(element, 'donnee_entree.tv_ujn_id'),
            enum_type_fermeture_id=get_int(element, 'donnee_entree.enum_type_fermeture_id'),
            presence_protection_solaire_hors_fermeture=get_bool(element, 'donnee_entree.presence_protection_solaire_hors_fermeture'),
            ujn_saisi=get_float(element, 'donnee_entree.ujn_saisi'),
            presence_retour_isolation=get_bool(element, 'donnee_entree.presence_retour_isolation'),
            presence_joint=get_bool(element, 'donnee_entree.presence_joint'),
            largeur_dormant=get_float(element, 'donnee_entree.largeur_dormant'),
            tv_sw_id=get_int(element, 'donnee_entree.tv_sw_id'),
            sw_saisi=get_float(element, 'donnee_entree.sw_saisi'),
            enum_type_pose_id=get_int(element, 'donnee_entree.enum_type_pose_id'),
            enum_orientation_id=get_int(element, 'donnee_entree.enum_orientation_id'),
            tv_coef_masque_proche_id=get_int(element, 'donnee_entree.tv_coef_masque_proche_id'),
            tv_coef_masque_lointain_homogene_id=get_int(element, 'donnee_entree.tv_coef_masque_lointain_homogene_id'),

            b=get_float(element, 'donnee_intermediaire.b'),
            ug=get_float(element, 'donnee_intermediaire.ug'),
            ujn=get_float(element, 'donnee_intermediaire.ujn'),
            u_menuiserie=get_float(element, 'donnee_intermediaire.u_menuiserie'),
            sw=get_float(element, 'donnee_intermediaire.sw'),
            fe1=get_float(element, 'donnee_intermediaire.fe1'),
            fe2=get_float(element, 'donnee_intermediaire.fe2'),
        )
        baie.save()
        
        tv_coef_masque_lointain_non_homogene_id=get_int(element, 'donnee_entree/masque_lointain_non_homogene_collection/masque_lointain_non_homogene/tv_coef_masque_lointain_non_homogene_id'),        
        if tv_coef_masque_lointain_non_homogene_id is not None:
            masque_lointain = DpeMasqueLointainNonHomogene(
                tv_coef_masque_lointain_non_homogene_id=get_int(element, 'tv_coef_masque_lointain_non_homogene_id'),        
            )
            masque_lointain.save()
            
            masque = DpeBaieVitreeMasque(
                baie_vitree_id = baie,
                masque_id = masque_lointain
            )
            masque.save()
        
        val = get_nested(data, 'donnee_entree/baie_vitree_double_fenetre', default=None)
        if val is not None:
            double_fen = DpeBaieVitreeDoubleFenetre(
                baie_vitree_id=baie,
                tv_ug_id=get_int(val, 'donnee_entree/tv_ug_id'),      
                enum_type_vitrage_id=get_int(val, 'donnee_entree.enum_type_vitrage_id'),
                enum_inclinaison_vitrage_id=get_int(val, 'donnee_entree.enum_inclinaison_vitrage_id'),
                enum_type_gaz_lame_id=get_int(val, 'donnee_entree.enum_type_gaz_lame_id'),
                epaisseur_lame=get_float(val, 'donnee_entree.epaisseur_lame'),
                vitrage_vir=get_bool(val, 'donnee_entree.vitrage_vir'),
                enum_methode_saisie_perf_vitrage_id=get_int(val, 'donnee_entree.enum_methode_saisie_perf_vitrage_id'),
                ug_saisi=get_float(val, 'donnee_entree.ug_saisi'),
                tv_uw_id=get_int(val, 'donnee_entree.tv_uw_id'),
                enum_type_materiaux_menuiserie_id=get_int(val, 'donnee_entree.enum_type_materiaux_menuiserie_id'),
                enum_type_baie_id=get_int(val, 'donnee_entree.enum_type_baie_id'),
                uw_saisi=get_float(val, 'donnee_entree.uw_saisi'),
                tv_sw_id=get_float(val, 'donnee_entree.tv_sw_id'),
                sw_saisi=get_float(val, 'donnee_entree.sw_saisi'),
                enum_type_pose_id=get_int(val, 'donnee_entree.enum_type_pose_id'),
                ug=get_float(val, 'donnee_intermediaire.ug'),
                uw=get_float(val, 'donnee_intermediaire.uw'),
                sw=get_float(val, 'donnee_intermediaire.sw'),
            )
            double_fen.save()
            

    # Parcours des portes
    elements = find_all_elements(data, 'logement.enveloppe.porte_collection.porte')
    for element in elements:
        porte = DpePorte(
            dpe_id=dpe,
            description=get_text(element, 'donnee_entree.description'),
            reference=get_text(element, 'donnee_entree.reference'),
            reference_paroi=get_text(element, 'donnee_entree.reference_paroi'),
            reference_lnc=get_text(element, 'donnee_entree.reference_lnc'),
            enum_cfg_isolation_lnc_id=get_int(element, 'donnee_entree.enum_cfg_isolation_lnc_id'),
            
            enum_type_adjacence_id=get_int(element, 'donnee_entree.enum_type_adjacence_id'),
            tv_coef_reduction_deperdition_id=get_int(element, 'donnee_entree.tv_coef_reduction_deperdition_id'),
            
            surface_aiu=get_float(element, 'donnee_entree.surface_aiu'),
            surface_aue=get_float(element, 'donnee_entree.surface_aue'),
            surface_porte=get_float(element, 'donnee_entree.surface_porte'),
            tv_uporte_id=get_int(element, 'donnee_entree.tv_uporte_id'),
            enum_methode_saisie_uporte_id=get_int(element, 'donnee_entree.enum_methode_saisie_uporte_id'),
            enum_type_porte_id=get_int(element, 'donnee_entree.enum_type_porte_id'),
            uporte_saisi=get_float(element, 'donnee_entree.uporte_saisi'),
            nb_porte=get_float(element, 'donnee_entree.nb_porte'),
            largeur_dormant=get_float(element, 'donnee_entree.largeur_dormant'),
            presence_retour_isolation=get_bool(element, 'donnee_entree.presence_retour_isolation'),
            presence_joint=get_bool(element, 'donnee_entree.presence_joint'),
            enum_type_pose_id=get_int(element, 'donnee_entree.enum_type_pose_id'),
            b=get_float(element, 'donnee_intermediaire.b'),
            uporte=get_float(element, 'donnee_intermediaire.uporte'),
        )
        porte.save()
        
     # Parcours des ETS
    ets_collection = find_all_elements(data, 'logement.enveloppe.ets_collection.ets')
    for ets in ets_collection:
        db_ets = DpeEts(
            dpe_id=dpe,
            description=get_text(element, 'donnee_entree.description'),
            reference=get_text(element, 'donnee_entree.reference'),
            tv_coef_reduction_deperdition_id=get_int(element, 'donnee_entree.tv_coef_reduction_deperdition_id'),
            enum_cfg_isolation_lnc_id=get_int(element, 'donnee_entree.enum_cfg_isolation_lnc_id'),
            tv_coef_transparence_ets_id=get_int(element, 'donnee_entree.tv_coef_transparence_ets_id'),
            coef_transparence_ets=get_float(element, 'coef_transparence_ets.coef_transparence_ets'),
            bver=get_float(element, 'donnee_intermediaire.bver'),
        )
        db_ets.save()
        
        baie_ets_collection = find_all_elements(elements, 'baie_ets_collection.baie_ets')
        for baie_ets in baie_ets_collection:
            db_baie_ets = DpeBaieEts(
                ets_id = db_ets,
                description = get_text(baie_ets, 'donnee_entree.description'),
                reference = get_text(baie_ets, 'donnee_entree.reference'),
                enum_orientation_id=get_int(baie_ets, 'donnee_entree.enum_orientation_id'),
                enum_inclinaison_vitrage_id=get_int(baie_ets, 'donnee_entree.enum_inclinaison_vitrage_id'),
                surface_totale_baie=get_float(baie_ets, 'coef_transparence_ets.surface_totale_baie'),
                nb_baie=get_float(baie_ets, 'coef_transparence_ets.nb_baie'),
            )
            db_baie_ets.save()


    # Parcours des pont_thermique
    elements = find_all_elements(data, 'logement.enveloppe.pont_thermique_collection.pont_thermique')
    for element in elements:
        pont_thermique = DpePontThermique(
            dpe_id=dpe,
            description=get_text(element, 'donnee_entree.description'),
            reference=get_text(element, 'donnee_entree.reference'),
            reference_1=get_text(element, 'donnee_entree.reference_1'),
            reference_2=get_text(element, 'donnee_entree.reference_2'),
            tv_pont_thermique_id=get_int(element, 'donnee_entree.tv_pont_thermique_id'),
            pourcentage_valeur_pont_thermique=get_float(element, 'donnee_entree.pourcentage_valeur_pont_thermique'),
            l=get_float(element, 'donnee_entree.l'),
            enum_methode_saisie_pont_thermique_id=get_int(element, 'donnee_entree.enum_methode_saisie_pont_thermique_id'),
            enum_type_liaison_id=get_int(element, 'donnee_entree.enum_type_liaison_id'),
            k_saisi=get_float(element, 'donnee_entree.k_saisi'),
            k=get_float(element, 'donnee_intermediaire.k'),
        )
        pont_thermique.save()
     
    # Parcours des ventilation_collection
    elements = find_all_elements(data, 'logement.ventilation_collection.ventilation')
    for element in elements:
        ventilation = DpeVentilation(
            dpe_id=dpe,
            surface_ventile=get_text(element, 'donnee_entree.surface_ventile'),
            description=get_text(element, 'donnee_entree.description'),
            reference=get_text(element, 'donnee_entree.reference'),
            plusieurs_facade_exposee=get_bool(element, 'donnee_entree.plusieurs_facade_exposee'),
            tv_q4pa_conv_id=get_int(element, 'donnee_entree.tv_q4pa_conv_id'),
            q4pa_conv_saisi=get_float(element, 'donnee_entree.q4pa_conv_saisi'),
            enum_methode_saisie_q4pa_conv_id=get_int(element, 'donnee_entree.enum_methode_saisie_q4pa_conv_id'),
            tv_debits_ventilation_id=get_int(element, 'donnee_entree.tv_debits_ventilation_id'),
            enum_type_ventilation_id=get_int(element, 'donnee_entree.enum_type_ventilation_id'),
            ventilation_post_2012=get_bool(element, 'donnee_entree.ventilation_post_2012'),
            ref_produit_ventilation=get_text(element, 'donnee_entree.ref_produit_ventilation'),
            cle_repartition_ventilation=get_float(element, 'donnee_entree.cle_repartition_ventilation'),
            
            pvent_moy=get_float(element, 'donnee_intermediaire.pvent_moy'),
            q4pa_conv=get_float(element, 'donnee_intermediaire.q4pa_conv'),
            conso_auxiliaire_ventilation=get_float(element, 'donnee_intermediaire.conso_auxiliaire_ventilation'),
            hperm=get_float(element, 'donnee_intermediaire.hperm'),
            hvent=get_float(element, 'donnee_intermediaire.hvent'),
        )
        ventilation.save()
        
    # Parcours des climatisation
    elements = find_all_elements(data, 'logement.climatisation_collection.climatisation')
    for element in elements:
        climatisation = DpeClimatisation(
            dpe_id=dpe,
            description=get_text(element, 'donnee_entree.description'),
            reference=get_text(element, 'donnee_entree.reference'),
            surface_clim=get_text(element, 'donnee_entree.surface_clim'),
            tv_seer_id=get_float(element, 'donnee_entree.tv_seer_id'),
            nombre_logement_echantillon=get_float(element, 'donnee_entree.nombre_logement_echantillon'),
            enum_methode_calcul_conso_id=get_int(element, 'donnee_entree.enum_methode_calcul_conso_id'),
            enum_periode_installation_fr_id=get_int(element, 'donnee_entree.enum_periode_installation_fr_id'),
            cle_repartition_clim=get_float(element, 'donnee_entree.cle_repartition_clim'),
            enum_type_generateur_fr_id=get_int(element, 'donnee_entree.enum_type_generateur_fr_id'),
            enum_type_energie_id=get_int(element, 'donnee_entree.enum_type_energie_id'),
            enum_methode_saisie_carac_sys_id=get_int(element, 'donnee_entree.enum_methode_saisie_carac_sys_id'),
            ref_produit_fr=get_text(element, 'donnee_entree.ref_produit_fr'),
            
            eer=get_float(element, 'donnee_intermediaire.eer'),
            besoin_fr=get_float(element, 'donnee_intermediaire.besoin_fr'),
            conso_fr=get_float(element, 'donnee_intermediaire.conso_fr'),
            conso_fr_depensier=get_float(element, 'donnee_intermediaire.conso_fr_depensier'),
        )
        climatisation.save()
        
            
    # Parcours des production_elec_enr
    presence_production_pv=get_bool(data, 'logement.production_elec_enr.donnee_entree.presence_production_pv')

    if presence_production_pv is not None:
        print (f'presence_production_pv {presence_production_pv}')
        enr = DpeProductionElecEnr(
            dpe_id=dpe,
            description=get_text(data, 'logement.production_elec_enr.donnee_entree.description'),
            presence_production_pv=get_bool(data, 'logement.production_elec_enr.donnee_entree.presence_production_pv'),
            enum_type_enr_id=get_int(data, 'logement.production_elec_enr.donnee_entree.enum_type_enr_id'),
            taux_autoproduction=get_float(data, 'logement.production_elec_enr.donnee_intermediaire.taux_autoproduction'),
            production_pv=get_float(data, 'logement.production_elec_enr.donnee_intermediaire.production_pv'),
            conso_elec_ac=get_float(data, 'logement.production_elec_enr.donnee_intermediaire.conso_elec_ac'),
        )
        enr.save()
        
        panneaux_pv_collection = find_all_elements(data, 'logement.production_elec_enr.panneaux_pv_collection.panneaux_pv')
        for panneaux_pv in panneaux_pv_collection:
            panneau_pv = DpePanneauxPv(
                production_elec_enr_id = enr.id,
                surface_totale_capteurs=get_float(element, 'surface_totale_capteurs'),
                ratio_virtualisation=get_float(element, 'ratio_virtualisation'),
                nombre_module=get_int(element, 'nombre_module'),
                tv_coef_orientation_pv_id=get_int(element, 'tv_coef_orientation_pv_id'),
                enum_orientation_pv_id=get_int(element, 'enum_orientation_pv_id'),
                enum_inclinaison_pv_id=get_int(element, 'enum_inclinaison_pv_id'),
            )
            panneau_pv.save()
            
    # Parcours installation_ecs_collection climatisation
    elements = find_all_elements(data, 'logement.installation_ecs_collection.installation_ecs')
    
    for element in elements:
        installation_ecs = DpeInstallationEcs(
            dpe_id=dpe,
            description=get_text(element, 'donnee_entree.description'),
            enum_cfg_installation_ecs_id=get_int(element, 'donnee_entree.enum_cfg_installation_ecs_id'),
            enum_type_installation_id=get_int(element, 'donnee_entree.enum_type_installation_id'),
            enum_methode_calcul_conso_id=get_int(element, 'donnee_entree.enum_methode_calcul_conso_id'),
            ratio_virtualisation=get_float(element, 'donnee_entree.ratio_virtualisation'),
            cle_repartition_ecs=get_float(element, 'donnee_entree.cle_repartition_ecs'),
            surface_habitable=get_float(element, 'donnee_entree.surface_habitable'),
            nombre_logement=get_float(element, 'donnee_entree.nombre_logement'),
            rdim=get_float(element, 'donnee_entree.rdim'),
            nombre_niveau_installation_ecs=get_float(element, 'donnee_entree.nombre_niveau_installation_ecs'),
            fecs_saisi=get_float(element, 'donnee_entree.fecs_saisi'),
            tv_facteur_couverture_solaire_id=get_int(element, 'donnee_entree.tv_facteur_couverture_solaire_id'),
            enum_methode_saisie_fact_couv_sol_id=get_int(element, 'donnee_entree.enum_methode_saisie_fact_couv_sol_id'),
            enum_type_installation_solaire_id=get_int(element, 'donnee_entree.enum_type_installation_solaire_id'),
            tv_rendement_distribution_ecs_id=get_int(element, 'donnee_entree.tv_rendement_distribution_ecs_id'),
            enum_bouclage_reseau_ecs_id=get_int(element, 'donnee_entree.enum_bouclage_reseau_ecs_id'),
            reseau_distribution_isole=get_bool(element, 'donnee_entree.reseau_distribution_isole'),
            
            
            rendement_distribution=get_float(element, 'donnee_intermediaire.rendement_distribution'),
            besoin_ecs=get_float(element, 'donnee_intermediaire.besoin_ecs'),
            besoin_ecs_depensier=get_float(element, 'donnee_intermediaire.besoin_ecs_depensier'),
            fecs=get_float(element, 'donnee_intermediaire.fecs'),
            production_ecs_solaire=get_float(element, 'donnee_intermediaire.production_ecs_solaire'),
            conso_ecs_depensier=get_float(element, 'donnee_intermediaire.conso_ecs_depensier'),
        )
        installation_ecs.save()
        generateurs = find_all_elements(element, 'generateur_ecs_collection.generateur_ecs')
        
        for generateur in generateurs:
            generateur_ecs = DpeGenerateurEcs(
                installation_ecs_id = installation_ecs,
                description=get_text(generateur, 'donnee_entree.description'),
                
                reference=get_text(generateur, 'donnee_entree.reference'),
                reference_generateur_mixte=get_text(generateur, 'donnee_entree.reference_generateur_mixte'),
                enum_type_generateur_ecs_id=get_int(generateur, 'donnee_entree.enum_type_generateur_ecs_id'),
                ref_produit_generateur_ecs=get_text(generateur, 'donnee_entree.ref_produit_generateur_ecs'),
                enum_usage_generateur_id=get_int(generateur, 'donnee_entree.enum_usage_generateur_id'),
                enum_type_energie_id=get_int(generateur, 'donnee_entree.enum_type_energie_id'),
                tv_generateur_combustion_id=get_int(generateur, 'donnee_entree.tv_generateur_combustion_id'),
                enum_methode_saisie_carac_sys_id=get_int(generateur, 'donnee_entree.enum_methode_saisie_carac_sys_id'),
                tv_pertes_stockage_id=get_int(generateur, 'donnee_entree.tv_pertes_stockage_id'),
                tv_scop_id=get_int(generateur, 'donnee_entree.tv_scop_id'),
                enum_periode_installation_ecs_thermo_id=get_int(generateur, 'donnee_entree.enum_periode_installation_ecs_thermo_id'),
                identifiant_reseau_chaleur=get_text(generateur, 'donnee_entree.identifiant_reseau_chaleur'),
                date_arrete_reseau_chaleur=get_date(generateur, 'donnee_entree.date_arrete_reseau_chaleur'),
                tv_reseau_chaleur_id=get_int(generateur, 'donnee_entree.tv_reseau_chaleur_id'),
                enum_type_stockage_ecs_id=get_int(generateur, 'donnee_entree.enum_type_stockage_ecs_id'),
                position_volume_chauffe=get_bool(generateur, 'donnee_entree.position_volume_chauffe'),
                position_volume_chauffe_stockage=get_bool(generateur, 'donnee_entree.position_volume_chauffe_stockage'),
                volume_stockage=get_float(generateur, 'donnee_entree.volume_stockage'),
                presence_ventouse=get_bool(generateur, 'donnee_entree.presence_ventouse'),
                
                pn=get_float(generateur, 'donnee_intermediaire.pn'),
                qp0=get_float(generateur, 'donnee_intermediaire.qp0'),
                pveilleuse=get_float(generateur, 'donnee_intermediaire.pveilleuse'),
                rpn=get_float(generateur, 'donnee_intermediaire.rpn'),
                cop=get_float(generateur, 'donnee_intermediaire.cop'),
                ratio_besoin_ecs=get_float(generateur, 'donnee_intermediaire.ratio_besoin_ecs'),
                rendement_generation=get_float(generateur, 'donnee_intermediaire.rendement_generation'),
                rendement_generation_stockage=get_float(generateur, 'donnee_intermediaire.rendement_generation_stockage'),
                conso_ecs=get_float(generateur, 'donnee_intermediaire.conso_ecs'),
                conso_ecs_depensier=get_float(generateur, 'donnee_intermediaire.conso_ecs_depensier'),
                rendement_stockage=get_float(generateur, 'donnee_intermediaire.rendement_stockage'),
            )
            generateur_ecs.save()
            dpe.generateur_ecs_principal_id = generateur_ecs
        
    # Parcours installation_ecs_collection climatisation
    installation_chauffage_collection = find_all_elements(data, 'logement.installation_chauffage_collection.installation_chauffage')
    for installation_chauffage in installation_chauffage_collection:
        db_installation_chauffage = DpeInstallationChauffage(
            dpe_id=dpe,
            description=get_text(installation_chauffage, 'donnee_entree.description'),
            reference=get_text(installation_chauffage, 'donnee_entree.reference'),
            surface_chauffee=get_float(installation_chauffage, 'donnee_entree.surface_chauffee'),
            nombre_logement_echantillon=get_float(installation_chauffage, 'donnee_entree.nombre_logement_echantillon'),
            rdim=get_float(installation_chauffage, 'donnee_entree.rdim'),
            nombre_niveau_installation_ch=get_float(installation_chauffage, 'donnee_entree.nombre_niveau_installation_ch'),
            enum_cfg_installation_ch_id=get_int(installation_chauffage, 'donnee_entree.enum_cfg_installation_ch_id'),
            ratio_virtualisation=get_float(installation_chauffage, 'donnee_entree.ratio_virtualisation'),
            coef_ifc=get_float(installation_chauffage, 'donnee_entree.coef_ifc'),
            cle_repartition_ch=get_float(installation_chauffage, 'donnee_entree.cle_repartition_ch'),
            enum_methode_calcul_conso_id=get_int(installation_chauffage, 'donnee_entree.enum_methode_calcul_conso_id'),
            enum_type_installation_id=get_int(installation_chauffage, 'donnee_entree.enum_type_installation_id'),
            enum_methode_saisie_fact_couv_sol_id=get_int(installation_chauffage, 'donnee_entree.enum_methode_saisie_fact_couv_sol_id'),
            tv_facteur_couverture_solaire_id=get_int(installation_chauffage, 'donnee_entree.tv_facteur_couverture_solaire_id'),
            fch_saisi=get_float(installation_chauffage, 'donnee_entree.fch_saisi'),
            
            besoin_ch=get_float(installation_chauffage, 'donnee_intermediaire.besoin_ch'),
            besoin_ch_depensier=get_float(installation_chauffage, 'donnee_intermediaire.besoin_ch_depensier'),
            production_ch_solaire=get_float(installation_chauffage, 'donnee_intermediaire.production_ch_solaire'),
            fch=get_float(installation_chauffage, 'donnee_intermediaire.fch'),
            conso_ch=get_float(installation_chauffage, 'donnee_intermediaire.conso_ch'),
            conso_ch_depensier=get_float(installation_chauffage, 'donnee_intermediaire.conso_ch_depensier'),
        )
        db_installation_chauffage.save()
        emetteur_chauffage_collection = find_all_elements(installation_chauffage, 'emetteur_chauffage_collection.emetteur_chauffage')
        for emetteur_chauffage in emetteur_chauffage_collection:
            db_emetteur_chauffage = DpeEmetteurChauffage(
                installation_chauffage_id = db_installation_chauffage,
                description=get_text(emetteur_chauffage, 'donnee_entree.description'),
                reference=get_text(emetteur_chauffage, 'donnee_entree.reference'),
                surface_chauffee=get_float(emetteur_chauffage, 'donnee_entree.surface_chauffee'),
                tv_rendement_emission_id=get_int(emetteur_chauffage, 'donnee_entree.tv_rendement_emission_id'),
                tv_rendement_distribution_ch_id=get_int(emetteur_chauffage, 'donnee_entree.tv_rendement_distribution_ch_id'),
                tv_rendement_regulation_id=get_int(emetteur_chauffage, 'donnee_entree.tv_rendement_regulation_id'),
                enum_type_emission_distribution_id=get_int(emetteur_chauffage, 'donnee_entree.enum_type_emission_distribution_id'),
                tv_intermittence_id=get_int(emetteur_chauffage, 'donnee_entree.tv_intermittence_id'),
                reseau_distribution_isole=get_bool(emetteur_chauffage, 'donnee_entree.reseau_distribution_isole'),
                enum_equipement_intermittence_id=get_int(emetteur_chauffage, 'donnee_entree.enum_equipement_intermittence_id'),
                enum_type_regulation_id=get_int(emetteur_chauffage, 'donnee_entree.enum_type_regulation_id'),
                enum_periode_installation_emetteur_id=get_int(emetteur_chauffage, 'donnee_entree.enum_periode_installation_emetteur_id'),
                enum_type_chauffage_id=get_int(emetteur_chauffage, 'donnee_entree.enum_type_chauffage_id'),
                enum_temp_distribution_ch_id=get_int(emetteur_chauffage, 'donnee_entree.enum_temp_distribution_ch_id'),
                enum_lien_generateur_emetteur_id=get_int(emetteur_chauffage, 'donnee_entree.enum_lien_generateur_emetteur_id'),
                
                i0=get_float(emetteur_chauffage, 'donnee_entree.i0'),
                rendement_emission=get_float(emetteur_chauffage, 'donnee_entree.rendement_emission'),
                rendement_distribution=get_float(emetteur_chauffage, 'donnee_entree.rendement_distribution'),
                rendement_regulation=get_float(emetteur_chauffage, 'donnee_entree.rendement_regulation'),
            )
            db_emetteur_chauffage.save()
        generateur_chauffage_collection = find_all_elements(installation_chauffage, 'generateur_chauffage_collection.generateur_chauffage')
        for generateur_chauffage in generateur_chauffage_collection:
            db_generateur_chauffage = DpeGenerateurChauffage(
                installation_chauffage_id = db_installation_chauffage,
                description=get_text(generateur_chauffage, 'donnee_entree.description'),
                reference=get_text(generateur_chauffage, 'donnee_entree.reference'),
                reference_generateur_mixte=get_text(generateur_chauffage, 'donnee_entree.reference_generateur_mixte'),
                ref_produit_generateur_ch=get_text(generateur_chauffage, 'donnee_entree.ref_produit_generateur_ch'),
                enum_type_generateur_ch_id=get_int(generateur_chauffage, 'donnee_entree.enum_type_generateur_ch_id'),
                enum_usage_generateur_id=get_int(generateur_chauffage, 'donnee_entree.enum_usage_generateur_id'),
                enum_type_energie_id=get_int(generateur_chauffage, 'donnee_entree.enum_type_energie_id'),
                position_volume_chauffe=get_bool(generateur_chauffage, 'donnee_entree.position_volume_chauffe'),
                tv_rendement_generation_id=get_int(generateur_chauffage, 'donnee_entree.tv_rendement_generation_id'),
                tv_scop_id=get_int(generateur_chauffage, 'donnee_entree.tv_scop_id'),
                tv_temp_fonc_100_id=get_int(generateur_chauffage, 'donnee_entree.tv_temp_fonc_100_id'),
                tv_temp_fonc_30_id=get_int(generateur_chauffage, 'donnee_entree.tv_temp_fonc_30_id'),
                tv_generateur_combustion_id=get_int(generateur_chauffage, 'donnee_entree.tv_generateur_combustion_id'),
                tv_reseau_chaleur_id=get_int(generateur_chauffage, 'donnee_entree.tv_reseau_chaleur_id'),
                identifiant_reseau_chaleur=get_int(generateur_chauffage, 'donnee_entree.identifiant_reseau_chaleur'),
                date_arrete_reseau_chaleur=get_date(generateur_chauffage, 'donnee_entree.date_arrete_reseau_chaleur'),
                n_radiateurs_gaz=get_int(generateur_chauffage, 'donnee_entree.n_radiateurs_gaz'),
                priorite_generateur_cascade=get_int(generateur_chauffage, 'donnee_entree.priorite_generateur_cascade'),
                presence_ventouse=get_bool(generateur_chauffage, 'donnee_entree.presence_ventouse'),
                presence_regulation_combustion=get_bool(generateur_chauffage, 'donnee_entree.presence_regulation_combustion'),
                enum_methode_saisie_carac_sys_id=get_int(generateur_chauffage, 'donnee_entree.enum_methode_saisie_carac_sys_id'),
                enum_lien_generateur_emetteur_id=get_int(generateur_chauffage, 'donnee_entree.enum_lien_generateur_emetteur_id'),

                scop=get_float(generateur_chauffage, 'donnee_intermediaire.scop'),
                pn=get_float(generateur_chauffage, 'donnee_intermediaire.pn'),
                qp0=get_float(generateur_chauffage, 'donnee_intermediaire.qp0'),
                pveilleuse=get_float(generateur_chauffage, 'donnee_intermediaire.pveilleuse'),
                temp_fonc_30=get_float(generateur_chauffage, 'donnee_intermediaire.temp_fonc_30'),
                temp_fonc_100=get_float(generateur_chauffage, 'donnee_intermediaire.temp_fonc_100'),
                rpn=get_float(generateur_chauffage, 'donnee_intermediaire.rpn'),
                rpint=get_float(generateur_chauffage, 'donnee_intermediaire.rpint'),
                rendement_generation=get_float(generateur_chauffage, 'donnee_intermediaire.rendement_generation'),
                conso_ch=get_float(generateur_chauffage, 'donnee_intermediaire.conso_ch'),
                conso_ch_depensier=get_float(generateur_chauffage, 'donnee_intermediaire.conso_ch_depensier'),
            )
            db_generateur_chauffage.save()

    deperdition = DpeDeperdition(
        dpe_id=dpe,
        hvent=get_float(data, 'logement.sortie.deperdition.hvent'),
        hperm=get_float(data, 'logement.sortie.deperdition.hperm'),
        deperdition_renouvellement_air=get_float(data, 'logement.sortie.deperdition.deperdition_renouvellement_air'),
        deperdition_mur=get_float(data, 'logement.sortie.deperdition.deperdition_mur'),
        deperdition_plancher_bas=get_float(data, 'logement.sortie.deperdition.deperdition_plancher_bas'),
        deperdition_plancher_haut=get_float(data, 'logement.sortie.deperdition.deperdition_plancher_haut'),
        deperdition_baie_vitree=get_float(data, 'logement.sortie.deperdition.deperdition_baie_vitree'),
        deperdition_porte=get_float(data, 'logement.sortie.deperdition.deperdition_porte'),
        deperdition_pont_thermique=get_float(data, 'logement.sortie.deperdition.deperdition_pont_thermique'),
        deperdition_enveloppe=get_float(data, 'logement.sortie.deperdition.deperdition_enveloppe'),
    )
    deperdition.save()
    
    apport_et_besoin = DpeApportEtBesoin(
        dpe_id=dpe,
        surface_sud_equivalente=get_float(data, 'logement.sortie.apport_et_besoin.surface_sud_equivalente'),
        apport_solaire_fr=get_float(data, 'logement.sortie.apport_et_besoin.apport_solaire_fr'),
        apport_interne_fr=get_float(data, 'logement.sortie.apport_et_besoin.apport_interne_fr'),
        apport_solaire_ch=get_float(data, 'logement.sortie.apport_et_besoin.apport_solaire_ch'),
        apport_interne_ch=get_float(data, 'logement.sortie.apport_et_besoin.apport_interne_ch'),
        fraction_apport_gratuit_ch=get_float(data, 'logement.sortie.apport_et_besoin.fraction_apport_gratuit_ch'),
        fraction_apport_gratuit_depensier_ch=get_float(data, 'logement.sortie.apport_et_besoin.fraction_apport_gratuit_depensier_ch'),
        pertes_distribution_ecs_recup=get_float(data, 'logement.sortie.apport_et_besoin.pertes_distribution_ecs_recup'),
        pertes_distribution_ecs_recup_depensier=get_float(data, 'logement.sortie.apport_et_besoin.pertes_distribution_ecs_recup_depensier'),
        pertes_stockage_ecs_recup=get_float(data, 'logement.sortie.apport_et_besoin.pertes_stockage_ecs_recup'),
        pertes_generateur_ch_recup=get_float(data, 'logement.sortie.apport_et_besoin.pertes_generateur_ch_recup'),
        pertes_generateur_ch_recup_depensier=get_float(data, 'logement.sortie.apport_et_besoin.pertes_generateur_ch_recup_depensier'),
        nadeq=get_float(data, 'logement.sortie.apport_et_besoin.nadeq'),
        v40_ecs_journalier=get_float(data, 'logement.sortie.apport_et_besoin.v40_ecs_journalier'),
        v40_ecs_journalier_depensier=get_float(data, 'logement.sortie.apport_et_besoin.v40_ecs_journalier_depensier'),
        besoin_ch=get_float(data, 'logement.sortie.apport_et_besoin.besoin_ch'),
        besoin_ch_depensier=get_float(data, 'logement.sortie.apport_et_besoin.besoin_ch_depensier'),
        besoin_ecs=get_float(data, 'logement.sortie.apport_et_besoin.besoin_ecs'),
        besoin_ecs_depensier=get_float(data, 'logement.sortie.apport_et_besoin.besoin_ecs_depensier'),
        besoin_fr=get_float(data, 'logement.sortie.apport_et_besoin.besoin_fr'),
        besoin_fr_depensier=get_float(data, 'logement.sortie.apport_et_besoin.besoin_fr_depensier'),
    )
    apport_et_besoin.save()
    
    ef_conso = DpeEfConso(
        dpe_id=dpe,
        conso_ch=get_float(data, 'logement.sortie.ef_conso.conso_ch'),
        conso_ch_depensier=get_float(data, 'logement.sortie.ef_conso.conso_ch_depensier'),
        conso_ecs=get_float(data, 'logement.sortie.ef_conso.conso_ecs'),
        conso_ecs_depensier=get_float(data, 'logement.sortie.ef_conso.conso_ecs_depensier'),
        conso_eclairage=get_float(data, 'logement.sortie.ef_conso.conso_eclairage'),
        conso_auxiliaire_generation_ch=get_float(data, 'logement.sortie.ef_conso.conso_auxiliaire_generation_ch'),
        conso_auxiliaire_generation_ch_depensier=get_float(data, 'logement.sortie.ef_conso.conso_auxiliaire_generation_ch_depensier'),
        conso_auxiliaire_distribution_ch=get_float(data, 'logement.sortie.ef_conso.conso_auxiliaire_distribution_ch'),
        conso_auxiliaire_generation_ecs=get_float(data, 'logement.sortie.ef_conso.conso_auxiliaire_generation_ecs'),
        conso_auxiliaire_generation_ecs_depensier=get_float(data, 'logement.sortie.ef_conso.conso_auxiliaire_generation_ecs_depensier'),
        conso_auxiliaire_distribution_ecs=get_float(data, 'logement.sortie.ef_conso.conso_auxiliaire_distribution_ecs'),
        conso_auxiliaire_distribution_fr=get_float(data, 'logement.sortie.ef_conso.conso_auxiliaire_distribution_fr'),
        conso_auxiliaire_ventilation=get_float(data, 'logement.sortie.ef_conso.conso_auxiliaire_ventilation'),
        conso_totale_auxiliaire=get_float(data, 'logement.sortie.ef_conso.conso_totale_auxiliaire'),
        conso_fr=get_float(data, 'logement.sortie.ef_conso.conso_fr'),
        conso_fr_depensier=get_float(data, 'logement.sortie.ef_conso.conso_fr_depensier'),
        conso_5_usages=get_float(data, 'logement.sortie.ef_conso.conso_5_usages'),
        conso_5_usages_m2=get_float(data, 'logement.sortie.ef_conso.conso_5_usages_m2'),
    )
    ef_conso.save()
    
    
    
    ep_conso = DpeEpConso(
        dpe_id=dpe,
        ep_conso_ch=get_float(data, 'logement.sortie.ep_conso.ep_conso_ch'),
        ep_conso_ch_depensier=get_float(data, 'logement.sortie.ep_conso.ep_conso_ch_depensier'),
        ep_conso_ecs=get_float(data, 'logement.sortie.ep_conso.ep_conso_ecs'),
        ep_conso_ecs_depensier=get_float(data, 'logement.sortie.ep_conso.ep_conso_ecs_depensier'),
        ep_conso_eclairage=get_float(data, 'logement.sortie.ep_conso.ep_conso_eclairage'),
        ep_conso_auxiliaire_generation_ch=get_float(data, 'logement.sortie.ep_conso.ep_conso_auxiliaire_generation_ch'),
        ep_conso_auxiliaire_generation_ch_depensier=get_float(data, 'logement.sortie.ep_conso.ep_conso_auxiliaire_generation_ch_depensier'),
        ep_conso_auxiliaire_distribution_ch=get_float(data, 'logement.sortie.ep_conso.ep_conso_auxiliaire_distribution_ch'),
        ep_conso_auxiliaire_generation_ecs=get_float(data, 'logement.sortie.ep_conso.ep_conso_auxiliaire_generation_ecs'),
        ep_conso_auxiliaire_generation_ecs_depensier=get_float(data, 'logement.sortie.ep_conso.ep_conso_auxiliaire_generation_ecs_depensier'),
        ep_conso_auxiliaire_distribution_ecs=get_float(data, 'logement.sortie.ep_conso.ep_conso_auxiliaire_distribution_ecs'),
        ep_conso_auxiliaire_distribution_fr=get_float(data, 'logement.sortie.ep_conso.ep_conso_auxiliaire_distribution_fr'),
        ep_conso_auxiliaire_ventilation=get_float(data, 'logement.sortie.ep_conso.ep_conso_auxiliaire_ventilation'),
        ep_conso_totale_auxiliaire=get_float(data, 'logement.sortie.ep_conso.ep_conso_totale_auxiliaire'),
        ep_conso_fr=get_float(data, 'logement.sortie.ep_conso.ep_conso_fr'),
        ep_conso_fr_depensier=get_float(data, 'logement.sortie.ep_conso.ep_conso_fr_depensier'),
        ep_conso_5_usages=get_float(data, 'logement.sortie.ep_conso.ep_conso_5_usages'),
        ep_conso_5_usages_m2=get_float(data, 'logement.sortie.ep_conso.ep_conso_5_usages_m2'),
        classe_bilan_dpe=get_float(data, 'logement.sortie.ep_conso.classe_bilan_dpe'),
    )
    ep_conso.save()
    
    
    emission_ges = DpeEmissionGes(
        dpe_id=dpe,
        emission_ges_ch=get_float(data, 'logement.sortie.emission_ges.emission_ges_ch'),
        emission_ges_ch_depensier=get_float(data, 'logement.sortie.emission_ges.emission_ges_ch_depensier'),
        emission_ges_ecs=get_float(data, 'logement.sortie.emission_ges.emission_ges_ecs'),
        emission_ges_ecs_depensier=get_float(data, 'logement.sortie.emission_ges.emission_ges_ecs_depensier'),
        emission_ges_eclairage=get_float(data, 'logement.sortie.emission_ges.emission_ges_eclairage'),
        emission_ges_auxiliaire_generation_ch=get_float(data, 'logement.sortie.emission_ges.emission_ges_auxiliaire_generation_ch'),
        emission_ges_auxiliaire_generation_ch_depensier=get_float(data, 'logement.sortie.emission_ges.emission_ges_auxiliaire_generation_ch_depensier'),
        emission_ges_auxiliaire_distribution_ch=get_float(data, 'logement.sortie.emission_ges.emission_ges_auxiliaire_distribution_ch'),
        emission_ges_auxiliaire_generation_ecs=get_float(data, 'logement.sortie.emission_ges.emission_ges_auxiliaire_generation_ecs'),
        emission_ges_auxiliaire_generation_ecs_depensier=get_float(data, 'logement.sortie.emission_ges.emission_ges_auxiliaire_generation_ecs_depensier'),
        emission_ges_auxiliaire_distribution_ecs=get_float(data, 'logement.sortie.emission_ges.emission_ges_auxiliaire_distribution_ecs'),
        emission_ges_auxiliaire_distribution_fr=get_float(data, 'logement.sortie.emission_ges.emission_ges_auxiliaire_distribution_fr'),
        emission_ges_auxiliaire_ventilation=get_float(data, 'logement.sortie.emission_ges.emission_ges_auxiliaire_ventilation'),
        emission_ges_totale_auxiliaire=get_float(data, 'logement.sortie.emission_ges.emission_ges_totale_auxiliaire'),
        emission_ges_fr=get_float(data, 'logement.sortie.emission_ges.emission_ges_fr'),
        emission_ges_fr_depensier=get_float(data, 'logement.sortie.emission_ges.emission_ges_fr_depensier'),
        emission_ges_5_usages=get_float(data, 'logement.sortie.emission_ges.emission_ges_5_usages'),
        emission_ges_5_usages_m2=get_float(data, 'logement.sortie.emission_ges.emission_ges_5_usages_m2'),
        classe_emission_ges=get_text(data, 'logement.sortie.emission_ges.classe_emission_ges'),
    )
    emission_ges.save()
 
    cout = DpeCout(
        dpe_id=dpe,
        cout_ch=get_float(data, 'logement.sortie.cout.cout_ch'),
        cout_ch_depensier=get_float(data, 'logement.sortie.cout.cout_ch_depensier'),
        cout_ecs=get_float(data, 'logement.sortie.cout.cout_ecs'),
        cout_ecs_depensier=get_float(data, 'logement.sortie.cout.cout_ecs_depensier'),
        cout_eclairage=get_float(data, 'logement.sortie.cout.cout_eclairage'),
        cout_auxiliaire_generation_ch=get_float(data, 'logement.sortie.cout.cout_auxiliaire_generation_ch'),
        cout_auxiliaire_generation_ch_depensier=get_float(data, 'logement.sortie.cout.cout_auxiliaire_generation_ch_depensier'),
        cout_auxiliaire_distribution_ch=get_float(data, 'logement.sortie.cout.cout_auxiliaire_distribution_ch'),
        cout_auxiliaire_generation_ecs=get_float(data, 'logement.sortie.cout.cout_auxiliaire_generation_ecs'),
        cout_auxiliaire_generation_ecs_depensier=get_float(data, 'logement.sortie.cout.cout_auxiliaire_generation_ecs_depensier'),
        cout_auxiliaire_distribution_ecs=get_float(data, 'logement.sortie.cout.cout_auxiliaire_distribution_ecs'),
        cout_auxiliaire_distribution_fr=get_float(data, 'logement.sortie.cout.cout_auxiliaire_distribution_fr'),
        cout_auxiliaire_ventilation=get_float(data, 'logement.sortie.cout.cout_auxiliaire_ventilation'),
        cout_total_auxiliaire=get_float(data, 'logement.sortie.cout.cout_total_auxiliaire'),
        cout_fr=get_float(data, 'logement.sortie.cout.cout_fr'),
        cout_fr_depensier=get_float(data, 'logement.sortie.cout.cout_fr_depensier'),
        cout_5_usages=get_float(data, 'logement.sortie.cout.cout_5_usages'),
    )
    cout.save()
               
    production_electricite = DpeProductionElectricite(
        dpe_id=dpe,
        production_pv=get_float(data, 'logement.sortie.production_electricite.production_pv'),
        conso_elec_ac=get_float(data, 'logement.sortie.production_electricite.conso_elec_ac'),
        conso_elec_ac_ch=get_float(data, 'logement.sortie.production_electricite.conso_elec_ac_ch'),
        conso_elec_ac_ecs=get_float(data, 'logement.sortie.production_electricite.conso_elec_ac_ecs'),
        conso_elec_ac_fr=get_float(data, 'logement.sortie.production_electricite.conso_elec_ac_fr'),
        conso_elec_ac_eclairage=get_float(data, 'logement.sortie.production_electricite.conso_elec_ac_eclairage'),
        conso_elec_ac_auxiliaire=get_float(data, 'logement.sortie.production_electricite.conso_elec_ac_auxiliaire'),
        conso_elec_ac_autre_usage=get_float(data, 'logement.sortie.production_electricite.conso_elec_ac_autre_usage'),
    )
    production_electricite.save()
    
    sortie_par_energie_collection = find_all_elements(data, 'logement.sortie.sortie_par_energie_collection.sortie_par_energie')
    for sortie_par_energie in sortie_par_energie_collection:
        db_sortie_par_energie = DpeSortieParEnergie(
            dpe_id = dpe,
            enum_type_energie_id=get_int(sortie_par_energie, 'enum_type_energie_id'),
            conso_ch=get_float(sortie_par_energie, 'conso_ch'),
            conso_ecs=get_float(sortie_par_energie, 'conso_ecs'),
            conso_5_usages=get_float(sortie_par_energie, 'conso_5_usages'),
            emission_ges_ch=get_float(sortie_par_energie, 'emission_ges_ch'),
            emission_ges_ecs=get_float(sortie_par_energie, 'emission_ges_ecs'),
            emission_ges_5_usages=get_float(sortie_par_energie, 'emission_ges_5_usages'),
            cout_ch=get_float(sortie_par_energie, 'cout_ch'),
            cout_ecs=get_float(sortie_par_energie, 'cout_ecs'),
            cout_5_usages=get_float(sortie_par_energie, 'cout_5_usages'),
        )
        db_sortie_par_energie.save()
    
    if get_nested(data, 'logement.sortie.confort_ete'):
        confort_ete = DpeConfortEte(
            dpe_id=dpe,
            isolation_toiture=get_bool(data, 'logement.sortie.confort_ete.isolation_toiture'),
            protection_solaire_exterieure=get_bool(data, 'logement.sortie.confort_ete.protection_solaire_exterieure'),
            aspect_traversant=get_bool(data, 'logement.sortie.confort_ete.aspect_traversant'),
            brasseur_air=get_bool(data, 'logement.sortie.confort_ete.brasseur_air'),
            inertie_lourde=get_bool(data, 'logement.sortie.confort_ete.inertie_lourde'),
            enum_indicateur_confort_ete_id=get_int(data, 'logement.sortie.confort_ete.enum_indicateur_confort_ete_id'),
        )
        confort_ete.save()
    
    qualite_isolation = DpeQualiteIsolation(
        dpe_id=dpe,
        ubat=get_float(data, 'logement.sortie.qualite_isolation.ubat'),
        qualite_isol_enveloppe=get_text(data, 'logement.sortie.qualite_isolation.qualite_isol_enveloppe'),
        qualite_isol_mur=get_text(data, 'logement.sortie.qualite_isolation.qualite_isol_mur'),
        qualite_isol_plancher_haut_toit_terrasse=get_text(data, 'logement.sortie.qualite_isolation.qualite_isol_plancher_haut_toit_terrasse'),
        qualite_isol_plancher_haut_comble_perdu=get_text(data, 'logement.sortie.qualite_isolation.qualite_isol_plancher_haut_comble_perdu'),
        qualite_isol_plancher_haut_comble_amenage=get_text(data, 'logement.sortie.qualite_isolation.qualite_isol_plancher_haut_comble_amenage'),
        qualite_isol_plancher_bas=get_text(data, 'logement.sortie.qualite_isolation.qualite_isol_plancher_bas'),
        qualite_isol_menuiserie=get_text(data, 'logement.sortie.qualite_isolation.qualite_isol_menuiserie'),
    )
    production_electricite.save()
    
    # descriptif_enr_collection
    descriptif_enr_collection = find_all_elements(data, 'descriptif_enr_collection.descriptif_enr')
    for descriptif_enr in descriptif_enr_collection:
        db_descriptif_enr = DpeDescriptifEnr(
            dpe_id = dpe,
            description=get_text(descriptif_enr, 'descriptif_enr.description'),
            enum_categorie_enr_descriptif_id=get_int(descriptif_enr, 'descriptif_enr.enum_categorie_enr_descriptif_id'),
        )
        db_descriptif_enr.save()
    
    # descriptif_simplifie_collection
    descriptif_simplifie_collection = find_all_elements(data, 'descriptif_simplifie_collection.descriptif_simplifie')
    for descriptif_simplifie in descriptif_simplifie_collection:
        db_descriptif_simplifie = DpeDescriptifSimplifie(
            dpe_id = dpe,
            description=get_text(descriptif_simplifie, 'descriptif_simplifie.description'),
            enum_categorie_descriptif_simplifie_id=get_int(descriptif_simplifie, 'descriptif_simplifie.enum_categorie_descriptif_simplifie_id'),
        )
        db_descriptif_simplifie.save()
    
    
    # fiche_technique_collection
    fiche_technique_collection = find_all_elements(data, 'fiche_technique_collection.fiche_technique')
    for fiche_technique in fiche_technique_collection:
        db_fiche_technique = DpeFicheTechnique(
            dpe_id = dpe,
            enum_categorie_fiche_technique_id=get_int(fiche_technique, 'enum_categorie_fiche_technique_id'),
        )
        db_fiche_technique.save()
        
        sous_fiche_technique_collection = find_all_elements(fiche_technique, 'sous_fiche_technique_collection.sous_fiche_technique')
        for sous_fiche_technique in sous_fiche_technique_collection:
            db_sous_fiche_technique = DpeSousFicheTechnique(
                dpe_id = dpe,
                fiche_technique_id = db_fiche_technique,
                description=get_text(sous_fiche_technique, 'sous_fiche_technique.description'),
                valeur=get_text(sous_fiche_technique, 'sous_fiche_technique.valeur'),
                detail_origine_donnee=get_text(sous_fiche_technique, 'sous_fiche_technique.detail_origine_donnee', 255),
                enum_origine_donnee_id=get_int(sous_fiche_technique, 'sous_fiche_technique.enum_origine_donnee_id'),
            )
            db_sous_fiche_technique.save()
    
    
    # justificatif
    justificatif_collection = find_all_elements(data, 'justificatif_collection.justificatif')
    for justificatif in justificatif_collection:
        db_justificatif = DpeJustificatif(
            dpe_id = dpe,
            description=get_text(justificatif, 'justificatif.description'),
            enum_type_justificatif_id=get_int(justificatif, 'justificatif.enum_type_justificatif_id'),
        )
        db_justificatif.save()
    
    
    # descriptif_geste_entretien
    descriptif_geste_entretien_collection = find_all_elements(data, 'descriptif_geste_entretien_collection.justificatif_collection')
    for descriptif_geste_entretien in descriptif_geste_entretien_collection:
        db_geste_entretien = DpeGesteEntretien(
            dpe_id = dpe,
            description=get_text(descriptif_geste_entretien, 'descriptif_geste_entretien.description'),
            enum_picto_geste_entretien_id=get_int(descriptif_geste_entretien, 'descriptif_geste_entretien.enum_picto_geste_entretien_id'),
            categorie_geste_entretien=get_text(descriptif_geste_entretien, 'descriptif_geste_entretien.categorie_geste_entretien', 255),
        )
        db_geste_entretien.save()
    
    # pack_travaux
    pack_travaux_collection = find_all_elements(data, 'descriptif_travaux.pack_travaux_collection.pack_travaux')
    for pack_travaux in pack_travaux_collection:
        db_pack_travaux = DpePackTravaux(
            dpe_id = dpe,
            enum_num_pack_travaux_id=get_int(pack_travaux, 'pack_travaux.enum_num_pack_travaux_id'),
            conso_5_usages_apres_travaux=get_float(pack_travaux, 'pack_travaux.conso_5_usages_apres_travaux'),
            emission_ges_5_usages_apres_travaux=get_float(pack_travaux, 'pack_travaux.emission_ges_5_usages_apres_travaux'),
            cout_pack_travaux_min=get_float(pack_travaux, 'pack_travaux.cout_pack_travaux_min'),
            cout_pack_travaux_max=get_float(pack_travaux, 'pack_travaux.cout_pack_travaux_max'),
        )
        db_pack_travaux.save()
        
        travaux_collection = find_all_elements(pack_travaux, 'travaux_collection.travaux')
        for travaux in travaux_collection:
            db_travaux = DpeTravaux(
                dpe_id = dpe,
                pack_travaux_id = db_pack_travaux,
                description_travaux=get_text(travaux, 'travaux.description_travaux'),
                enum_lot_travaux_id=get_int(travaux, 'travaux.enum_lot_travaux_id'),
                avertissement_travaux=get_text(travaux, 'travaux.avertissement_travaux', 255),
                performance_recommande=get_text(travaux, 'travaux.performance_recommande', 255),
            )
            db_travaux.save()
    
        
    dpe.save()
    if not extended:
        return

    surface_habitable_logement=get_float(data, 'logement.caracteristique_generale.surface_habitable_logement')
    conso_val=get_float(data, 'logement.sortie.ep_conso.ep_conso_5_usages_m2')
    conso_lettre=dpe_conso_lettre(conso_val)
    classe = get_float(data, 'logement.sortie.ep_conso.classe_bilan_dpe')
    ges_val=get_float(data, 'logement.sortie.emission_ges.emission_ges_5_usages_m2')
    ges_lettre=get_float(data, 'logement.sortie.emission_ges.classe_emission_ges')

    infos = GaliDpeInfos(
        dpe_id=dpe,
        ademe=num_ademe,
        surface_habitable_logement=surface_habitable_logement,
        conso_val=conso_val,
        conso_lettre=conso_lettre,
        classe = classe,
        ges_val=ges_val,
        ges_lettre=ges_lettre,
        depot_source=str(xml_path)[:1000],
        usr_logiciel_id=get_text(data, 'administratif.diagnostiqueur.usr_logiciel_id', 100),
        version_logiciel=get_text(data, 'administratif.diagnostiqueur.version_logiciel', 100),
        version_moteur_calcul=get_text(data, 'administratif.diagnostiqueur.version_moteur_calcul', 100),
        nom_diagnostiqueur=get_text(data, 'administratif.diagnostiqueur.nom_diagnostiqueur', 100),
        prenom_diagnostiqueur=get_text(data, 'administratif.diagnostiqueur.prenom_diagnostiqueur', 100),
        mail_diagnostiqueur=get_text(data, 'administratif.diagnostiqueur.mail_diagnostiqueur', 100),
        telephone_diagnostiqueur=get_text(data, 'administratif.diagnostiqueur.telephone_diagnostiqueur', 100),
        adresse_diagnostiqueur=get_text(data, 'administratif.diagnostiqueur.adresse_diagnostiqueur', 100),
        entreprise_diagnostiqueur=get_text(data, 'administratif.diagnostiqueur.entreprise_diagnostiqueur', 100),
        numero_certification_diagnostiqueur=get_text(data, 'administratif.diagnostiqueur.numero_certification_diagnostiqueur', 100),
        organisme_certificateur=get_text(data, 'administratif.diagnostiqueur.organisme_certificateur', 100),
        invar_logement=get_text(data, 'administratif.geolocalisation.invar_logement', 100),
        numero_fiscal_local=get_text(data, 'administratif.geolocalisation.numero_fiscal_local', 100),
        rpls_org_id=get_text(data, 'administratif.geolocalisation.rpls_org_id', 100),
        enum_consentement_formulaire_id=get_text(data, 'administratif.enum_consentement_formulaire_id', 100),
        nom_formulaire=get_text(data, 'administratif.nom_formulaire', 100),
        personne_morale=get_text(data, 'administratif.personne_morale', 100),
        siren_formulaire=get_text(data, 'administratif.siren_formulaire', 100),
        telephone=get_text(data, 'administratif.telephone', 100),
        mail=get_text(data, 'administratif.mail', 100),
        label_adresse=get_text(data, 'administratif.label_adresse', 100),
        label_adresse_avec_complement=get_text(data, 'administratif.label_adresse_avec_complement', 100),
        commentaire_travaux=get_text(data, 'descriptif_travaux.commentaire_travaux', 1000),
    )
    infos.save()


# La fonction effacer_dpe_ademe reste la même si elle ne dépend pas de l'entrée XML/JSON
# On la réutilise telle quelle, ou on la copie-colle ici.
