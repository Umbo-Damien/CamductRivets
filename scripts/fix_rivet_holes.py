#!/usr/bin/env python3
"""
CAMduct DXF Rivet Hole Correction Script

Logic:
- Rivet holes (Ø 4.2mm) at 10mm from edge = OK (raw edge)
- Rivet holes (Ø 4.2mm) at 30mm from edge = Move -20mm perpendicularly
  (30mm = 10mm offset + 20mm flange → bring back to 10mm from edge)
- Other diameters = Ignored (not rivet holes)
"""

import ezdxf
import sys
import math
from pathlib import Path

# Configuration
RIVET_DIAMETER = 4.2  # mm - rivet hole diameter
DIAMETER_TOLERANCE = 0.3  # mm - diameter tolerance (4.2 ± 0.3)
TARGET_DISTANCE = 10.0  # mm - target distance from edge
TOLERANCE_10MM = 4.0  # mm - tolerance to detect holes at ~10mm (6-14mm)
TOLERANCE_30MM = 8.0  # mm - tolerance to detect holes at ~30mm (22-38mm)
CORRECTION = -20.0  # mm - correction to apply to holes

def point_to_segment_distance_and_direction(px, py, x1, y1, x2, y2):
    """
    Calculate distance from point to segment AND perpendicular direction
    
    Returns:
        (distance, direction_x, direction_y) where direction is normalized
    """
    # Segment vector
    dx = x2 - x1
    dy = y2 - y1
    
    # Squared length
    length_sq = dx*dx + dy*dy
    
    if length_sq == 0:
        dist = math.sqrt((px-x1)**2 + (py-y1)**2)
        return dist, 0, 0
    
    # Project point onto line
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / length_sq))
    
    # Closest point on segment
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    
    # Distance
    dist = math.sqrt((px - proj_x)**2 + (py - proj_y)**2)
    
    # Perpendicular vector (from segment to point)
    if dist > 0:
        perp_x = (px - proj_x) / dist
        perp_y = (py - proj_y) / dist
    else:
        perp_x, perp_y = 0, 0
    
    return dist, perp_x, perp_y

def fix_holes_in_dxf(dxf_path, output_path=None, dry_run=False):
    """
    Fix rivet holes in a DXF file
    """
    print(f"\n{'='*70}")
    print(f"File: {dxf_path.name}")
    print(f"{'='*70}")
    
    # Load DXF
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    
    # Extract lines and circles
    lines = [e for e in msp if e.dxftype() == 'LINE']
    circles = [e for e in msp if e.dxftype() == 'CIRCLE']
    
    if not circles:
        print(" No holes found")
        return 0
    
    holes_corrected = 0
    holes_ok = 0
    holes_unknown = 0
    holes_ignored = 0
    
    print(f"\n{'Hole':<6} {'Position':<20} {'Ø':<6} {'Dist':<8} {'Action':<30}")
    print("-" * 76)
    
    for i, circle in enumerate(circles, 1):
        cx, cy = circle.dxf.center.x, circle.dxf.center.y
        radius = circle.dxf.radius
        diameter = radius * 2
        
        # Filter by diameter: only process rivet holes (Ø 4.2mm)
        if not (RIVET_DIAMETER - DIAMETER_TOLERANCE <= diameter <= RIVET_DIAMETER + DIAMETER_TOLERANCE):
            # Ignore holes that are not rivet holes
            holes_ignored += 1
            if not dry_run:
                continue  # Don't display in production mode
            print(f"  {i:<4} ({cx:.1f}, {cy:.1f}){'':<8} {diameter:.1f}mm {'':>8} Ignored (Ø ≠ 4.2mm)")
            continue
        
        # Find closest edge and perpendicular direction
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
        
        # Determine action
        pos_str = f"({cx:.1f}, {cy:.1f})"
        diam_str = f"{diameter:.1f}mm"
        
        if TARGET_DISTANCE - TOLERANCE_10MM <= min_dist <= TARGET_DISTANCE + TOLERANCE_10MM:
            # Hole at ~10mm = OK
            action = "OK (already at 10mm)"
            marker = "="
            holes_ok += 1
            
        elif 30.0 - TOLERANCE_30MM <= min_dist <= 30.0 + TOLERANCE_30MM:
            # Hole at ~30mm = To correct
            action = f"Move {CORRECTION}mm"
            marker = ""
            
            if not dry_run:
                # Calculate new position
                new_x = cx + best_perp_x * CORRECTION
                new_y = cy + best_perp_y * CORRECTION
                circle.dxf.center = (new_x, new_y, circle.dxf.center.z)
            
            holes_corrected += 1
            
        else:
            # Unusual distance
            action = f"? (distance: {min_dist:.1f}mm)"
            marker = "?"
            holes_unknown += 1
        
        print(f"{marker} {i:<4} {pos_str:<20} {diam_str:<6} {min_dist:>6.1f}mm {action}")
    
    print("-" * 76)
    summary = f"Summary: {holes_ok} OK, {holes_corrected} corrected, {holes_unknown} unknown"
    if holes_ignored > 0:
        summary += f", {holes_ignored} ignored (Ø ≠ 4.2mm)"
    print(summary)
    
    # Save
    if not dry_run and holes_corrected > 0:
        if output_path is None:
            output_path = dxf_path.parent / f"{dxf_path.stem}_fixed.DXF"
        
        doc.saveas(output_path)
        print(f" Saved: {output_path.name}")
    
    return holes_corrected

def process_directory(input_dir, output_dir=None, dry_run=False):
    """
    Process all DXF files in a directory
    """
    input_path = Path(input_dir)
    dxf_files = list(input_path.glob("*.dxf")) + list(input_path.glob("*.DXF"))
    
    if not dxf_files:
        print(f" No DXF files found in {input_dir}")
        return
    
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = None
    
    print(f"\n{'='*70}")
    print(f"Processing {len(dxf_files)} DXF files")
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
    print(f" TOTAL: {total_holes} holes corrected in {len(dxf_files)} files")
    print(f"{'='*70}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix_rivet_holes.py <dxf_file_or_directory> [output_directory] [--dry-run]")
        print("\nExamples:")
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
