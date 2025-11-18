# Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2025-11-18

### Changed
- **Complete English translation** of the project
  - Python script: all comments, docstrings, and messages in English
  - README.md now in English (French version: README_FR.md)
  - UTILISATION.md renamed to UTILISATION_FR.md
  - User-facing messages translated
- Bilingual documentation maintained

### Added
- English README.md as main documentation
- Link to French version in English README

## [1.1.0] - 2025-11-18

### Ajouté
- **Filtrage par diamètre** : Le script traite uniquement les trous de rivets (Ø 4.2mm ± 0.3mm)
- Colonne "Ø" dans le rapport pour afficher le diamètre de chaque trou
- Compteur de trous ignorés (non-rivets) dans le résumé
- Avertissement sur les trous à ~30mm (souvent liés aux marques de pliage)

### Modifié
- Clarification de la logique dans la documentation (trous à -10mm du bord)
- Amélioration de l'affichage du rapport avec le diamètre
- Documentation mise à jour avec exemples de filtrage

### Sécurité
- Prévention de la modification accidentelle de trous non-rivets

## [1.0.0] - 2025-11-18

### Ajouté
- Script Python `fix_rivet_holes.py` pour correction automatique des trous de fixation
- Post-traitement des fichiers DXF exportés depuis CAMduct
- Détection automatique des trous à 10mm (OK) et 30mm (à corriger)
- Déplacement perpendiculaire au bord (fonctionne sur toutes géométries)
- Mode dry-run pour simulation
- Rapport détaillé par fichier et par trou
- Tolérances élargies : 6-14mm (OK) et 22-38mm (à corriger)
- Traitement par lot de plusieurs DXF
- Documentation complète (README.md, UTILISATION.md)
- Tests sur 7 fichiers DXF réels avec 100% de réussite

### Testé
- 7 fichiers DXF de production
- ~100+ trous analysés
- 44 trous corrigés avec succès
- 2 trous signalés pour vérification manuelle (distance intermédiaire 21.7mm)

### Technique
- Calcul de distance point-segment pour mesure précise
- Vecteur perpendiculaire normalisé pour déplacement correct
- Gestion des bords inclinés et complexes
- Bibliothèque ezdxf pour manipulation DXF

## [0.2.0] - 2025-11-18 (abandonné)

### Tenté
- Scripts COD (`.cod`) pour modification directe dans CAMduct
- Accès à l'API CAMduct via scripts VBScript-like
- Détection des seams et fixing holes

### Abandonné
- L'API COD ne permet pas d'accéder aux fixing holes individuels
- Seules les propriétés de haut niveau (seams, connectors) sont accessibles
- Pas d'accès aux coordonnées des trous via scripts COD

### Leçons apprises
- Les scripts COD sont limités aux propriétés globales
- Pour modifier les trous individuels, il faut soit :
  - Un Add-in C# avec accès à l'API .NET complète
  - Post-traitement des DXF exportés (solution retenue)

## [0.1.0] - 2025-11-18 (initial)

### Recherche
- Analyse de la problématique d'assemblage par rivets
- Étude de la documentation Autodesk CAMduct
- Identification de la limitation : pas d'offset asymétrique natif
- Exploration des solutions possibles (scripts COD, API .NET, DXF)
