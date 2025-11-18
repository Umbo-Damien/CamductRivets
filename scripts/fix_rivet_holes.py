#!/usr/bin/env python3
"""
Script de correction des trous de fixation dans les fichiers DXF CAMduct

Logique:
- Trous de rivets (Ø 4.2mm) à 10mm du bord = OK (bord nu)
- Trous de rivets (Ø 4.2mm) à 30mm du bord = Déplacer de -20mm perpendiculairement
  (30mm = 10mm offset + 20mm agrafe → ramener à 10mm du bord)
- Autres diamètres = Ignorés (pas des trous de rivets)
"""

import ezdxf
import sys
import math
from pathlib import Path

# Configuration
RIVET_DIAMETER = 4.2  # mm - diamètre des trous de rivets
DIAMETER_TOLERANCE = 0.3  # mm - tolérance sur le diamètre (4.2 ± 0.3)
TARGET_DISTANCE = 10.0  # mm - distance cible finale du bord
TOLERANCE_10MM = 4.0  # mm - tolérance pour détecter les trous à ~10mm (6-14mm)
TOLERANCE_30MM = 8.0  # mm - tolérance pour détecter les trous à ~30mm (22-38mm)
CORRECTION = -20.0  # mm - correction à appliquer aux trous à corriger

def point_to_segment_distance_and_direction(px, py, x1, y1, x2, y2):
    """
    Calcule la distance d'un point à un segment ET la direction perpendiculaire
    
    Returns:
        (distance, direction_x, direction_y) où direction est normalisée
    """
    # Vecteur du segment
    dx = x2 - x1
    dy = y2 - y1
    
    # Longueur au carré
    length_sq = dx*dx + dy*dy
    
    if length_sq == 0:
        dist = math.sqrt((px-x1)**2 + (py-y1)**2)
        return dist, 0, 0
    
    # Projection du point sur la ligne
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / length_sq))
    
    # Point le plus proche sur le segment
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    
    # Distance
    dist = math.sqrt((px - proj_x)**2 + (py - proj_y)**2)
    
    # Vecteur perpendiculaire (du segment vers le point)
    if dist > 0:
        perp_x = (px - proj_x) / dist
        perp_y = (py - proj_y) / dist
    else:
        perp_x, perp_y = 0, 0
    
    return dist, perp_x, perp_y

def fix_holes_in_dxf(dxf_path, output_path=None, dry_run=False):
    """
    Corrige les trous de fixation dans un fichier DXF
    """
    print(f"\n{'='*70}")
    print(f"Fichier: {dxf_path.name}")
    print(f"{'='*70}")
    
    # Charger le DXF
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    
    # Extraire lignes et cercles
    lines = [e for e in msp if e.dxftype() == 'LINE']
    circles = [e for e in msp if e.dxftype() == 'CIRCLE']
    
    if not circles:
        print("⚠ Aucun trou trouvé")
        return 0
    
    holes_corrected = 0
    holes_ok = 0
    holes_unknown = 0
    holes_ignored = 0
    
    print(f"\n{'Trou':<6} {'Position':<20} {'Ø':<6} {'Dist':<8} {'Action':<30}")
    print("-" * 76)
    
    for i, circle in enumerate(circles, 1):
        cx, cy = circle.dxf.center.x, circle.dxf.center.y
        radius = circle.dxf.radius
        diameter = radius * 2
        
        # Filtrer par diamètre : traiter uniquement les trous de rivets (Ø 4.2mm)
        if not (RIVET_DIAMETER - DIAMETER_TOLERANCE <= diameter <= RIVET_DIAMETER + DIAMETER_TOLERANCE):
            # Ignorer les trous qui ne sont pas des trous de rivets
            holes_ignored += 1
            if not dry_run:
                continue  # Ne pas afficher en mode production
            print(f"⊗ {i:<4} ({cx:.1f}, {cy:.1f}){'':<8} {diameter:.1f}mm {'':>8} Ignoré (Ø ≠ 4.2mm)")
            continue
        
        # Trouver le bord le plus proche et la direction perpendiculaire
        min_dist = float('inf')
        best_perp_x, best_perp_y = 0, 0
        
        for line in lines:
            x1, y1 = line.dxf.start.x, line.dxf.start.y
            x2, y2 = line.dxf.end.x, line.dxf.end.y
            
            dist, perp_x, perp_y = point_to_segment_distance_and_direction(
                cx, cy, x1, y1, x2, y2
            )
            
            if dist < min_dist:
                min_dist = dist
                best_perp_x = perp_x
                best_perp_y = perp_y
        
        # Déterminer l'action
        pos_str = f"({cx:.1f}, {cy:.1f})"
        diam_str = f"{diameter:.1f}mm"
        
        if TARGET_DISTANCE - TOLERANCE_10MM <= min_dist <= TARGET_DISTANCE + TOLERANCE_10MM:
            # Trou à ~10mm = OK
            action = "OK (déjà à 10mm)"
            marker = "="
            holes_ok += 1
            
        elif 30.0 - TOLERANCE_30MM <= min_dist <= 30.0 + TOLERANCE_30MM:
            # Trou à ~30mm = À corriger
            action = f"Déplacer de {CORRECTION}mm"
            marker = "✓"
            
            if not dry_run:
                # Calculer la nouvelle position
                new_x = cx + best_perp_x * CORRECTION
                new_y = cy + best_perp_y * CORRECTION
                circle.dxf.center = (new_x, new_y, circle.dxf.center.z)
            
            holes_corrected += 1
            
        else:
            # Distance inhabituelle
            action = f"? (distance: {min_dist:.1f}mm)"
            marker = "?"
            holes_unknown += 1
        
        print(f"{marker} {i:<4} {pos_str:<20} {diam_str:<6} {min_dist:>6.1f}mm {action}")
    
    print("-" * 76)
    summary = f"Résumé: {holes_ok} OK, {holes_corrected} corrigés, {holes_unknown} inconnus"
    if holes_ignored > 0:
        summary += f", {holes_ignored} ignorés (Ø ≠ 4.2mm)"
    print(summary)
    
    # Sauvegarder
    if not dry_run and holes_corrected > 0:
        if output_path is None:
            output_path = dxf_path.parent / f"{dxf_path.stem}_fixed.DXF"
        
        doc.saveas(output_path)
        print(f"✓ Sauvegardé: {output_path.name}")
    
    return holes_corrected

def process_directory(input_dir, output_dir=None, dry_run=False):
    """
    Traite tous les DXF d'un répertoire
    """
    input_path = Path(input_dir)
    dxf_files = list(input_path.glob("*.dxf")) + list(input_path.glob("*.DXF"))
    
    if not dxf_files:
        print(f"❌ Aucun fichier DXF trouvé dans {input_dir}")
        return
    
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = None
    
    print(f"\n{'='*70}")
    print(f"Traitement de {len(dxf_files)} fichiers DXF")
    print(f"Mode: {'DRY-RUN (simulation)' if dry_run else 'PRODUCTION'}")
    print(f"{'='*70}")
    
    total_holes = 0
    for dxf_file in sorted(dxf_files):
        if output_path:
            out_file = output_path / f"{dxf_file.stem}_fixed.DXF"
        else:
            out_file = None
        
        holes = fix_holes_in_dxf(dxf_file, out_file, dry_run=dry_run)
        total_holes += holes
    
    print(f"\n{'='*70}")
    print(f"✓ TOTAL: {total_holes} trous corrigés dans {len(dxf_files)} fichiers")
    print(f"{'='*70}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_rivet_holes.py <dxf_file_or_directory> [output_directory] [--dry-run]")
        print("\nExemples:")
        print("  python fix_rivet_holes.py input.dxf --dry-run")
        print("  python fix_rivet_holes.py ./dxf_input/")
        print("  python fix_rivet_holes.py ./dxf_input/ ./dxf_output/")
        sys.exit(1)
    
    dry_run = "--dry-run" in sys.argv
    args = [arg for arg in sys.argv[1:] if arg != "--dry-run"]
    
    input_path = Path(args[0])
    output_dir = args[1] if len(args) > 1 else None
    
    if input_path.is_file():
        fix_holes_in_dxf(input_path, dry_run=dry_run)
    elif input_path.is_dir():
        process_directory(input_path, output_dir, dry_run=dry_run)
    else:
        print(f"❌ Erreur: {input_path} n'existe pas")
        sys.exit(1)
