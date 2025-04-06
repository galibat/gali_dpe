#!/usr/bin/env python3
"""
Chemin : setup.py
Script d'installation pour le projet Django.

Fonctionnalités :
- Vérifie que le client PostgreSQL (psql) est installé.
- Crée un environnement virtuel s'il n'existe pas.
- Installe les dépendances Python depuis requirements.txt.
- Gère le fichier .env en le copiant depuis .env_exemple si nécessaire.
- Charge les variables d'environnement du fichier .env.
- Extrait les paramètres de connexion depuis DATABASE_GALIDPE_URL.
- Vérifie l'existence des bases 'galidpe' et 'dpe' via psql (en forçant la connexion TCP).
- Propose de créer la base 'galidpe' si elle n'existe pas.
- Propose d'exécuter les commandes Django (makemigrations et migrate).
"""

import os
import sys
import subprocess
import shutil
import re

def check_command(cmd):
    return shutil.which(cmd) is not None

def run_command(command, env=None):
    print("Exécution :", " ".join(command))
    subprocess.run(command, check=True, env=env)

def get_python_executable():
    # Si on n'est pas dans un venv, on utilise l'exécutable du venv (s'il existe)
    if sys.prefix == sys.base_prefix:
        venv_python = os.path.join(os.getcwd(), ".venv", "bin", "python")
        if os.path.exists(venv_python):
            return venv_python
        else:
            return sys.executable
    else:
        return sys.executable

def create_virtualenv(venv_dir):
    if not os.path.isdir(venv_dir):
        print(f"Création de l'environnement virtuel Python ({venv_dir})...")
        run_command([sys.executable, "-m", "venv", venv_dir])
    else:
        print("Environnement virtuel Python déjà présent")

def install_dependencies(python_executable):
    print("Installation des paquets Python...")
    # On utilise --break-system-packages si besoin, mais dans le venv ce n'est normalement pas nécessaire
    run_command([python_executable, "-m", "pip", "install", "--upgrade", "pip"])
    run_command([python_executable, "-m", "pip", "install", "-r", "requirements.txt"])

def manage_env_file(env_file, env_example):
    if not os.path.exists(env_file):
        print(f"Copie de {env_example} vers {env_file}...")
        shutil.copy(env_example, env_file)
    else:
        rep = input(f"Le fichier {env_file} existe déjà. Voulez-vous le remplacer ? [o/N] ").strip().lower()
        if rep == "o":
            shutil.copy(env_example, env_file)
            print(f"Fichier {env_file} mis à jour.")
        else:
            print(f"Fichier {env_file} conservé.")

def load_env_file(env_file):
    # Parse simple de lignes au format KEY=VALUE
    env_vars = {}
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                value = value.strip().strip('"').strip("'")
                env_vars[key.strip()] = value
    os.environ.update(env_vars)

def extract_pg_params(db_url):
    # Format attendu : postgres://user:password@host:port/dbname
    pattern = r"postgres://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)"
    match = re.match(pattern, db_url)
    if not match:
        print("Erreur : URL de base de données mal formée :", db_url)
        sys.exit(1)
    return match.groups()  # (pg_user, pg_password, pg_host, pg_port, dbname)

def check_db_exists(pg_user, pg_password, pg_host, pg_port, dbname):
    try:
        result = subprocess.run(
            ["psql", "-h", pg_host, "-p", pg_port, "-U", pg_user, "-d", "postgres", "-tAc",
             f"SELECT 1 FROM pg_database WHERE datname='{dbname}'"],
            env={**os.environ, "PGPASSWORD": pg_password},
            capture_output=True, text=True, check=True
        )
        return "1" in result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Erreur lors de la vérification de la base {dbname}")
        return False

def create_db(pg_user, pg_password, pg_host, pg_port, dbname):
    print(f"Création de la base '{dbname}'...")
    run_command(
        ["psql", "-h", pg_host, "-p", pg_port, "-U", pg_user, "-d", "postgres", "-c",
         f"CREATE DATABASE {dbname};"],
        env={**os.environ, "PGPASSWORD": pg_password}
    )
    run_command(
        ["psql", "-h", pg_host, "-p", pg_port, "-U", pg_user, "-d", "postgres", "-c",
         f"CREATE SCHEMA IF NOT EXISTS galidpe;"],
        env={**os.environ, "PGPASSWORD": pg_password}
    )

    print(f"Base '{dbname}' créée avec succès.")

def run_django_migrations(python_executable):
    rep = input("Souhaitez-vous lancer 'makemigrations' et 'migrate' ? [O/n] ").strip().lower()
    if rep == "n":
        print("Migration Django ignorée.")
    else:
        print("Lancement des migrations...")
        run_command([python_executable, "manage.py", "makemigrations"])
        run_command([python_executable, "manage.py", "migrate"])

def main():
    # Se positionner dans le répertoire du script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Vérification que psql est installé
    if not check_command("psql"):
        print("Le client PostgreSQL (psql) n'est pas installé ou introuvable dans le PATH.")
        print("Installez-le avec la commande suivante (pour Debian/Ubuntu) :")
        print("  sudo apt update && sudo apt install postgresql-client")
        sys.exit(1)
    
    # Création de l'environnement virtuel
    venv_dir = ".venv"
    create_virtualenv(venv_dir)
    
    # Utilisation de l'exécutable Python du venv
    python_executable = get_python_executable()
    print("Exécutable Python utilisé :", python_executable)
    
    # Installation des dépendances Python
    install_dependencies(python_executable)
    
    # Gestion du fichier .env
    env_file = ".env"
    env_example = ".env_exemple"
    manage_env_file(env_file, env_example)
    
    # Chargement des variables d'environnement depuis .env
    load_env_file(env_file)
    
    # Extraction des paramètres de connexion
    database_galidpe_url = os.environ.get("DATABASE_GALIDPE_URL")
    if not database_galidpe_url:
        print("Les variables DATABASE_GALIDPE_URL doivent être définies dans le .env")
        sys.exit(1)
    
    pg_user, pg_password, pg_host, pg_port, galidpe_db = extract_pg_params(database_galidpe_url)
    
    print("Paramètres PostgreSQL extraits :")
    print("  Utilisateur :", pg_user)
    print("  Hôte        :", pg_host)
    print("  Port        :", pg_port)
    print("  Base dpe    :", galidpe_db)
    
    # Vérification de l'existence de la base 'galidpe'
    print("Vérification de l'existence de la base dpe...")
    if not check_db_exists(pg_user, pg_password, pg_host, pg_port, galidpe_db):
        print("La base 'dpe' n'existe pas.")
        rep = input("Souhaitez-vous la créer maintenant ? [O/n] ").strip().lower()
        if rep == "n":
            print("Création annulée. Veuillez créer la base manuellement.")
            sys.exit(1)
        else:
            create_db(pg_user, pg_password, pg_host, pg_port, galidpe_db)
    else:
        print("Base 'galidpe' détectée.")
    
    run_django_migrations(python_executable)
    print("Installation terminée avec succès.")

if __name__ == "__main__":
    main()
