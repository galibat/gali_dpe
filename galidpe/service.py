from django.db import connections, ProgrammingError, OperationalError, DatabaseError
from django.db import connection
from django.conf import settings


# DB Utils
def execute_sql(req, ignore_errors=False):
    """
    Exécute une requête SQL sur la base de données galidpe.
    :param req: Requête SQL à exécuter
    :param ignore_errors: Si True, les erreurs ne seront pas affichées
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(req)
    except (ProgrammingError, OperationalError, DatabaseError) as e:
        if not ignore_errors : 
            print(f"[ERROR] Erreur lors de l'exécution de la requête : {e}")
        return False
    return True

def setup_dblink_to_dpe():
    """
    Configure une connexion dblink vers la base de données DPE.
    """
    dpe_db = settings.DATABASES['dpe']

    dbname = dpe_db['NAME']
    user = dpe_db['USER']
    password = dpe_db.get('PASSWORD', '')
    host = dpe_db.get('HOST', 'localhost')
    port = dpe_db.get('PORT', '5432')

    # Construction de la chaîne de connexion PostgreSQL pour dblink
    conn_string = f"host={host} port={port} dbname={dbname} user={user}"
    if password:
        conn_string += f" password={password}"

    # Créer l'extension dblink si nécessaire
    execute_sql("CREATE EXTENSION IF NOT EXISTS dblink;", ignore_errors=True)

    # Déconnecter toute connexion existante avec ce nom
    execute_sql("SELECT dblink_disconnect('conn_dpe');", ignore_errors=True)

    # Créer une nouvelle connexion dblink
    execute_sql(f"SELECT dblink_connect('conn_dpe', '{conn_string}');")

    print("[OK] Connexion dblink 'conn_dpe' prête.")    

def import_dpe_infos():
    """
    Importe les informations de la base de données DPE dans la base de données galidpe.
    """
    setup_dblink_to_dpe()

    # Créer la table galidpe_info si elle n'existe pas
    execute_sql ("""
        INSERT INTO galidpe_info (
            dpe_id,
            ademe,
            surface_habitable_logement,
            conso_val,
            conso_lettre,
            ges_val,
            ges_lettre,
            classe,
            adresse,
            cp,
            ville
        )
        SELECT 
            dpe_id,
            identifiant_dpe,
            surface_habitable_logement,
            conso_val,
            CASE 
                WHEN conso_val IS NULL OR conso_val = 0 THEN 'N'
                WHEN conso_val <= 70 THEN 'A'
                WHEN conso_val <= 110 THEN 'B'
                WHEN conso_val <= 180 THEN 'C'
                WHEN conso_val <= 250 THEN 'D'
                WHEN conso_val <= 330 THEN 'E'
                WHEN conso_val <= 420 THEN 'F'
                ELSE 'G'
            END AS conso_lettre,
            ges_val,
            ges_lettre,
            classe,
            adresse,
            cp,
            ville
        FROM dblink('conn_dpe', $$
            SELECT d.id::uuid AS dpe_id,
                   d.identifiant_dpe,
                   ca.surface_habitable_logement,
                   conso.ep_conso_5_usages_m2 AS conso_val,
                   ges.emission_ges_5_usages_m2 AS ges_val,
                   ges.classe_emission_ges AS ges_lettre,
                   conso.classe_bilan_dpe AS classe,
                   addr.adresse_brut AS adresse,
                   addr.code_postal_brut AS cp,
                   addr.nom_commune_brut AS ville
            FROM dpe d
            JOIN dpe_administratif adm ON d.id = adm.dpe_id
            JOIN dpe_caracteristique_generale ca ON d.id = ca.dpe_id
            JOIN dpe_ep_conso conso ON d.id = conso.dpe_id
            JOIN dpe_emission_ges ges ON d.id = ges.dpe_id
            JOIN dpe_geolocalisation geo ON d.id = geo.administratif_id
            JOIN dpe_t_adresse addr ON addr.id = geo.adresse_bien_id
            WHERE d.identifiant_dpe >= '21'
        $$) AS t (
            dpe_id uuid,
            identifiant_dpe varchar,
            surface_habitable_logement float,
            conso_val float,
            ges_val float,
            ges_lettre varchar,
            classe varchar,
            adresse varchar,
            cp varchar,
            ville varchar
        )
        ON CONFLICT (ademe) DO UPDATE SET
            dpe_id = EXCLUDED.dpe_id,
            surface_habitable_logement = EXCLUDED.surface_habitable_logement,
            conso_val = EXCLUDED.conso_val,
            conso_lettre = EXCLUDED.conso_lettre,
            ges_val = EXCLUDED.ges_val,
            ges_lettre = EXCLUDED.ges_lettre,
            classe = EXCLUDED.classe,
            adresse = EXCLUDED.adresse,
            cp = EXCLUDED.cp,
            ville = EXCLUDED.ville;
        """)