# Gali DPE

** Version 0.0.1 - Projet en cours de création. De nombreuses parties du codes sont en cours de modification.

**Gali DPE** est un module de l'application [Galibat](https://github.com/galibat) dédié à l'analyse des DPE (Diagnostics de Performance Énergétique).  
Il s'intègre dans l'écosystème open-source Galibat pour aider à la gestion et à l'optimisation énergétique des bâtiments.

---

## Origine du nom

- **Gali** : En hommage au *galibot*, jeune apprenti mineur, symbole du travail du bassin minier.
- **DPE** : Diagnostic de Performance Énergétique, au cœur de ce module.

---

## Objectifs de Gali DPE

Ce projet Django a pour but de :

- Importer, lire et analyser des fichiers DPE (XML DPE v2.5).
- Stocker les données dans une base relationnelle PostgreSQL ou SQLite
- Évaluer la qualité et la cohérence des DPE (précision, incohérences, fiabilité...).
- Fournir une interface web pour l'exploration, la recherche et la visualisation cartographique des diagnostics.

---

## Fonctionnalités

- Import de DPE au format XML.
- Import de DPE au format OpenData Ademe.
- Import / Export au format DPE Json compatible open3Cl
- Stockage DPE Json dans la base de donnée ou dans des dossiers ou pas de stockage
- Analyse des DPE selon un jeu de règles pondérées (précision, incohérence, fiabilité).
- Interface Django.
- Recherche full-text par adresse ou numéro ADEME.
- Affichage cartographique des diagnostics (Leaflet + GeoJSON). (en projet)
- API sécurisée pour exploitation externe (OpenAPI + tokens).  (en projet)

---

## Django
# app galidpe
- module principal de l'app

# app dpe
- model de données OpenData Ademe

# app home
- Page d'accueil

---

## Intégration dans Galibat

Gali DPE s’intègre dans le projet principal Galibat en tant que brique spécialisée.  
Il peut fonctionner de manière autonome ou être combiné avec les autres modules du projet pour une gestion globale du patrimoine bâti.

---

## Contribution

Gali DPE est un projet communautaire open-source.  
Vous êtes les bienvenus pour :

- Proposer des règles ou scores d'analyse supplémentaires.
- Améliorer les performances ou la qualité du code.
- Créer des visualisations ou exports utiles pour les utilisateurs.
- Documenter les fichiers XML DPE et leurs structures.
- Traduire l’interface ou les messages d’analyse.

---

## Licence

**Galibat License v1.0**

Vous êtes autorisé à utiliser, modifier et distribuer ce logiciel librement, à condition que :

- Toute modification soit communiquée au créateur original.
- Toute redistribution inclue cette même licence.
- L'usage et la modification à des fins commerciales sont strictement interdits.

> Ce logiciel est fourni "tel quel", sans garantie d'aucune sorte.

---

## Rejoignez-nous

Prêt à rejoindre l'aventure Galibat ?  
Suivez les projets sur [github.com/galibat](https://github.com/galibat) et contribuez à une meilleure rénovation énergétique collective.
