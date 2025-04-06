# galidpe/signals.py
from django.db import connections, ProgrammingError, OperationalError, DatabaseError
from django.db.models.signals import pre_migrate, post_migrate
from django.dispatch import receiver
from django.db import connection
from django.conf import settings
from dpe.service import check_dpe_index
from .service import execute_sql

@receiver(pre_migrate)
def create_galidpe_schema(sender, **kwargs):
    with connection.cursor() as cursor:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS galidpe;")

@receiver(post_migrate)
def after_migration(sender, **kwargs):
    
    check_dpe_index()
    
    execute_sql("""
        CREATE INDEX IF NOT EXISTS idx_galidpeinfo_tsv
        ON galidpe.galidpe_info
        USING GIN (tsv);
    """)


    execute_sql("""
        CREATE OR REPLACE FUNCTION galidpe.update_galidpeinfo_tsv() RETURNS trigger AS $$
        BEGIN
        NEW.tsv := to_tsvector('french',
            coalesce(NEW.adresse, '') || ' ' ||
            coalesce(NEW.cp, '') || ' ' ||
            coalesce(NEW.ville, '') || ' ' ||
            coalesce(NEW.ug, '') || ' ' ||
            coalesce(NEW.ademe, '')
        );
        RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
    """)

    execute_sql("""
        DROP TRIGGER IF EXISTS tsv_update ON galidpe.galidpe_info;
    """)

    execute_sql("""
        CREATE TRIGGER tsv_update
        BEFORE INSERT OR UPDATE
        ON galidpe.galidpe_info
        FOR EACH ROW
        EXECUTE FUNCTION galidpe.update_galidpeinfo_tsv();
    """)

    # Crée les fonctions PostgreSQL : dpe_conso_lettre et dpe_ges_lettre
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

 