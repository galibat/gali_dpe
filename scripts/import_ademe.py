# scripts/import_ademe.py
# Script lancé sur la base PostgreSQL importée depuis l'Open Data ADEME pour la préparer à GaliDPE


# !!!!!!!!!!!!!!!! En cours de développement !!!!!!!!!!!!!!!!!!!

from decouple import config
import dj_database_url
import psycopg2

# Récupération de la configuration depuis .env
DATABASE_URL = config("DATABASE_URL")
db_config = dj_database_url.parse(DATABASE_URL)

# Connexion PostgreSQL
conn = psycopg2.connect(
    dbname=db_config["NAME"],
    user=db_config["USER"],
    password=db_config["PASSWORD"],
    host=db_config["HOST"] or "localhost",
    port=db_config["PORT"] or 5432
)
conn.autocommit = True
cur = conn.cursor()

print(f"Connexion à la base : {db_config['NAME']}")

# === 1. Suppression de contraintes ===
contraintes = [
    ("dpe", "dpe_identifiant_dpe_is_dpe_2012_uindex"),
    ("dpe", "dpe_remplacant_id_key"),
    ("dpe_infos", "dpe_infos_code_postal_check"),
]

for table, contrainte in contraintes:
    print(f"→ Suppression de {contrainte} sur {table} (si elle existe)...")
    cur.execute(f"""
    DO $$
    BEGIN
        IF EXISTS (
            SELECT 1 FROM pg_constraint WHERE conname = %s
        ) THEN
            EXECUTE 'ALTER TABLE {table} DROP CONSTRAINT ' || quote_ident(%s);
        END IF;
    END$$;
    """, (contrainte, contrainte))
    print(f"   ✔ {contrainte} traité.")

# === 2. Création d’index (si aucun index ne couvre déjà la même colonne dans la même table) ===

index_definitions = [
    ("dpe", "identifiant_dpe"),
    ("dpe_administratif", "dpe_id"),
    ("dpe_caracteristique_generale", "dpe_id"),
    ("dpe_ep_conso", "dpe_id"),
    ("dpe_emission_ges", "dpe_id"),
    ("dpe_geolocalisation", "administratif_id"),
    ("dpe_t_adresse", "id"),
]

for table, column in index_definitions:
    index_name = f"idx_{table}_{column}"
    print(f"→ Vérification d'un index existant sur {table}.{column}...")

    cur.execute("""
        SELECT indexname
        FROM pg_indexes
        WHERE tablename = %s
    """, (table,))

    indexes = cur.fetchall()
    index_exists = False

    for (existing_index,) in indexes:
        cur.execute(f"""
            SELECT a.attname
            FROM pg_class t
            JOIN pg_index i ON t.oid = i.indrelid
            JOIN pg_class ix ON ix.oid = i.indexrelid
            JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(i.indkey)
            WHERE t.relname = %s AND ix.relname = %s
        """, (table, existing_index))

        indexed_columns = [row[0] for row in cur.fetchall()]
        if [column] == indexed_columns:  # exact match sur 1 seule colonne
            index_exists = True
            print(f"   ✔ Index existant trouvé : {existing_index} sur {table}({column})")
            break

    if not index_exists:
        print(f"   ➕ Création de l’index {index_name} sur {table}({column})...")
        cur.execute(f'CREATE INDEX {index_name} ON {table} ({column})')
        print(f"   ✔ {index_name} créé.")


# === 3. Exemple de requête préparée ===

sql_insert_in_dpe_infos = """
SELECT d.id, d.identifiant_dpe, NULL ug,
       ca.surface_habitable_logement,
       conso.ep_conso_5_usages_m2 AS conso_val,
       NULL conso_lettre,
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
"""

print("✅ Préparation terminée. La base est prête pour GaliDPE.")

cur.close()
conn.close()
