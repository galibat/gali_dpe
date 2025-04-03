#!/bin/bash

# Variables
REPO_OWNER="Open3CL"
REPO_NAME="engine"
DEST_DIR="./3clEngine"

# Récupérer la dernière version (release) via l'API GitHub
LATEST_TAG=$(curl -s "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

# Vérification
if [ -z "$LATEST_TAG" ]; then
  echo "Erreur : impossible de récupérer la dernière version du dépôt ${REPO_OWNER}/${REPO_NAME}"
  exit 1
fi

echo "Dernière version détectée : $LATEST_TAG"

# Supprimer le répertoire si déjà existant
if [ -d "$DEST_DIR" ]; then
  echo "Suppression de l'ancien dossier $DEST_DIR"
  rm -rf "$DEST_DIR"
fi

# Cloner la dernière version
git clone --depth 1 --branch "$LATEST_TAG" "https://github.com/${REPO_OWNER}/${REPO_NAME}.git" "$DEST_DIR"

# Vérification post-clonage
if [ $? -ne 0 ]; then
  echo "Erreur : le clonage a échoué"
  exit 2
fi

echo "Clonage terminé dans $DEST_DIR"

# Vérifier si package.json est présent et exécuter npm install
if [ -f "$DEST_DIR/package.json" ]; then
  echo "Fichier package.json détecté, installation des dépendances..."
  cd "$DEST_DIR"
  npm install
  if [ $? -ne 0 ]; then
    echo "Erreur : l'installation npm a échoué"
    exit 3
  fi
  echo "npm install terminé avec succès"
else
  echo "Aucun fichier package.json trouvé, npm install ignoré"
fi
