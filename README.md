# Dynamic QGIS Map Layouts
Scripts to create dynamically adapting Map Layouts in QGIS. Refering to talk "Arbeit mit standardisierten Karten - Dynamische Kartenerstellung mit PyQGIS" at FOSSGIS-Konferenz 2026.

## Usage
1. Place startup.py script in QGIS' Python home directory:
    - Windows: ```AppData\Roaming\QGIS\QGIS3```
    - Linux: ```.local/share/QGIS/QGIS3```
    - Mac: ```Library/Application Support/QGIS/QGIS3```

2. Set parameters at top of the Layout script to your liking, define paths, and run script inside your Python console in QGIS.

3. Open Layout in QGIS GUI, and: 
    - Click "Refresh view (F5)" a few times, until Layout is not changing anymore
    - If the map is not rendering, click "Set Map Extent to Match Main Canvas Extent" to inizialize rendering
    - Adapt scale bar size manually


## Known Limitations
- Text label height calculation can get inaccurate if label has many lines
- Expression evaluation get's lost sometimes. Save QGIS Project, reopen and refresh view. In case that doesn't help rerun the script. However, remember to rename your Layout before to prevent it from being overwritten
- Legend label autowrap is not implemented as this function was added in QGIS v3.44 while these scripts are written for LTR v3.40
