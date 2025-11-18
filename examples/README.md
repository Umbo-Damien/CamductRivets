# Exemples d'Utilisation

## Exemple 1 : Correction d'un seul fichier DXF

```bash
python scripts/fix_rivet_holes.py piece.DXF piece_fixed.DXF
```

## Exemple 2 : Traitement par lot d'un dossier

```bash
python scripts/fix_rivet_holes.py ./dxf_input/ ./dxf_output/
```

## Exemple 3 : Simulation (dry-run)

```bash
python scripts/fix_rivet_holes.py ./dxf_input/ --dry-run
```

Affiche un rapport détaillé sans modifier les fichiers.

## Exemple 4 : Workflow complet

```bash
# 1. Export DXF depuis CAMduct
# (Manuellement dans CAMduct : File > Export > DXF)

# 2. Simulation pour vérifier
python scripts/fix_rivet_holes.py C:/DXFS/ --dry-run

# 3. Correction en production
python scripts/fix_rivet_holes.py C:/DXFS/ C:/DXFS_FIXED/

# 4. Vérification des résultats
# Ouvrir les fichiers *_fixed.DXF dans un visualiseur DXF
```

## Sortie Attendue

```
======================================================================
Fichier: piece.DXF
======================================================================

Trou   Position             Dist     Action                        
----------------------------------------------------------------------
✓ 1    (368.1, 390.4)         29.6mm Déplacer de -20.0mm
= 2    (289.1, 366.8)         10.0mm OK (déjà à 10mm)
✓ 3    (210.1, 343.3)         30.0mm Déplacer de -20.0mm
----------------------------------------------------------------------
Résumé: 1 OK, 2 corrigés, 0 inconnus
✓ Sauvegardé: piece_fixed.DXF
```

## Cas d'Usage Réels

### Pièce rectangulaire simple
- 10 trous
- 5 à corriger (côté avec agrafe)
- 5 déjà OK (côté nu)

### Pièce complexe avec bords inclinés
- 52 trous
- 20 à corriger
- 30 déjà OK
- 2 signalés pour vérification manuelle

### Lot de production
- 7 fichiers DXF
- 44 trous corrigés au total
- Temps de traitement : < 1 seconde
