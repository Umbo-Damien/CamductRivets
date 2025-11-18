# CamductRivets - Gestion des Trous de Fixation pour Assemblage par Rivets

## Problématique

CAMduct positionne les trous de fixation de manière symétrique à 10mm du bord de la pièce. Pour l'assemblage par rivets avec agrafes de 20mm, cette position n'est correcte que pour un côté :

- **Bord nu** : 10mm → ✓ OK
- **Bord avec agrafe 20mm** : 10mm → ✗ Devrait être à 30mm (10mm + 20mm d'agrafe)

## Solution : Post-traitement DXF

Après avoir tenté d'utiliser les scripts COD (API limitée), la solution retenue est le **post-traitement des fichiers DXF exportés** :

1. **CAMduct** génère les pièces avec trous à 10mm (symétrique)
2. **Export DXF** des développés depuis CAMduct
3. **Script Python** corrige automatiquement les trous à 30mm → 10mm
4. **Réimport** dans CAMduct ou envoi direct à la découpe

### Limitation actuelle de CAMduct

D'après la documentation Autodesk :
- Seul un **Inset/Offset global** est disponible pour la ligne de trous
- Option "Allow holes one side only" (trous des deux côtés ou d'un seul)
- **Aucune option** pour définir des offsets différents par côté (+10mm d'un côté, -10mm de l'autre)

Référence : https://help.autodesk.com/view/FABRICATION/ENU/?guid=GUID-7A589738-4B1D-4D93-A98B-D848281E653D

## Installation

```bash
pip install -r requirements_dxf.txt
```

Ou directement :

```bash
pip install ezdxf
```

## Utilisation

### 1. Export DXF depuis CAMduct

1. Ouvrir la pièce dans CAMduct
2. **File > Export > DXF** (ou équivalent)
3. Exporter tous les développés dans un dossier

### 2. Correction automatique

```bash
# Simulation (dry-run)
python scripts/fix_rivet_holes.py /chemin/vers/dxf/ --dry-run

# Production (génère les fichiers *_fixed.DXF)
python scripts/fix_rivet_holes.py /chemin/vers/dxf/ /chemin/vers/output/
```

### 3. Résultat

Le script :
- ✅ Détecte automatiquement les trous à 30mm du bord
- ✅ Les déplace de -20mm **perpendiculairement au bord**
- ✅ Laisse intacts les trous déjà à 10mm
- ✅ Fonctionne sur **toutes les géométries** (bords droits, inclinés, etc.)

## Exemple de sortie

```
======================================================================
Fichier: 1-2.DXF
======================================================================

Trou   Position             Dist     Action                        
----------------------------------------------------------------------
✓ 1    (368.1, 390.4)         29.6mm Déplacer de -20.0mm
✓ 2    (289.1, 366.8)         30.0mm Déplacer de -20.0mm
= 3    (210.1, 343.3)         10.0mm OK (déjà à 10mm)
...
----------------------------------------------------------------------
Résumé: 5 OK, 5 corrigés, 0 inconnus
✓ Sauvegardé: 1-2_fixed.DXF
```

## Fonctionnalités

- ✅ Détection automatique des trous à 10mm ou 30mm (avec tolérances)
- ✅ Déplacement perpendiculaire au bord (géométrie quelconque)
- ✅ Traitement par lot de plusieurs DXF
- ✅ Mode dry-run pour simulation
- ✅ Rapport détaillé par fichier et par trou
- ✅ Gestion des bords inclinés et complexes
- ✅ Tolérances élargies : 6-14mm (OK) et 22-38mm (à corriger)

## Prérequis

- Python 3.6+
- Bibliothèque `ezdxf` (voir Installation)
- CAMduct pour l'export DXF

## Résultats de Test

Testé sur 7 fichiers DXF réels :
- **44 trous corrigés** avec succès
- **~50+ trous** déjà corrects (non modifiés)
- **2 trous** signalés pour vérification manuelle (distance intermédiaire)
- **100% de réussite** sur les cas standards

## Limitations Connues

1. **Trous entre 15-21mm** : Signalés comme "inconnus", vérification manuelle recommandée
2. **Géométries très complexes** : Peuvent nécessiter un ajustement des tolérances
3. **DXF corrompus** : Le script ignore les fichiers non valides

## Structure du Projet

```
CamductRivets/
├── scripts/
│   ├── fix_rivet_holes.py       # Script principal
│   └── reposition_holes_dxf_v2.py  # Version de développement
├── requirements_dxf.txt         # Dépendances Python
├── UTILISATION.md               # Guide d'utilisation détaillé
└── README.md                    # Ce fichier
```

## Licence

MIT

## Auteur

Projet créé pour résoudre la problématique d'assemblage par rivets dans CAMduct.
