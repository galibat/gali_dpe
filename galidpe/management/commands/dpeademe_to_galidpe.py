from django.core.management.base import BaseCommand
from django.db import transaction
from dpe.models import Dpe
from galidpe.models import GaliDpeInfo
from galidpe.utils.dpe import dpe_conso_lettre

class Command(BaseCommand):
    help = "Importe les DPE ADEME manquants depuis la base dpe (via ORM) dans galidpe"

    def handle(self, *args, **options):
        self.stdout.write("Chargement des ADEME déjà existants dans GaliDpeInfo...")
        ademe_existants = set(GaliDpeInfo.objects.values_list('ademe', flat=True))
        self.stdout.write(f"{len(ademe_existants)} ADEME déjà présents dans GaliDpeInfo.")

        self.stdout.write("Exécution de la requête ORM consolidée...")
        qs = (
            Dpe.objects.filter(identifiant_dpe__gte='21')
            .select_related(
                'dpeadministratif',
                'dpecaracteristiquegenerale',
                'dpeepconso',
                'dpeemissionges',
                'dpeadministratif__geolocalisation__adresse_bien_id'
            )
            .values(
                'identifiant_dpe',
                'dpecaracteristiquegenerale__surface_habitable_logement',
                'dpeepconso__ep_conso_5_usages_m2',    # alias conso_val
                'dpeepconso__classe_bilan_dpe',           # alias classe
                'dpeemissionges__emission_ges_5_usages_m2',  # alias ges_val
                'dpeemissionges__classe_emission_ges',       # alias ges_lettre
                'dpeadministratif__geolocalisation__adresse_bien_id__adresse_brut',  # alias adresse
                'dpeadministratif__geolocalisation__adresse_bien_id__code_postal_brut',  # alias cp
                'dpeadministratif__geolocalisation__adresse_bien_id__nom_commune_brut',  # alias ville
            )
        )

        inserted = 0
        batch = []
        BATCH_SIZE = 1000

        # On enveloppe l'itération dans un bloc transactionnel pour garantir la persistance du curseur
        with transaction.atomic():
            for record in qs.iterator(chunk_size=BATCH_SIZE):
                ademe = record.get('identifiant_dpe')
                if not ademe or ademe in ademe_existants:
                    continue

                instance = GaliDpeInfo(
                    ademe=ademe,
                    ug=None,
                    surface_habitable_logement=record.get('dpecaracteristiquegenerale__surface_habitable_logement'),
                    conso_val=record.get('dpeepconso__ep_conso_5_usages_m2'),
                    conso_lettre=dpe_conso_lettre(
                        record.get('dpeepconso__ep_conso_5_usages_m2'),
                        record.get('dpecaracteristiquegenerale__surface_habitable_logement')
                    ),
                    ges_val=record.get('dpeemissionges__emission_ges_5_usages_m2'),
                    ges_lettre=record.get('dpeemissionges__classe_emission_ges'),
                    classe=record.get('dpeepconso__classe_bilan_dpe'),
                    adresse=record.get('dpeadministratif__geolocalisation__adresse_bien_id__adresse_brut'),
                    cp=record.get('dpeadministratif__geolocalisation__adresse_bien_id__code_postal_brut'),
                    ville=record.get('dpeadministratif__geolocalisation__adresse_bien_id__nom_commune_brut'),
                )
                batch.append(instance)
                inserted += 1

                if len(batch) >= BATCH_SIZE:
                    GaliDpeInfo.objects.bulk_create(batch, batch_size=BATCH_SIZE)
                    self.stdout.write(f"{inserted} insérés")
                    batch.clear()

            if batch:
                GaliDpeInfo.objects.bulk_create(batch, batch_size=BATCH_SIZE)

        self.stdout.write(self.style.SUCCESS(
            f"Import terminé : {inserted} nouveaux DPE."
        ))
"""INSERT INTO galidpe.galidpe_info (
    dpe_id,
    ademe,
    date_etablissement_dpe,
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
    d.id,
    d.identifiant_dpe,
    d.date_etablissement_dpe,
    ca.surface_habitable_logement,
    conso.ep_conso_5_usages_m2 AS conso_val,
    CASE 
        WHEN conso.ep_conso_5_usages_m2 IS NULL OR conso.ep_conso_5_usages_m2 = 0 THEN 'N'
        WHEN conso.ep_conso_5_usages_m2 <= 70 THEN 'A'
        WHEN conso.ep_conso_5_usages_m2 <= 110 THEN 'B'
        WHEN conso.ep_conso_5_usages_m2 <= 180 THEN 'C'
        WHEN conso.ep_conso_5_usages_m2 <= 250 THEN 'D'
        WHEN conso.ep_conso_5_usages_m2 <= 330 THEN 'E'
        WHEN conso.ep_conso_5_usages_m2 <= 420 THEN 'F'
        ELSE 'G'
    END AS conso_lettre,
    ges.emission_ges_5_usages_m2 AS ges_val,
    ges.classe_emission_ges AS ges_lettre,
    conso.classe_bilan_dpe AS classe,
    addr.adresse_brut,
    addr.code_postal_brut,
    addr.nom_commune_brut
FROM public.dpe d
JOIN public.dpe_administratif adm ON d.id = adm.dpe_id
JOIN public.dpe_caracteristique_generale ca ON d.id = ca.dpe_id
JOIN public.dpe_ep_conso conso ON d.id = conso.dpe_id
JOIN public.dpe_emission_ges ges ON d.id = ges.dpe_id
JOIN public.dpe_geolocalisation geo ON d.id = geo.administratif_id
JOIN public.dpe_t_adresse addr ON addr.id = geo.adresse_bien_id
ON CONFLICT (ademe) DO NOTHING;"""