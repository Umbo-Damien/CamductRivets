# CamductRivets - Rivet Hole Positioning Fix for CAMduct

[![Python Tests](https://github.com/Umbo-Damien/CamductRivets/actions/workflows/python-test.yml/badge.svg)](https://github.com/Umbo-Damien/CamductRivets/actions/workflows/python-test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

[🇫🇷 Version française](README_FR.md)

## Problem Statement

CAMduct positions fixing holes symmetrically at 10mm from the part edge. For rivet assembly with 20mm flanges, this position is only correct for one side:

- **Raw edge**: Holes at 10mm → ✓ OK (correct position at -10mm from edge)
- **Edge with 20mm flange**: Holes at 10mm → ✗ Should be at -10mm from edge, but the flange shifts them to +10mm (30mm from developed part edge)

## Solution: DXF Post-Processing

After attempting to use COD scripts (limited API), the chosen solution is **post-processing of exported DXF files**:

1. **CAMduct** generates parts with holes at 10mm (symmetric)
2. **Export DXF** of developed parts from CAMduct
3. **Python script** automatically corrects holes at 30mm → 10mm
4. **Re-import** into CAMduct or send directly to cutting

### Current CAMduct Limitation

According to Autodesk documentation:
- Only a **global Inset/Offset** is available for the hole line
- "Allow holes one side only" option (holes on both sides or one side only)
- **No option** to define different offsets per side (+10mm on one side, -10mm on the other)

Reference: https://help.autodesk.com/view/FABRICATION/ENU/?guid=GUID-7A589738-4B1D-4D93-A98B-D848281E653D

## Installation

```bash
pip install -r requirements_dxf.txt
```

Or directly:

```bash
pip install ezdxf
```

## CAMduct Configuration

Before using this script, you need to configure fixing holes in CAMduct:

### 1. Database Configuration - Pattern Options

1. Open **Database** in CAMduct
2. Go to **Fittings** tab
3. Select **Pattern Options** in the left panel
4. Click on the **Holes** tab
5. Configure **Fixing Holes** section:
   - **Hole Diameter**: `4.2` mm (rivet hole size)
   - **Hole Spacing (Shoulder) Distance**: `25.0` mm (or as needed)
   - **Spacing**: `110.0` mm (or as needed)
   - **Hole Inset**: `0.0` mm
   - Check **Draw Holes** ✓
   - Check **Develop Holes** ✓

![CAMduct Database - Holes Configuration](docs/images/camduct-database-holes.png)

### 2. Takeoff Configuration - Item Information

To display fixing holes information in takeoff reports:

**Note:** These settings are only accessible from within a project. Open a project, select an item, then the **Takeoff** button will appear.

1. Go to **Takeoff** > **Customize Main Takeoff**
2. In **Item Information** tab
3. Add **Fixing Holes** to the displayed fields list
4. This will show fixing hole information in your reports

![CAMduct Takeoff - Fixing Holes](docs/images/camduct-takeoff-fixing-holes.png)

**📖 For detailed configuration instructions, see [CAMduct Setup Guide](docs/CAMDUCT_SETUP.md)**

## Usage

### 1. Export DXF from CAMduct

1. Open the part in CAMduct
2. **File > Export > DXF** (or equivalent)
3. Export all developed parts to a folder

### 2. Automatic Correction

```bash
# Simulation (dry-run)
python scripts/fix_rivet_holes.py /path/to/dxf/ --dry-run

# Production (generates *_fixed.DXF files)
python scripts/fix_rivet_holes.py /path/to/dxf/ /path/to/output/
```

### 3. Result

The script:
- ✅ **Smart filtering**: Processes only rivet holes (Ø 4.2mm ± 0.3mm)
- ✅ Automatically detects holes at 30mm from edge
- ✅ Moves them -20mm **perpendicular to the edge** (brings back to 10mm)
- ✅ Leaves holes already at 10mm untouched
- ✅ Ignores other holes (non-rivets)
- ✅ Works on **all geometries** (straight edges, angled, etc.)

## Output Example

```
======================================================================
File: 1-2.DXF
======================================================================

Hole   Position             Ø      Dist     Action                        
----------------------------------------------------------------------------
✓ 1    (368.1, 390.4)       4.2mm    29.6mm Move -20.0mm
✓ 2    (289.1, 366.8)       4.2mm    30.0mm Move -20.0mm
= 3    (210.1, 343.3)       4.2mm    10.0mm OK (already at 10mm)
⊗ 4    (150.0, 200.0)       6.0mm    15.0mm Ignored (Ø ≠ 4.2mm)
...
----------------------------------------------------------------------------
Summary: 5 OK, 5 corrected, 0 unknown, 2 ignored (Ø ≠ 4.2mm)
✓ Saved: 1-2_fixed.DXF

⚠ Note: Holes at ~30mm are often related to fold marks or notches.
Visual validation is always recommended.
```

## Features

- ✅ **Smart filtering**: Processes only rivet holes (Ø 4.2mm ± 0.3mm)
- ✅ Automatic detection of holes at 10mm or 30mm (with tolerances)
- ✅ Perpendicular displacement to edge (any geometry)
- ✅ Batch processing of multiple DXF files
- ✅ Dry-run mode for simulation
- ✅ Detailed report per file and per hole (with diameter)
- ✅ Handles angled and complex edges
- ✅ Extended tolerances: 6-14mm (OK) and 22-38mm (to correct)
- ✅ Automatically ignores non-rivet holes (other diameters)

## Requirements

- Python 3.6+
- `ezdxf` library (see Installation)
- CAMduct for DXF export

## Test Results

Tested on 7 real DXF files:
- **44 holes corrected** successfully
- **~50+ holes** already correct (not modified)
- **2 holes** flagged for manual verification (intermediate distance)
- **100% success rate** on standard cases

## Known Limitations

1. **Holes between 15-21mm**: Flagged as "unknown", manual verification recommended
2. **Very complex geometries**: May require tolerance adjustment
3. **Corrupted DXF files**: Script ignores invalid files

## Project Structure

```
CamductRivets/
├── scripts/
│   └── fix_rivet_holes.py       # Main script
├── examples/
│   └── README.md                # Usage examples
├── .github/
│   └── workflows/
│       └── python-test.yml      # CI/CD GitHub Actions
├── requirements_dxf.txt         # Python dependencies
├── UTILISATION.md               # Detailed usage guide (French)
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT License
└── README.md                    # This file
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the project
2. Create a branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

## License

MIT - See [LICENSE](LICENSE) file for details.

## Author

Project created to solve rivet assembly positioning issues in CAMduct.

## Support

- 📖 [Complete documentation](README.md)
- 📝 [Usage guide](UTILISATION.md) (French)
- 💡 [Examples](examples/README.md)
- 🐛 [Report a bug](https://github.com/Umbo-Damien/CamductRivets/issues)
- ⭐ [Star the project](https://github.com/Umbo-Damien/CamductRivets)
