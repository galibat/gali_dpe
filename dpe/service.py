# dpe/services/dpe_index_service.py

from django.db import connection, ProgrammingError, OperationalError, DatabaseError
from django.apps import apps

def add_index(table_name: str, column_name: str):
    """
    Crée un index BTree sur table_name.column_name si aucun index n'existe déjà pour cette colonne.
    :param table_name: nom de la table (ex: 'dpe_caracteristique_generale')
    :param column_name: nom de la colonne (ex: 'surface_habitable_logement')
    :param using: nom de la base Django (par défaut 'dpe')
    """
    index_name = f"idx_{table_name}_{column_name}"

    try:
        with connection.cursor() as cursor:
            # Vérifie si un index existe déjà sur la colonne, peu importe son nom
            cursor.execute("""
                SELECT 1
                FROM pg_index i
                JOIN pg_class t ON t.oid = i.indrelid
                JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(i.indkey)
                WHERE t.relname = %s AND a.attname = %s
            """, [table_name, column_name])
            exists = cursor.fetchone()

            if exists:
                #print(f"[INFO] Un index existe déjà sur {table_name}.{column_name}")
                return

            print(f"[CREATE] Création de l’index {index_name} sur {table_name}.{column_name}")
            cursor.execute(f"""
                CREATE INDEX {index_name}
                ON {table_name} ({column_name});
            """)
    except Exception as e:
        print(f"[ERROR] Impossible de créer l’index {index_name} sur {table_name}.{column_name} : {e}")


def create_indexes_on_dpe_id_fields(using='dpe'):
    try:
        models = apps.get_app_config('dpe').get_models()

        with connection.cursor() as cursor:
            for model in models:
                table_name = model._meta.db_table
                for field in model._meta.fields:
                    if field.name == 'dpe_id':
                        try:
                            cursor.execute("""
                                SELECT 1
                                FROM pg_index i
                                JOIN pg_class t ON t.oid = i.indrelid
                                JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(i.indkey)
                                WHERE t.relname = %s AND a.attname = %s
                            """, [table_name, 'dpe_id'])
                            exists = cursor.fetchone()

                            if exists:
                                #print(f"[INFO] Un index existe déjà sur {table_name}.dpe_id")
                                continue

                            index_name = f"idx_{table_name}_dpe_id"
                            print(f"[CREATE] Création de l’index {index_name} sur {table_name}.dpe_id")
                            cursor.execute(f"""
                                CREATE INDEX {index_name}
                                ON {table_name} (dpe_id);
                            """)
                        except Exception as e:
                            print(f"[ERROR] Erreur sur {table_name}.dpe_id : {e}")
    except Exception as outer:
        print(f"[ERROR] Impossible de parcourir les modèles de l'app 'dpe' : {outer}")

def execute_sql(req, ignore_error = False):
    """
    Exécute une requête SQL sur la base de données DPE.
    :param req: Requête SQL à exécuter
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(req)
            #return cursor.fetchall()
    except (ProgrammingError, OperationalError, DatabaseError) as e:
        if not ignore_error: print(f"[ERROR] Erreur lors de l'exécution de la requête : {e}")
        return None
    

def check_dpe_index():
    """
    Crée les index manquants sur les tables de la base de données DPE.
    """
    add_index('dpe', 'identifiant_dpe')
    add_index('dpe', 'ancien_dpe_id')
    add_index('dpe_geolocalisation', 'adresse_bien_id')
    add_index('dpe_geolocalisation', 'administratif_id')
    add_index('dpe_emetteur_chauffage', 'installation_chauffage_id')
    add_index('dpe_generateur_chauffage', 'installation_chauffage_id')
    add_index('dpe_generateur_ecs', 'installation_ecs_id')
    add_index('dpe_pack_travaux', 'descriptif_travaux_id')
    add_index('dpe_baie_vitree_masque', 'baie_vitree_id')
    add_index('dpe_baie_vitree_masque', 'masque_id')
    add_index('dpe', 'id')
    create_indexes_on_dpe_id_fields()


    execute_sql("""ALTER TABLE dpe_baie_vitree_masque ADD COLUMN id bigserial PRIMARY KEY;""", ignore_error=True)
    
    # Crée les fonctions PostgreSQL : dpe_conso_lettre et dpe_ges_lettre
    # Création de la fonction dpe_conso_lettre
    execute_sql("""
        CREATE OR REPLACE FUNCTION dpe_conso_lettre(DPE_index numeric)
        RETURNS char AS $$
        BEGIN
            IF DPE_index IS NULL OR DPE_index = 0 THEN
                RETURN 'N';
            ELSIF DPE_index <= 70 THEN
                RETURN 'A';
            ELSIF DPE_index <= 110 THEN
                RETURN 'B';
            ELSIF DPE_index <= 180 THEN
                RETURN 'C';
            ELSIF DPE_index <= 250 THEN
                RETURN 'D';
            ELSIF DPE_index <= 330 THEN
                RETURN 'E';
            ELSIF DPE_index <= 420 THEN
                RETURN 'F';
            ELSE
                RETURN 'G';
            END IF;
        END;
        $$ LANGUAGE plpgsql IMMUTABLE;
    """)

    # Création de la fonction dpe_ges_lettre
    execute_sql("""
        CREATE OR REPLACE FUNCTION dpe_ges_lettre(DPE_index numeric)
        RETURNS char AS $$
        BEGIN
            IF DPE_index IS NULL OR DPE_index = 0 THEN
                RETURN 'N';
            ELSIF DPE_index <= 6 THEN
                RETURN 'A';
            ELSIF DPE_index <= 11 THEN
                RETURN 'B';
            ELSIF DPE_index <= 30 THEN
                RETURN 'C';
            ELSIF DPE_index <= 50 THEN
                RETURN 'D';
            ELSIF DPE_index <= 70 THEN
                RETURN 'E';
            ELSIF DPE_index <= 100 THEN
                RETURN 'F';
            ELSE
                RETURN 'G';
            END IF;
        END;
        $$ LANGUAGE plpgsql IMMUTABLE;
    """)
