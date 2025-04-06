#!/usr/bin/env python3
# Chemin : check_models.py
"""
Ce script parcourt automatiquement tous les modèles de l'application 'dpe'
et tente d'instancier et de valider chacun d'eux via full_clean().
Les erreurs rencontrées sont affichées avec le nom du modèle.
"""

import os
import django
from django.core.exceptions import ValidationError

# Assurez-vous que DJANGO_SETTINGS_MODULE est bien défini pour votre projet
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.apps import apps

error_models = []

print("Vérification des modèles de l'application 'dpe'...\n")

# Récupère tous les modèles de l'app dpe
for model in apps.get_app_config("dpe").get_models():
    try:
        # On essaie d'instancier le modèle sans paramètres.
        # Certains modèles requièrent des valeurs obligatoires et pourraient lever une erreur de validation.
        instance = model()
        instance.full_clean()  # Déclenche la validation du modèle
        print(f"{model.__name__}: OK")
    except ValidationError as ve:
        # Une ValidationError peut être attendue pour des champs obligatoires manquants
        print(f"{model.__name__}: ValidationError - {ve}")
        error_models.append((model.__name__, f"ValidationError: {ve}"))
    except Exception as e:
        print(f"{model.__name__}: ERREUR - {e}")
        error_models.append((model.__name__, str(e)))

if error_models:
    print("\nModèles posant problème :")
    for name, error in error_models:
        print(f"- {name}: {error}")
else:
    print("\nAucun modèle ne provoque d'erreur.")
