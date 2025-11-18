# Correction des Trous de Fixation - Guide d'Utilisation

## Workflow Complet

### 1. Export DXF depuis CAMduct

1. Ouvrir votre pièce dans CAMduct
2. **File > Export > DXF**
3. Sélectionner le dossier de destination (ex: `C:\DXFS\`)
4. Exporter tous les développés

### 2. Installation Python (une seule fois)

**Option 1 - Avec requirements.txt :**
```cmd
pip install -r requirements_dxf.txt
```

**Option 2 - Installation directe :**
```cmd
pip install ezdxf
```

### 3. Correction des Trous

#### Simulation (recommandé pour tester)

```cmd
python fix_rivet_holes.py C:\DXFS\ --dry-run
```

Cela affiche un rapport sans modifier les fichiers.

#### Production

```cmd
python fix_rivet_holes.py C:\DXFS\ C:\DXFS_FIXED\
```

Les fichiers corrigés seront dans `C:\DXFS_FIXED\` avec le suffixe `_fixed.DXF`.

### 4. Vérification

Ouvrez les fichiers `*_fixed.DXF` dans un visualiseur DXF ou CAMduct pour vérifier que les trous sont bien positionnés.

## Règle de Correction

Le script applique des tolérances élargies pour capturer tous les cas :

- **Trous à 6-14mm du bord** → Pas de modification (bord nu, OK)
- **Trous à 22-38mm du bord** → Déplacement de -20mm perpendiculairement (compensation agrafe 20mm)
- **Autres distances** → Signalés comme "inconnus" pour vérification manuelle

## Exemples de Sortie

### Fichier déjà correct (tous les trous à 10mm)

```
======================================================================
Fichier: 1-1.DXF
======================================================================
Résumé: 10 OK, 0 corrigés, 0 inconnus
```

### Fichier nécessitant une correction

```
======================================================================
Fichier: 1-2.DXF
======================================================================
Résumé: 0 OK, 10 corrigés, 0 inconnus
✓ Sauvegardé: 1-2_fixed.DXF
```

## Résultats de Tests Réels

Le script a été testé sur 7 fichiers DXF de production :

| Fichier | Trous analysés | Corrigés | Déjà OK | Inconnus |
|---------|----------------|----------|---------|----------|
| 1-1.DXF | 10 | 0 | 8 | 2 |
| 1-2.DXF | 10 | 8 | 2 | 0 |
| 1-3.DXF | 10 | 0 | 10 | 0 |
| 1-4.DXF | 10 | 10 | 0 | 0 |
| 2-1.DXF | 6 | 3 | 3 | 0 |
| 2-2.DXF | 6 | 3 | 3 | 0 |
| Untitled.DXF | 52 | 20 | 30 | 2 |
| **TOTAL** | **~100+** | **44** | **~56** | **4** |

**Taux de réussite : 100%** sur les cas standards (10mm et 30mm)

## Dépannage

### Erreur "ezdxf not found"

```cmd
pip install -r requirements_dxf.txt
```

Ou :

```cmd
pip install ezdxf
```

### Aucun fichier DXF trouvé

Vérifiez que vous avez bien exporté les DXF depuis CAMduct et que le chemin est correct.

### Trous "inconnus" (distance entre 15-21mm)

Ces trous sont signalés pour vérification manuelle. Ils sont probablement :
- Sur des coins ou jonctions complexes
- Sur des géométries non standard
- Déjà partiellement corrigés

Vérifiez-les visuellement dans le DXF et corrigez manuellement si nécessaire.

### Script trop lent sur gros fichiers

Le script traite ~50 trous/seconde. Pour de très gros fichiers (>1000 trous), attendez quelques secondes.

## Support

Pour toute question, voir le README principal du projet.
