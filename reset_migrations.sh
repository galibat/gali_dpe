#!/bin/bash

# Supprimer les fichiers .py dans les dossiers migrations (sauf __init__.py), en excluant .venv
find . -path "*/migrations/*.py" -not -name "__init__.py" -not -path "./.venv/*" -delete

# Supprimer les .pyc dans les migrations, en excluant .venv
find . -path "*/migrations/*.pyc" -not -path "./.venv/*" -delete

python manage.py makemigrations
python manage.py migrate