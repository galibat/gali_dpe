# galidpe/utils/import_dpe_xml.py

# permet de transformer des donénes de la base de données ademe en json compatible avec le moteur 3cl

import hashlib
import xml.etree.ElementTree as ET
from dpe.models import *
from django.utils.dateparse import parse_date
import json
from .dpe import date_json, to_dpe_json
from galidpe.models import *



def to_int(value, default=None):
    """
    Convertit une valeur en entier.
    - None, '' ou valeur invalide retourne `default`.
    """
    if value is None:
        return default
    try:
        return int(str(value).strip())
    except (ValueError, TypeError):
        return default


def to_text(value, default=None):
    """
    Convertit une valeur en chaîne de caractères.
    - None ou valeur vide retourne `default`.
    """
    if value is None:
        return default
    return str(value).strip()

def model_instance_to_json(instance, exclude_fields=None):
    """
    Convertit une instance Django ORM en un dictionnaire JSON.
    Les champs commençant par 'enum' sont automatiquement convertis via .to_int().
    """
    if instance is None:
        return None
    
    if exclude_fields is None:
        exclude_fields = {'id', 'dpe', 'dpe_id'}

    result = {}
    for field in instance._meta.get_fields():
        name = field.name
        if name in exclude_fields:
            continue

        value = getattr(instance, name)

        # Appelle to_int() si le champ commence par 'enum'
        if name.startswith('enum') and value is not None:
            try:
                value = to_int(value)
            except AttributeError:
                pass  # on laisse tel quel si .to_int() n'existe pas

        result[name] = value
    return result


def dpe_db_to_json (ademe, extended=True):
    dpe = (
        Dpe.objects
        .filter(identifiant_dpe=ademe, is_dpe_2012=False)
        .first()
    )
    if not dpe:
        print(f'DPE {ademe} non trouvé')
        return None

    # Construction d’un dictionnaire exportable en JSON
    infos = GaliDpeInfo.objects.filter(ademe=ademe).first()
    
    administratif = (
        DpeAdministratif.objects
        .filter(dpe_id=dpe)
        .first()
    )
    
    dpe_data = {
        'id': str(dpe.id),
        'identifiant_dpe': dpe.identifiant_dpe,
        'dpe': {}
    }
    
    if administratif:
        
        diagnostiqueur = (
            GaliDpeDiagnostiqueur.objects
            .filter(id=infos.diagnostiqueur)
            .first()
        )
        if diagnostiqueur:
            diagnostiqueur_info = {
                'usr_logiciel_id' : diagnostiqueur.usr_logiciel_id,
                'version_logiciel' : diagnostiqueur.version_logiciel ,
                'version_moteur_calcul' : diagnostiqueur.version_moteur_calcul ,
                'nom_diagnostiqueur'  : diagnostiqueur.nom_diagnostiqueur ,
                'prenom_diagnostiqueur'  : diagnostiqueur.prenom_diagnostiqueur ,
                'mail_diagnostiqueur' : diagnostiqueur.mail_diagnostiqueur ,
                'telephone_diagnostiqueur' : diagnostiqueur.telephone_diagnostiqueur ,
                'adresse_diagnostiqueur'  : diagnostiqueur.adresse_diagnostiqueur ,
                'entreprise_diagnostiqueur'  : diagnostiqueur.entreprise_diagnostiqueur ,
                'numero_certification_diagnostiqueur' : diagnostiqueur.numero_certification_diagnostiqueur ,
                'organisme_certificateur'  : diagnostiqueur.organisme_certificateur ,
            }
        else :
            diagnostiqueur_info = {}
    
        dpe_data['administratif'] = {
            'dpe_a_remplacer': administratif.dpe_a_remplacer,
            'reference_interne_projet': administratif.reference_interne_projet,
            'motif_remplacement': administratif.motif_remplacement,
            'dpe_immeuble_associe': administratif.dpe_immeuble_associe,
            'enum_version_id': administratif.enum_version_id,
            'date_visite_diagnostiqueur': administratif.date_visite_diagnostiqueur,

            'date_etablissement_dpe': administratif.date_etablissement_dpe,
            'enum_modele_dpe_id': administratif.enum_modele_dpe_id,
            'diagnostiqueur' :diagnostiqueur_info ,
        }
        
    geolocalisation = DpeGeolocalisation.objects.filter(administratif_id=administratif).first() 
    if geolocalisation:
        dpe_data['administratif']['geolocalisation'] = {
                'id_batiment_rnb' : geolocalisation.id_batiment_rnb,
                'rpls_log_id' : geolocalisation.rpls_log_id,
                'idpar' : geolocalisation.idpar,
                'immatriculation_copropriete' : geolocalisation.immatriculation_copropriete,
            }
        print (f"adresse_bien_id : {geolocalisation.adresse_bien_id}")
        adresse_bien = geolocalisation.adresse_bien_id
        if adresse_bien:
            dpe_data['administratif']['geolocalisation']['adresses'] = {}
            dpe_data['administratif']['geolocalisation']['adresses']['adresse_bien'] = {
                'adresse_brut': adresse_bien.adresse_brut,
                'ban_city': adresse_bien.ban_city,
                'adreban_citycodesse_brut': adresse_bien.ban_citycode,
                'ban_date_appel': adresse_bien.ban_date_appel,
                'ban_housenumber': adresse_bien.ban_housenumber,
                'ban_id': adresse_bien.ban_id,
                'ban_label': adresse_bien.ban_label,
                'ban_postcode': adresse_bien.ban_postcode,
                'ban_score': adresse_bien.ban_score,
                'ban_street': adresse_bien.ban_street,
                'ban_type': adresse_bien.ban_type,
                'ban_x': adresse_bien.ban_x,
                'ban_y': adresse_bien.ban_y,
                'code_postal_brut': adresse_bien.code_postal_brut,
                'compl_etage_appartement': adresse_bien.compl_etage_appartement,
                'compl_nom_residence': adresse_bien.compl_nom_residence,
                'compl_ref_batiment': adresse_bien.compl_ref_batiment,
                'compl_ref_cage_escalier': adresse_bien.compl_ref_cage_escalier,
                'compl_ref_logement': adresse_bien.compl_ref_logement,
                'enum_statut_geocodage_ban_id': adresse_bien.enum_statut_geocodage_ban_id,
                'label_brut': adresse_bien.label_brut,
                'nom_commune_brut': adresse_bien.nom_commune_brut,
                'ban_departement': adresse_bien.ban_departement,
                'ban_erreur': adresse_bien.ban_erreur,
                'ban_region': adresse_bien.ban_region,
                'traite_par_batch': adresse_bien.traite_par_batch,
                'ban_epci': adresse_bien.ban_epci,
                'label_brut_avec_complement': adresse_bien.label_brut_avec_complement,
                'ban_id_ban_adresse': adresse_bien.ban_id_ban_adresse,
            }
    
    dpe_logement_type = "logement"
    dpe_data[dpe_logement_type] = {}
    dpe_data[dpe_logement_type]['ventilation_collection'] = {}
    dpe_data[dpe_logement_type]['climatisation_collection'] = {}
    dpe_data[dpe_logement_type]['installation_ecs_collection'] = {}
    dpe_data[dpe_logement_type]['installation_chauffage_collection'] = {}
    dpe_data[dpe_logement_type]['sortie'] = {}
    
    caracteristique_generale = DpeCaracteristiqueGenerale.objects.filter(dpe_id=dpe.id).first()
    if caracteristique_generale:
        dpe_data[dpe_logement_type]['caracteristique_generale'] = {
            'annee_construction': caracteristique_generale.annee_construction,
            'appartement_non_visite': caracteristique_generale.appartement_non_visite,
            'enum_categorie_erp_id': to_int(caracteristique_generale.enum_categorie_erp_id),
            'enum_methode_application_dpe_log_id': to_int(caracteristique_generale.enum_methode_application_dpe_log_id),
            'enum_periode_construction_id': to_int(caracteristique_generale.enum_periode_construction_id),
            'enum_usage_fonctionnel_batiment_id': to_int(caracteristique_generale.enum_usage_fonctionnel_batiment_id),
            'hsp': caracteristique_generale.hsp,
            'nombre_appartement': caracteristique_generale.nombre_appartement,
            'nombre_niveau_immeuble': caracteristique_generale.nombre_niveau_immeuble,
            'nombre_niveau_logement': caracteristique_generale.nombre_niveau_logement,
            'nombre_occupant': caracteristique_generale.nombre_occupant,
            'shon': caracteristique_generale.shon,
            'surface_habitable_immeuble': caracteristique_generale.surface_habitable_immeuble,
            'surface_habitable_logement': caracteristique_generale.surface_habitable_logement,
            'surface_utile': caracteristique_generale.surface_utile,
            'surface_tertiaire_immeuble': caracteristique_generale.surface_tertiaire_immeuble,
            'enum_methode_application_dpe_ter_id': to_int(caracteristique_generale.enum_methode_application_dpe_ter_id),
            'enum_calcul_echantillonnage_id': to_int(caracteristique_generale.enum_calcul_echantillonnage_id),
            'is_dpe_2012': caracteristique_generale.is_dpe_2012,
            'enum_sous_modele_dpe_ter_id': to_int(caracteristique_generale.enum_sous_modele_dpe_ter_id),
        }

    meteo = DpeMeteo.objects.filter(dpe_id=dpe.id).first()
    if meteo:
        dpe_data[dpe_logement_type]['meteo'] = {
            'enum_zone_climatique_id': meteo.enum_zone_climatique_id,
            'altitude': meteo.altitude,
            'enum_classe_altitude_id': meteo.enum_classe_altitude_id,
            'batiment_materiaux_anciens': meteo.batiment_materiaux_anciens
        }
    
    # enveloppe
    dpe_data[dpe_logement_type]['enveloppe'] = {}
    intertie = DpeInertie.objects.filter(dpe_id=dpe.id).first()
    if intertie:
        dpe_data[dpe_logement_type]['enveloppe']['inertie'] = {
            'inertie_plancher_bas_lourd': intertie.inertie_plancher_bas_lourd,
            'inertie_plancher_haut_lourd': intertie.inertie_plancher_haut_lourd,
            'inertie_paroi_verticale_lourd': intertie.inertie_paroi_verticale_lourd,
            'enum_classe_inertie_id': intertie.enum_classe_inertie_id
        }
    
    # mur
    dpe_data[dpe_logement_type]['enveloppe']['mur_collection'] = {'mur' : []}
    elements = DpeMur.objects.filter(dpe_id=dpe.id)
    for element in elements:
        new_element = {
            'donnee_entree':
            {
                'description' : element.description,
                'reference' : element.reference,
                'reference_lnc' : element.reference_lnc,
                'tv_coef_reduction_deperdition_id' : element.tv_coef_reduction_deperdition_id,
                'surface_aiu' : element.surface_aiu,
                'surface_aue' : element.surface_aue,
                'enum_cfg_isolation_lnc_id' : to_int(element.enum_cfg_isolation_lnc_id),
                'enum_type_adjacence_id' : to_int(element.enum_type_adjacence_id),
                'enum_orientation_id' : to_int(element.enum_orientation_id),
                'surface_paroi_totale' : element.surface_paroi_totale,
                'surface_paroi_opaque' : element.surface_paroi_opaque,
                #'paroi_lourde' : element.paroi_lourde,
                'umur0_saisi' : element.umur0_saisi,
                'tv_umur0_id' : element.tv_umur0_id,
                'epaisseur_structure' : element.epaisseur_structure,
                'enum_materiaux_structure_mur_id' : to_int(element.enum_materiaux_structure_mur_id),
                'enum_methode_saisie_u0_id' : to_int(element.enum_methode_saisie_u0_id),
                'enduit_isolant_paroi_ancienne' : element.enduit_isolant_paroi_ancienne,
                'umur_saisi' : element.umur_saisi,
                'enum_type_doublage_id' : to_int(element.enum_type_doublage_id),
                'enum_type_isolation_id' : to_int(element.enum_type_isolation_id),
                'enum_periode_isolation_id' : to_int(element.enum_periode_isolation_id),
                'resistance_isolation' : element.resistance_isolation,
                'epaisseur_isolation' : element.epaisseur_isolation,
                'tv_umur_id' : element.tv_umur_id,
                'enum_methode_saisie_u_id' : to_int(element.enum_methode_saisie_u_id),
            },
            'donnee_intermediaire':
            {
                'b' : element.b,
                'umur' : element.umur,
                'umur0' : element.umur0,
            }
        }
        dpe_data[dpe_logement_type]['enveloppe']['mur_collection']['mur'].append(new_element)

    # plancher bas
    dpe_data[dpe_logement_type]['enveloppe']['plancher_bas_collection'] = {'plancher_bas' : []}
    elements = DpePlancherBas.objects.filter(dpe_id=dpe.id)
    for element in elements:
        new_element = {
            'donnee_entree':
            {
                'description' : element.description,
                'reference' : element.reference,
                'reference_lnc' : element.reference_lnc,
                'tv_coef_reduction_deperdition_id' : element.tv_coef_reduction_deperdition_id,
                'surface_aiu' : element.surface_aiu,
                'surface_aue' : element.surface_aue,
                'enum_cfg_isolation_lnc_id' : to_int(element.enum_cfg_isolation_lnc_id),
                'enum_type_adjacence_id' : to_int(element.enum_type_adjacence_id),
                'surface_paroi_opaque' : element.surface_paroi_opaque,
                #'paroi_lourde' : element.paroi_lourde,
                'upb0_saisi' : element.upb0_saisi,
                'tv_upb0_id' : element.tv_upb0_id,
                'enum_type_plancher_bas_id' : to_int(element.enum_type_plancher_bas_id),
                'enum_methode_saisie_u0_id' : to_int(element.enum_methode_saisie_u0_id),
                'upb_saisi' : element.upb_saisi,
                'enum_type_isolation_id' : to_int(element.enum_type_isolation_id),
                'enum_periode_isolation_id' : to_int(element.enum_periode_isolation_id),
                'resistance_isolation' : element.resistance_isolation,
                'epaisseur_isolation' : element.epaisseur_isolation,
                'tv_upb_id' : element.tv_upb_id,
                'enum_methode_saisie_u_id' : to_int(element.enum_methode_saisie_u_id),
                'calcul_ue' : element.calcul_ue,
                'perimetre_ue' : element.perimetre_ue,
                'surface_ue' : element.surface_ue,
                'ue' : element.ue,
            },
            'donnee_intermediaire':
            {
                'b' : element.b,
                'upb' : element.upb,
                'upb_final' : element.upb_final,
                'upb0' : element.upb0,
            }
        }
        dpe_data[dpe_logement_type]['enveloppe']['plancher_bas_collection']['plancher_bas'].append(new_element)
    
    # plancher haut
    dpe_data[dpe_logement_type]['enveloppe']['plancher_haut_collection'] = {'plancher_haut' : []}
    elements = DpePlancherHaut.objects.filter(dpe_id=dpe.id)
    for element in elements:
        plafond = {
            'donnee_entree':
            {
                'description' : element.description,
                'reference' : element.reference,
                'reference_lnc' : element.reference_lnc,
                'tv_coef_reduction_deperdition_id' : element.tv_coef_reduction_deperdition_id,
                'surface_aiu' : element.surface_aiu,
                'surface_aue' : element.surface_aue,
                'enum_cfg_isolation_lnc_id' : to_int(element.enum_cfg_isolation_lnc_id),
                'enum_type_adjacence_id' : to_int(element.enum_type_adjacence_id),
                'surface_paroi_opaque' : element.surface_paroi_opaque,
                #'paroi_lourde' : element.paroi_lourde,
                'uph0_saisi' : element.uph0_saisi,
                'tv_uph0_id' : element.tv_uph0_id,
                'enum_type_plancher_haut_id' : to_int(element.enum_type_plancher_haut_id),
                'enum_methode_saisie_u0_id' : to_int(element.enum_methode_saisie_u0_id),
                'uph_saisi' : element.uph_saisi,
                'enum_type_isolation_id' : to_int(element.enum_type_isolation_id),
                'enum_periode_isolation_id' : to_int(element.enum_periode_isolation_id),
                'resistance_isolation' : element.resistance_isolation,
                'epaisseur_isolation' : element.epaisseur_isolation,
                'tv_uph_id' : element.tv_uph_id,
                'enum_methode_saisie_u_id' : to_int(element.enum_methode_saisie_u_id),
            },
            'donnee_intermediaire':
            {
                'b' : element.b,
                'uph' : element.uph,
                'uph0' : element.uph0,
            }
        }
        dpe_data[dpe_logement_type]['enveloppe']['plancher_haut_collection']['plancher_haut'].append(plafond)
        
    # baie vitree
    dpe_data[dpe_logement_type]['enveloppe']['baie_vitree_collection'] = {'baie_vitree' : []}
    elements = DpeBaieVitree.objects.filter(dpe_id=dpe.id)
    for element in elements:
        new_element = {
            'donnee_entree':
            {
                'description' : element.description,
                'double_fenetre' : element.double_fenetre,
                'enum_cfg_isolation_lnc_id' : to_int(element.enum_cfg_isolation_lnc_id),
                'enum_inclinaison_vitrage_id' : to_int(element.enum_inclinaison_vitrage_id),
                'enum_methode_saisie_perf_vitrage_id' : to_int(element.enum_methode_saisie_perf_vitrage_id),
                'enum_orientation_id' : to_int(element.enum_orientation_id),
                'enum_type_adjacence_id' : to_int(element.enum_type_adjacence_id),
                'enum_type_baie_id' : to_int(element.enum_type_baie_id),
                'enum_type_fermeture_id' : to_int(element.enum_type_fermeture_id),
                'enum_type_gaz_lame_id' : to_int(element.enum_type_gaz_lame_id),
                'enum_type_materiaux_menuiserie_id' : to_int(element.enum_type_materiaux_menuiserie_id),
                'enum_type_vitrage_id' : to_int(element.enum_type_vitrage_id),
                'epaisseur_lame' : element.epaisseur_lame ,
                'largeur_dormant' : element.largeur_dormant ,
                'nb_baie' : element.nb_baie ,
                'presence_retour_isolation' : to_int(element.presence_retour_isolation),
                'surface_aiu' : element.surface_aiu ,
                'surface_aue' : element.surface_aue ,
                'surface_totale_baie' : element.surface_totale_baie ,
                'sw_1' : element.sw_1 ,
                'sw_2' : element.sw_2 ,
                'sw_saisi' : element.sw_saisi ,
                'tv_coef_masque_lointain_homogene_id' : element.tv_coef_masque_lointain_homogene_id,
                'tv_coef_masque_proche_id' : element.tv_coef_masque_proche_id,
                'tv_coef_orientation_id' : element.tv_coef_orientation_id,
                'tv_coef_reduction_deperdition_id' : element.tv_coef_reduction_deperdition_id,
                'tv_deltar_id' : element.tv_deltar_id,
                'tv_sw_id' : element.tv_sw_id,
                'tv_ug_id' : element.tv_ug_id,
                'tv_ujn_id' : element.tv_ujn_id,
                'tv_uw_id' : element.tv_uw_id,
                'ug_saisi' : element.ug_saisi ,
                'ujn_saisi' : element.ujn_saisi ,
                'uw_1' : element.uw_1 ,
                'uw_2' : element.uw_2 ,
                'uw_saisi' : element.uw_saisi ,
                'vitrage_vir' : to_int(element.vitrage_vir),
                'enum_type_pose_id' : to_int(element.enum_type_pose_id),
                'reference' : element.reference ,
                'reference_paroi' : element.reference_paroi ,
                'reference_lnc' : element.reference_lnc ,
                'presence_protection_solaire_hors_fermeture' : element.presence_protection_solaire_hors_fermeture ,
                'presence_joint' : to_int(element.presence_joint),
            },
            'donnee_intermediaire':
            {
                'b' : element.b,
                'ug' : element.ug ,
                'uw' : element.uw ,
                'ujn' : element.ujn ,
                'u_menuiserie' : element.u_menuiserie ,
                'sw' : element.sw ,
                'fe1' : element.fe1 ,
                'fe2' : element.fe2 ,
            }
        }

        
        masques = DpeBaieVitreeMasque.objects.filter(baie_vitree_id=element)
        masque_list = []
        for masque in masques:
            ml = masque.masque_id
            tv_coef_id = ml.tv_coef_masque_lointain_non_homogene_id
            if tv_coef_id:
                masque_list.append({
                    "tv_coef_masque_lointain_non_homogene_id": tv_coef_id
                })
        if masque_list:
            new_element["masque_lointain_non_homogene_collection"] = {
                "masque_lointain_non_homogene": masque_list
            }

    
        doublebaies = DpeBaieVitreeDoubleFenetre.objects.filter(baie_vitree_id=element)
        for baie in doublebaies:
            new_element['baie_vitree_double_fenetre'] = {
                'donnee_entree':
                {
                    'baie_vitree_id' : baie.baie_vitree,
                    'tv_ug_id' : baie.tv_ug_id,
                    'enum_type_vitrage_id' : baie.v,
                    'enum_inclinaison_vitrage_id' : baie.enum_inclinaison_vitrage_id,
                    'enum_type_gaz_lame_id' : baie.enum_type_gaz_lame_id ,
                    'epaisseur_lame' : baie.epaisseur_lame ,
                    'vitrage_vir' : baie.vitrage_vir ,
                    'enum_methode_saisie_perf_vitrage_id' : baie.enum_methode_saisie_perf_vitrage_id ,
                    'ug_saisi' : baie.ug_saisi ,
                    'tv_uw_id' : baie.tv_uw_id ,
                    'enum_type_materiaux_menuiserie_id' : baie.enum_type_materiaux_menuiserie_id ,
                    'enum_type_baie_id' : baie.enum_type_baie_id ,
                    'uw_saisi' : baie.uw_saisi ,
                    'tv_sw_id' : baie.tv_sw_id ,
                    'sw_saisi' : baie.sw_saisi ,
                    'enum_type_pose_id' : baie.enum_type_pose_id ,
                },
                'donnee_intermediaire':
                {
                    'ug' : baie.ug ,
                    'uw' : baie.uw ,
                    'sw' : baie.sw ,
                }
            }
            
        dpe_data[dpe_logement_type]['enveloppe']['baie_vitree_collection']['baie_vitree'].append(new_element)
        
    # portes
    dpe_data[dpe_logement_type]['enveloppe']['porte_collection'] = {'porte' : []}
    elements = DpePorte.objects.filter(dpe_id=dpe.id)
    for element in elements:
        porte = {
            'donnee_entree':
            {
                'description' : element.description,
                'reference' : element.reference,
                'reference_paroi' : element.reference_paroi,
                'reference_lnc' : element.reference_lnc,
                'enum_cfg_isolation_lnc_id' : to_int(element.enum_cfg_isolation_lnc_id),
                'enum_type_adjacence_id' : to_int(element.enum_type_adjacence_id),
                'tv_coef_reduction_deperdition_id' : element.tv_coef_reduction_deperdition_id,
                'surface_aiu' : element.surface_aiu,
                'surface_aue' : element.surface_aue,
                'surface_porte' : element.surface_porte,
                'tv_uporte_id' : element.tv_uporte_id,
                'enum_methode_saisie_uporte_id' : to_int(element.enum_methode_saisie_uporte_id),
                'enum_type_porte_id' : to_int(element.enum_type_porte_id),
                
                'uporte_saisi' : element.uporte_saisi,
                'nb_porte' : element.nb_porte,
                'largeur_dormant' : element.largeur_dormant,
                'presence_retour_isolation' : to_int(element.presence_retour_isolation),
                'presence_joint' : to_int(element.presence_joint),
                'enum_type_pose_id' : to_int(element.enum_type_pose_id),
            },
            'donnee_intermediaire':
            {
                'uporte' : element.uporte,
                'b' : element.b,
            }
        }
        dpe_data[dpe_logement_type]['enveloppe']['porte_collection']['porte'].append(porte)
    
    # ets
    ets_collection = DpeEts.objects.filter(dpe_id=dpe.id)
    dpe_data[dpe_logement_type]['enveloppe']['ets_collection'] = {'ets' : []}
    for ets in ets_collection:
        extension = {
            'donnee_entree':
            {
                'description' : element.description,
                'reference' : element.reference,
                'tv_coef_reduction_deperdition_id' : element.tv_coef_reduction_deperdition_id,
                'enum_cfg_isolation_lnc_id' : to_int(element.enum_cfg_isolation_lnc_id),
                'tv_coef_transparence_ets_id' : element.tv_coef_transparence_ets_id,
            },
            'donnee_intermediaire':
            {
                'coef_transparence_ets' : element.coef_transparence_ets,
                'bver' : element.bver,
            }, 
            'baie_ets_collection': {'baie_ets' : []}
            
        }
        baie_ets_collection = DpeBaieEts.objects.filter(baie_id=ets.id)
        for baie_ets in baie_ets_collection:
            extension['baie_ets_collection']['baie_ets'].append(
                {
                    'donnee_entree':
                    {
                        'description' : baie_ets.description,
                        'reference' : baie_ets.reference,
                        'enum_orientation_id' : to_int(baie_ets.enum_orientation_id),
                        'enum_inclinaison_vitrage_id' : to_int(baie_ets.enum_inclinaison_vitrage_id),
                        'surface_totale_baie' : baie_ets.surface_totale_baie,
                        'nb_baie' : baie_ets.nb_baie,
                    }
                }
            )
        dpe_data[dpe_logement_type]['enveloppe']['ets_collection']['ets'].append(extension)
        
    # pont_thermique
    dpe_data[dpe_logement_type]['enveloppe']['pont_thermique_collection'] = {'pont_thermique' : []}
    elements = DpePontThermique.objects.filter(dpe_id=dpe.id)
    for element in elements:
        pont = {
            'donnee_entree':
            {
                'description' : element.description,
                'reference' : element.reference,
                'reference_1' : element.reference_1,
                'reference_2' : element.reference_2,
                'tv_pont_thermique_id' : element.tv_pont_thermique_id,
                'pourcentage_valeur_pont_thermique' : element.pourcentage_valeur_pont_thermique,
                'l' : element.l,
                'enum_methode_saisie_pont_thermique_id' : to_int(element.enum_methode_saisie_pont_thermique_id),
                'enum_type_liaison_id' : to_int(element.enum_type_liaison_id),
                'k_saisi' : element.k_saisi,
            },
            'donnee_intermediaire':
            {
                'k' : element.k,
            }
        }
        dpe_data[dpe_logement_type]['enveloppe']['pont_thermique_collection']['pont_thermique'].append(pont)
        
    # ventilation
    dpe_data[dpe_logement_type]['ventilation_collection'] = {'ventilation' : []}
    elements = DpeVentilation.objects.filter(dpe_id=dpe.id)
    for element in elements:
        pont = {
            'donnee_entree':
            {
                'surface_ventile' : element.surface_ventile,
                'description' : element.description,
                'reference' : element.reference,
                'plusieurs_facade_exposee' : element.plusieurs_facade_exposee,
                'tv_q4pa_conv_id' : element.tv_q4pa_conv_id,
                'q4pa_conv_saisi' : element.q4pa_conv_saisi,
                'enum_methode_saisie_q4pa_conv_id' : to_int(element.enum_methode_saisie_q4pa_conv_id),
                'tv_debits_ventilation_id' : element.tv_debits_ventilation_id,
                'enum_type_ventilation_id' : to_int(element.enum_type_ventilation_id),
                'ventilation_post_2012' : element.ventilation_post_2012,
                'ref_produit_ventilation' : element.ref_produit_ventilation,
                'cle_repartition_ventilation' : element.cle_repartition_ventilation,
            },
            'donnee_intermediaire':
            {
                'pvent_moy' : element.pvent_moy,
                'q4pa_conv' : element.q4pa_conv,
                'conso_auxiliaire_ventilation' : element.conso_auxiliaire_ventilation,
                'hperm' : element.hperm,
                'hvent' : element.hvent,
            }
        }
        dpe_data[dpe_logement_type]['ventilation_collection']['ventilation'].append(pont)
    
    # climatisation
    dpe_data[dpe_logement_type]['climatisation_collection'] = {'climatisation' : []}
    elements = DpeClimatisation.objects.filter(dpe_id=dpe.id)
    for element in elements:
        pont = {
            'donnee_entree':
            {
                'surface_clim' : element.surface_clim,
                'description' : element.description,
                'reference' : element.reference,
                'tv_seer_id' : element.tv_seer_id,
                'nombre_logement_echantillon' : element.nombre_logement_echantillon,
                'enum_methode_calcul_conso_id' : to_int(element.enum_methode_calcul_conso_id),
                'enum_periode_installation_fr_id' : to_int(element.enum_periode_installation_fr_id),
                'cle_repartition_clim' : element.cle_repartition_clim,
                'enum_type_generateur_fr_id' : to_int(element.enum_type_generateur_fr_id),
                'enum_type_energie_id' : to_int(element.enum_type_energie_id),
                'enum_methode_saisie_carac_sys_id' : to_int(element.enum_methode_saisie_carac_sys_id),
                'ref_produit_fr' : element.ref_produit_fr,
            },
            'donnee_intermediaire':
            {
                'eer' : element.eer,
                'besoin_fr' : element.besoin_fr,
                'conso_fr' : element.conso_fr,
                'conso_fr_depensier' : element.conso_fr_depensier,
            }
        }
        dpe_data[dpe_logement_type]['climatisation_collection']['climatisation'].append(pont)
        
    # production_elec_enr
    dpe_data[dpe_logement_type]['production_elec_enr'] = ""
    elements = DpeProductionElecEnr.objects.filter(dpe_id=dpe.id)
    for element in elements:
        panneaux = DpePanneauxPv.objects.filter(production_elec_enr_id=element)
        panneau_list = []
        for panneau in panneaux:
            panneau_list.append(
                {
                    'surface_totale_capteurs' : panneau.surface_totale_capteurs,
                    'ratio_virtualisation' : panneau.ratio_virtualisation,
                    'nombre_module' : panneau.nombre_module,
                    'tv_coef_orientation_pv_id' : panneau.tv_coef_orientation_pv_id,
                    'enum_orientation_pv_id' : to_int(panneau.enum_orientation_pv_id),
                    'enum_inclinaison_pv_id' : to_int(panneau.enum_inclinaison_pv_id),
                }
            )
        dpe_data[dpe_logement_type]['production_elec_enr'] = {
            'donnee_entree':
            {
                'description' : element.description,
                'reference' : element.reference,
                'presence_production_pv' : element.presence_production_pv,
                'enum_type_enr_id' : to_int(element.enum_type_enr_id),
            },
            'donnee_intermediaire':
            {
                'taux_autoproduction' : element.taux_autoproduction,
                'production_pv' : element.production_pv,
                'conso_elec_ac' : element.conso_elec_ac,
            },
            'panneaux_pv_collection':
            {
                'panneaux_pv' : panneau_list
            },
        }

    # production_elec_enr
    dpe_data[dpe_logement_type]['installation_ecs_collection']['installation_ecs'] = []
    elements = DpeInstallationEcs.objects.filter(dpe_id=dpe.id)
    print(elements)
    for element in elements:
        installation_ecs = {
            'donnee_entree':
            {
                'description' : element.description,
                'reference' : element.reference,
                #'reference_generateur_mixte' : element.reference_generateur_mixte,
                'enum_cfg_installation_ecs_id' : to_int(element.enum_cfg_installation_ecs_id),
                'enum_type_installation_id' : to_int(element.enum_type_installation_id),
                'enum_methode_calcul_conso_id' : to_int(element.enum_methode_calcul_conso_id),
                'ratio_virtualisation' : element.ratio_virtualisation,
                'cle_repartition_ecs' : element.cle_repartition_ecs,
                'surface_habitable' : element.surface_habitable,
                'nombre_logement' : element.nombre_logement,
                'rdim' : element.rdim,
                'fecs_saisi' : element.fecs_saisi,
                'tv_facteur_couverture_solaire_id' : element.tv_facteur_couverture_solaire_id,
                'enum_methode_saisie_fact_couv_sol_id' : to_int(element.enum_methode_saisie_fact_couv_sol_id),
                'enum_type_installation_solaire_id' : to_int(element.enum_type_installation_solaire_id),
                'tv_rendement_distribution_ecs_id' : element.tv_rendement_distribution_ecs_id,
                'enum_bouclage_reseau_ecs_id' : to_int(element.enum_bouclage_reseau_ecs_id),
                'reseau_distribution_isole' : element.reseau_distribution_isole,
            },
            'donnee_intermediaire':
            {
                'rendement_distribution' : element.rendement_distribution,
                'besoin_ecs' : element.besoin_ecs,
                'besoin_ecs_depensier' : element.besoin_ecs_depensier,
                'fecs' : element.fecs,
                'production_ecs_solaire' : element.production_ecs_solaire,
                'conso_ecs' : element.conso_ecs,
                'conso_ecs_depensier' : element.conso_ecs_depensier,
            },
            'generateur_ecs_collection': { 'generateur_ecs' : []}
        }
        generateur_ecs_collection = DpeGenerateurEcs.objects.filter(installation_ecs_id=element)
        for generateur_ecs in generateur_ecs_collection:
            installation_ecs['generateur_ecs_collection']['generateur_ecs'].append(
                {
                    'donnee_entree':
                    {
                        'description' : generateur_ecs.description,
                        'reference' : generateur_ecs.reference,
                        'reference_generateur_mixte' : generateur_ecs.reference_generateur_mixte,
                        'enum_type_generateur_ecs_id' : to_int(generateur_ecs.enum_type_generateur_ecs_id),
                        'ref_produit_generateur_ecs' : generateur_ecs.ref_produit_generateur_ecs,
                        'enum_usage_generateur_id' : to_int(generateur_ecs.enum_usage_generateur_id),
                        'enum_type_energie_id' : to_int(generateur_ecs.enum_type_energie_id),
                        'tv_generateur_combustion_id' : generateur_ecs.tv_generateur_combustion_id,
                        'enum_methode_saisie_carac_sys_id' : to_int(generateur_ecs.enum_methode_saisie_carac_sys_id),
                        'tv_pertes_stockage_id' : generateur_ecs.tv_pertes_stockage_id,
                        'tv_scop_id' : generateur_ecs.tv_scop_id,
                        'enum_periode_installation_ecs_thermo_id' : to_int(generateur_ecs.enum_periode_installation_ecs_thermo_id),
                        'identifiant_reseau_chaleur' : generateur_ecs.identifiant_reseau_chaleur,
                        'date_arrete_reseau_chaleur' : generateur_ecs.date_arrete_reseau_chaleur,
                        'tv_reseau_chaleur_id' : generateur_ecs.tv_reseau_chaleur_id,
                        'enum_type_stockage_ecs_id' : to_int(generateur_ecs.enum_type_stockage_ecs_id),
                        'position_volume_chauffe' : generateur_ecs.position_volume_chauffe,                        
                        'position_volume_chauffe_stockage' : generateur_ecs.position_volume_chauffe_stockage,                        
                        'volume_stockage' : generateur_ecs.volume_stockage,                        
                        'presence_ventouse' : generateur_ecs.presence_ventouse,                        
                     },
                    'donnee_intermediaire':
                    {
                        'pn' : generateur_ecs.pn,
                        'qp0' : generateur_ecs.qp0,
                        'rpn' : generateur_ecs.rpn,
                        'cop' : generateur_ecs.cop,
                        'ratio_besoin_ecs' : generateur_ecs.ratio_besoin_ecs,
                        'rendement_generation' : generateur_ecs.rendement_generation,
                        'rendement_generation_stockage' : generateur_ecs.rendement_generation_stockage,
                        'conso_ecs' : generateur_ecs.conso_ecs,
                        'conso_ecs_depensier' : generateur_ecs.conso_ecs_depensier,
                        'rendement_stockage' : generateur_ecs.rendement_stockage,
                    }
                }
            )
        dpe_data[dpe_logement_type]['installation_ecs_collection']['installation_ecs'].append(installation_ecs)
    
    
    # production_elec_enr
    dpe_data[dpe_logement_type]['installation_chauffage_collection']['installation_chauffage'] = []
    elements = DpeInstallationChauffage.objects.filter(dpe_id=dpe.id)
    print(elements)
    for element in elements:
        installation_chauffage = {
            'donnee_entree':
            {
                'description' : element.description,
                'reference' : element.reference,
                'surface_chauffee' : element.surface_chauffee,
                'nombre_logement_echantillon' : element.nombre_logement_echantillon,
                'rdim' : element.rdim,
                'nombre_niveau_installation_ch' : element.nombre_niveau_installation_ch,
                'enum_cfg_installation_ch_id' : to_int(element.enum_cfg_installation_ch_id),
                'ratio_virtualisation' : element.ratio_virtualisation,
                'coef_ifc' : element.coef_ifc,
                'cle_repartition_ch' : element.cle_repartition_ch,
                'enum_type_installation_id' : to_int(element.enum_type_installation_id),
                'enum_methode_calcul_conso_id' : to_int(element.enum_methode_calcul_conso_id),
                'enum_methode_saisie_fact_couv_sol_id' : to_int(element.enum_methode_saisie_fact_couv_sol_id),
                'tv_facteur_couverture_solaire_id' : element.tv_facteur_couverture_solaire_id,
                'fch_saisi' : element.fch_saisi,
            },
            'donnee_intermediaire':
            {
                'besoin_ch' : element.besoin_ch,
                'besoin_ch_depensier' : element.besoin_ch_depensier,
                'production_ch_solaire' : element.production_ch_solaire,
                'fch' : element.fch,
                'conso_ch' : element.conso_ch,
                'conso_ch_depensier' : element.conso_ch_depensier,
            },
            'emetteur_chauffage_collection': { 'emetteur_chauffage' : []},
            'generateur_chauffage_collection': { 'generateur_chauffage' : []}
        }
        
        emetteur_chauffage_collection = DpeEmetteurChauffage.objects.filter(installation_chauffage_id=element)
        for emetteur_chauffage in emetteur_chauffage_collection:
            installation_chauffage['emetteur_chauffage_collection']['emetteur_chauffage'].append({
                 'donnee_entree':
                {
                    'description' : emetteur_chauffage.description,
                    'reference' : emetteur_chauffage.reference,
                    'surface_chauffee' : emetteur_chauffage.surface_chauffee,
                    'tv_rendement_emission_id' : emetteur_chauffage.tv_rendement_emission_id,
                    'tv_rendement_distribution_ch_id' : emetteur_chauffage.tv_rendement_distribution_ch_id,
                    'tv_rendement_regulation_id' : emetteur_chauffage.tv_rendement_regulation_id,
                    'enum_type_emission_distribution_id' : to_int(emetteur_chauffage.enum_type_emission_distribution_id),
                    'tv_intermittence_id' : emetteur_chauffage.tv_intermittence_id,
                    'reseau_distribution_isole' : emetteur_chauffage.reseau_distribution_isole,
                    'enum_equipement_intermittence_id' : to_int(emetteur_chauffage.enum_equipement_intermittence_id),
                    'enum_type_regulation_id' : to_int(emetteur_chauffage.enum_type_regulation_id),
                    'enum_periode_installation_emetteur_id' : to_int(emetteur_chauffage.enum_periode_installation_emetteur_id),
                    'enum_type_chauffage_id' : to_int(emetteur_chauffage.enum_type_chauffage_id),
                    'enum_temp_distribution_ch_id' : to_int(emetteur_chauffage.enum_temp_distribution_ch_id),
                    'enum_lien_generateur_emetteur_id' : to_int(emetteur_chauffage.enum_lien_generateur_emetteur_id),
                },
                'donnee_intermediaire':
                {
                    'i0' : emetteur_chauffage.i0,
                    'rendement_emission' : emetteur_chauffage.rendement_emission,
                    'rendement_distribution' : emetteur_chauffage.rendement_distribution,
                    'rendement_regulation' : emetteur_chauffage.rendement_regulation,
                },
            })
            
        generateur_chauffage_collection = DpeGenerateurChauffage.objects.filter(installation_chauffage_id=element)
        for generateur_chauffage in generateur_chauffage_collection:
            installation_chauffage['generateur_chauffage_collection']['generateur_chauffage'].append({
                 'donnee_entree':
                {
                    'description' : generateur_chauffage.description,
                    'reference' : generateur_chauffage.reference,
                    'reference_generateur_mixte' : generateur_chauffage.reference_generateur_mixte,
                    'ref_produit_generateur_ch' : generateur_chauffage.ref_produit_generateur_ch,
                    'enum_type_generateur_ch_id' : to_int(generateur_chauffage.enum_type_generateur_ch_id),
                    'enum_usage_generateur_id' : to_int(generateur_chauffage.enum_usage_generateur_id),
                    'enum_type_energie_id' : to_int(generateur_chauffage.enum_type_energie_id),
                    'position_volume_chauffe' : generateur_chauffage.position_volume_chauffe,
                    'tv_rendement_generation_id' : generateur_chauffage.tv_rendement_generation_id,
                    'tv_scop_id' : generateur_chauffage.tv_scop_id,
                    'tv_temp_fonc_100_id' : generateur_chauffage.tv_temp_fonc_100_id,
                    'tv_temp_fonc_30_id' : generateur_chauffage.tv_temp_fonc_30_id,
                    'tv_generateur_combustion_id' : generateur_chauffage.tv_generateur_combustion_id,
                    'tv_reseau_chaleur_id' : generateur_chauffage.tv_reseau_chaleur_id,
                    'identifiant_reseau_chaleur' : generateur_chauffage.identifiant_reseau_chaleur,
                    'date_arrete_reseau_chaleur' : generateur_chauffage.date_arrete_reseau_chaleur,
                    'n_radiateurs_gaz' : generateur_chauffage.n_radiateurs_gaz,
                    'priorite_generateur_cascade' : generateur_chauffage.priorite_generateur_cascade,
                    'presence_ventouse' : generateur_chauffage.presence_ventouse,
                    'presence_regulation_combustion' : generateur_chauffage.presence_regulation_combustion,
                    'enum_methode_saisie_carac_sys_id' : to_int(generateur_chauffage.enum_methode_saisie_carac_sys_id),
                    'enum_lien_generateur_emetteur_id' : to_int(generateur_chauffage.enum_lien_generateur_emetteur_id),
                },
                'donnee_intermediaire':
                {
                    'scop' : generateur_chauffage.scop,
                    'pn' : generateur_chauffage.pn,
                    'qp0' : generateur_chauffage.qp0,
                    'pveilleuse' : generateur_chauffage.pveilleuse,
                    'temp_fonc_30' : generateur_chauffage.temp_fonc_30,
                    'temp_fonc_100' : generateur_chauffage.temp_fonc_100,
                    'rpn' : generateur_chauffage.rpn,
                    'rpint' : generateur_chauffage.rpint,
                    'rendement_generation' : generateur_chauffage.rendement_generation,
                    'conso_ch' : generateur_chauffage.conso_ch,
                    'conso_ch_depensier' : generateur_chauffage.conso_ch_depensier,
                },
            })
        dpe_data[dpe_logement_type]['installation_chauffage_collection']['installation_chauffage'].append(installation_chauffage)
    
    # Sortie
    dpe_data[dpe_logement_type]['sortie'] = {}
    dpe_data[dpe_logement_type]['sortie']['deperdition'] = model_instance_to_json(DpeDeperdition.objects.filter(dpe_id=dpe.id).first())
    dpe_data[dpe_logement_type]['sortie']['apport_et_besoin'] = model_instance_to_json(DpeApportEtBesoin.objects.filter(dpe_id=dpe.id).first())
    dpe_data[dpe_logement_type]['sortie']['ef_conso'] = model_instance_to_json(DpeEfConso.objects.filter(dpe_id=dpe.id).first())
    dpe_data[dpe_logement_type]['sortie']['ep_conso'] = model_instance_to_json(DpeEpConso.objects.filter(dpe_id=dpe.id).first())
    dpe_data[dpe_logement_type]['sortie']['emission_ges'] = model_instance_to_json(DpeEmissionGes.objects.filter(dpe_id=dpe.id).first())
    dpe_data[dpe_logement_type]['sortie']['production_electricite'] = model_instance_to_json(DpeProductionElectricite.objects.filter(dpe_id=dpe.id).first())
    #dpe_data[dpe_logement_type]['sortie']['sortie_par_energie_collection'] = model_instance_to_json(DpeSortieParEnergie.objects.filter(dpe_id=dpe.id))
    dpe_data[dpe_logement_type]['sortie']['confort_ete'] = model_instance_to_json(DpeConfortEte.objects.filter(dpe_id=dpe.id).first())
    dpe_data[dpe_logement_type]['sortie']['qualite_isolation'] = model_instance_to_json(DpeQualiteIsolation.objects.filter(dpe_id=dpe.id).first())

    dpe_data['descriptif_travaux'] =  {
            'pack_travaux_collection' : {'pack_travaux':[]}
        }
    dpe_data['fiche_technique_collection'] =  {
        'fiche_technique' : []}
    
    

    return to_dpe_json(dpe_data)