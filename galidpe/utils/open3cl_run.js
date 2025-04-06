#!/bin/env node
// ce fichier est copié dans le dossier d'Open3Cl pour executer le moteur 3cl en mode pipe en utilisant stdin et stdout 

import * as fs from 'fs';
import enums from '../src/enums.js';
import { calcul_3cl } from '../src/engine.js';
import { set_bug_for_bug_compat } from '../src/utils.js';

try {
  // Lecture du flux d'entrée (stdin)
  const data = fs.readFileSync(0, 'utf-8');

  if (!data.trim()) {
    console.error('ERREUR: Données d’entrée vides');
    process.exit(1);
  }

  // Activation du mode de compatibilité
  set_bug_for_bug_compat();

  // Parsing du JSON d'entrée
  const dpe_in = JSON.parse(data);

  if (!dpe_in?.administratif?.enum_modele_dpe_id) {
    console.error('ERREUR: Champ enum_modele_dpe_id manquant');
    process.exit(1);
  }

  const modele = enums.modele_dpe[dpe_in.administratif.enum_modele_dpe_id];

  if (modele !== 'dpe 3cl 2021 méthode logement') {
    console.error('ERREUR: Moteur DPE non implémenté pour le modèle: ' + modele);
    process.exit(1);
  }

  // Traitement sans nettoyage (pour comparaison fidèle)
  const dpe_out = calcul_3cl(dpe_in);

  // Écriture en sortie standard du résultat JSON
  console.log(JSON.stringify(dpe_out, null, 2));

} catch (err) {
  console.error('ERREUR: Exception lors du traitement du DPE:', err instanceof Error ? err.message : err);
  process.exit(1);
}
