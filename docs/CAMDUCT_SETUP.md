# CAMduct Setup Guide for Rivet Holes

[🇫🇷 Version française](#guide-de-configuration-camduct-pour-les-trous-de-rivets)

## English Version

### Prerequisites

- CAMduct 2020 or later
- Administrative access to Database configuration

### Step 1: Configure Fixing Holes in Database

1. **Open Database**
   - Launch CAMduct
   - Click on **Database** button in the main toolbar

2. **Navigate to Pattern Options**
   - Click on the **Fittings** tab
   - In the left panel, expand the tree and select **Pattern Options**

3. **Configure Holes Tab**
   - Click on the **Holes** tab at the top
   - Scroll down to the **Fixing Holes** section

4. **Set Fixing Holes Parameters**
   
   | Parameter | Value | Description |
   |-----------|-------|-------------|
   | **Hole Diameter** | `4.2` mm | Standard rivet hole diameter |
   | **Hole Spacing (Shoulder) Distance** | `25.0` mm | Distance between holes |
   | **Hole Spacing (Shoulder) Fraction** | `10` | Fraction for spacing calculation |
   | **Spacing** | `110.0` mm | Overall spacing |
   | **Number Of Holes** | `99` | Maximum number of holes |
   | **Hole Inset** | `0.0` mm | Distance from edge (will be corrected by script) |
   | **Allow holes one side only** | ☐ | Unchecked (holes on both sides) |
   | **Draw Holes** | ✓ | Checked (display holes in 3D) |
   | **Develop Holes** | ✓ | Checked (include in DXF export) |
   | **Dynamic Hole Adjust** | `50.0` | Adjustment factor |

5. **Apply Changes**
   - Click **Apply** button
   - Click **OK** to close the Database window

### Step 2: Add Fixing Holes to Takeoff Reports

1. **Open Takeoff Customization**
   - Go to **Takeoff** menu
   - Select **Customize Main Takeoff**

2. **Configure Item Information**
   - Click on the **Item Information** tab
   - In the left panel (available fields), locate **Fixing Holes**
   - Select **Fixing Holes** and click the **→** arrow button to add it to the right panel
   - This will display fixing hole information in your takeoff reports

3. **Save Configuration**
   - Click **OK** to save and close

### Step 3: Verify Configuration

1. **Create a Test Part**
   - Create a simple rectangular duct with a Pittsburgh seam
   - Verify that fixing holes appear in the 3D view

2. **Export DXF**
   - Select the part
   - Go to **File > Export > DXF**
   - Export the developed part
   - Open the DXF file and verify that circles (holes) are present

3. **Check Hole Diameter**
   - In the DXF file, verify that hole diameter is 4.2mm
   - If not, adjust the **Hole Diameter** setting in Database

### Troubleshooting

**Holes not appearing in 3D view:**
- Check that **Draw Holes** is enabled in Database
- Verify that the seam type supports fixing holes

**Holes not in DXF export:**
- Check that **Develop Holes** is enabled in Database
- Ensure you're exporting developed parts, not 3D geometry

**Wrong hole diameter:**
- Adjust **Hole Diameter** in Database > Fittings > Pattern Options > Holes
- Re-export DXF after changes

---

## Guide de Configuration CAMduct pour les Trous de Rivets

### Prérequis

- CAMduct 2020 ou ultérieur
- Accès administrateur à la configuration de la base de données

### Étape 1 : Configurer les Trous de Fixation dans la Base de Données

1. **Ouvrir la Base de Données**
   - Lancer CAMduct
   - Cliquer sur le bouton **Database** dans la barre d'outils principale

2. **Naviguer vers Pattern Options**
   - Cliquer sur l'onglet **Fittings**
   - Dans le panneau de gauche, développer l'arborescence et sélectionner **Pattern Options**

3. **Configurer l'Onglet Holes**
   - Cliquer sur l'onglet **Holes** en haut
   - Faire défiler jusqu'à la section **Fixing Holes**

4. **Définir les Paramètres des Trous de Fixation**
   
   | Paramètre | Valeur | Description |
   |-----------|--------|-------------|
   | **Hole Diameter** | `4.2` mm | Diamètre standard des trous de rivets |
   | **Hole Spacing (Shoulder) Distance** | `25.0` mm | Distance entre les trous |
   | **Hole Spacing (Shoulder) Fraction** | `10` | Fraction pour le calcul de l'espacement |
   | **Spacing** | `110.0` mm | Espacement global |
   | **Number Of Holes** | `99` | Nombre maximum de trous |
   | **Hole Inset** | `0.0` mm | Distance du bord (sera corrigée par le script) |
   | **Allow holes one side only** | ☐ | Décoché (trous des deux côtés) |
   | **Draw Holes** | ✓ | Coché (afficher les trous en 3D) |
   | **Develop Holes** | ✓ | Coché (inclure dans l'export DXF) |
   | **Dynamic Hole Adjust** | `50.0` | Facteur d'ajustement |

5. **Appliquer les Modifications**
   - Cliquer sur le bouton **Apply**
   - Cliquer sur **OK** pour fermer la fenêtre Database

### Étape 2 : Ajouter les Trous de Fixation aux Rapports Takeoff

1. **Ouvrir la Personnalisation du Takeoff**
   - Aller dans le menu **Takeoff**
   - Sélectionner **Customize Main Takeoff**

2. **Configurer Item Information**
   - Cliquer sur l'onglet **Item Information**
   - Dans le panneau de gauche (champs disponibles), localiser **Fixing Holes**
   - Sélectionner **Fixing Holes** et cliquer sur la flèche **→** pour l'ajouter au panneau de droite
   - Cela affichera les informations des trous de fixation dans vos rapports

3. **Sauvegarder la Configuration**
   - Cliquer sur **OK** pour sauvegarder et fermer

### Étape 3 : Vérifier la Configuration

1. **Créer une Pièce de Test**
   - Créer un conduit rectangulaire simple avec une agrafe Pittsburgh
   - Vérifier que les trous de fixation apparaissent dans la vue 3D

2. **Exporter en DXF**
   - Sélectionner la pièce
   - Aller dans **File > Export > DXF**
   - Exporter le développé
   - Ouvrir le fichier DXF et vérifier que les cercles (trous) sont présents

3. **Vérifier le Diamètre des Trous**
   - Dans le fichier DXF, vérifier que le diamètre des trous est de 4.2mm
   - Si ce n'est pas le cas, ajuster le paramètre **Hole Diameter** dans Database

### Dépannage

**Les trous n'apparaissent pas dans la vue 3D :**
- Vérifier que **Draw Holes** est activé dans Database
- Vérifier que le type d'agrafe supporte les trous de fixation

**Les trous ne sont pas dans l'export DXF :**
- Vérifier que **Develop Holes** est activé dans Database
- S'assurer d'exporter les développés, pas la géométrie 3D

**Mauvais diamètre de trou :**
- Ajuster **Hole Diameter** dans Database > Fittings > Pattern Options > Holes
- Ré-exporter le DXF après les modifications
