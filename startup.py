'''
Place this Script in 'AppData\Roaming\QGIS\QGIS3' to have the functions available on startup.
'''


from qgis.utils import qgsfunction

from qgis.core import *
from qgis.gui import *

from PyQt5.QtGui import QFontMetricsF


### Funktionen ###
@qgsfunction(args='auto', group='Custom')
def GetDynamicItemHeight(LayoutName, ItemName):
    layout_name = LayoutName
    item_name = ItemName

    # Layout abfragen
    manager = QgsProject.instance().layoutManager()
    layout = manager.layoutByName(layout_name)

    # Layout Element --> Größe des Elements --> Höhe des Elements
    get_item = layout.itemById(item_name)
    get_item_size = get_item.sizeWithUnits()
    get_item_height = get_item_size.height()

    return get_item_height


@qgsfunction(args='auto', group='Custom')
def GetDynamicItemWidth(LayoutName, ItemName):
    layout_name = LayoutName
    item_name = ItemName

    # Layout abfragen
    manager = QgsProject.instance().layoutManager()
    layout = manager.layoutByName(layout_name)

    # Layout Element --> Größe des Elements --> Breite des Elements
    get_item = layout.itemById(item_name)
    get_item_size = get_item.sizeWithUnits()
    get_item_width = get_item_size.width()

    return get_item_width


@qgsfunction(args='auto', group='Custom')
def GetDynamicItemPositionX(LayoutName, ItemName):
    layout_name = LayoutName
    item_name = ItemName

    # Layout abfragen
    manager = QgsProject.instance().layoutManager()
    layout = manager.layoutByName(layout_name)

    # Layout Element --> Position des Elements --> X-Wert
    get_item = layout.itemById(item_name)
    get_item_position = get_item.positionWithUnits()
    get_item_position_x = get_item_position.x()

    return get_item_position_x


@qgsfunction(args='auto', group='Custom')
def GetDynamicItemPositionY(LayoutName, ItemName):
    layout_name = LayoutName
    item_name = ItemName

    # Layout abfragen
    manager = QgsProject.instance().layoutManager()
    layout = manager.layoutByName(layout_name)

    # Layout Element --> Position des Elements --> Y-Wert
    get_item = layout.itemById(item_name)
    get_item_position = get_item.positionWithUnits()
    get_item_position_y = get_item_position.y()

    return get_item_position_y


@qgsfunction(args='auto', group='Custom')
def GetPageSizeWidth(LayoutName):
    layout_name = LayoutName

    # Layout abfragen
    manager = QgsProject.instance().layoutManager()
    layout = manager.layoutByName(layout_name)

    # Printseite --> Größe der Printseite --> Breite
    page = layout.pageCollection().page(0)
    size = page.pageSize()
    width_mm = size.width()

    return width_mm


@qgsfunction(args='auto', group='Custom')
def GetPageSizeHeight(LayoutName):
    layout_name = LayoutName

    # Layout abfragen
    manager = QgsProject.instance().layoutManager()
    layout = manager.layoutByName(layout_name)

    # Printseite --> Größe der Printseite --> Höhe
    page = layout.pageCollection().page(0)
    size = page.pageSize()
    height_mm = size.height()

    return height_mm


@qgsfunction(args='auto', group='Custom')
def CalcLabelHeight(layout_name, item_name, feature, parent, line_spacing=1.0):
    """
    Berechnet die tatsächliche Höhe eines QTextLabel-Items im Layout.
    line_spacing = Faktor für Zeilenabstand (z. B. 1.15 für 15% mehr Abstand)
    """

    manager = QgsProject.instance().layoutManager()
    layout = manager.layoutByName(layout_name)

    if not layout:
        return 0

    item = layout.itemById(item_name)
    if not item or not isinstance(item, QgsLayoutItemLabel):
        return 0

    # Text, Font und Breite des Labels
    text = item.text()
    font = item.font()
    width_mm = item.sizeWithUnits().width()
    if not text.strip():
        return 0

    # Umrechnung mm - Pixel (96 dpi)
    width_px = width_mm * 96 / 25.4
    metrics = QFontMetricsF(font)

    lines = []

    # Text in Abschnitte trennen (Absatz = Zeilenumbruch)
    paragraphs = text.split('\n')

    for para in paragraphs:

        # harte Leerzeile - als echte Zeile zaehlen
        if para.strip() == "":
            lines.append(" ")
            continue

        words = para.split(" ")
        current_line = ""

        for word in words:
            test_line = word if current_line == "" else current_line + " " + word

            # boundingRect statt horizontalAdvance
            if metrics.boundingRect(test_line).width() > width_px:
                # alte Zeile abschliessen
                if current_line != "":
                    lines.append(current_line)
                current_line = word
            else:
                current_line = test_line

        if current_line != "":
            lines.append(current_line)

    # Gesamthoehe berechnen
    total_height_px = 0
    for line in lines:
        h = metrics.boundingRect(line).height()
        total_height_px += h * line_spacing

    # Sicherheitsabstand
    total_height_px *= 1.025

    # zurueck in mm
    height_mm = total_height_px * 25.4 / 96
    return height_mm


@qgsfunction(args="auto", group="Custom")
def CalcLabelWidth(layout_name, item_id, feature, parent):
    layout = QgsProject.instance().layoutManager().layoutByName(layout_name)
    if not layout:
        return 0

    item = layout.itemById(item_id)
    if not item or not isinstance(item, QgsLayoutItemLabel):
        return 0

    text = item.text()
    font = item.font()
    if not text.strip():
        return 0

    font_metrics = QFontMetricsF(font)
    # get max line width in pixels
    widths_px = [font_metrics.horizontalAdvance(line) for line in text.split("\n")]
    max_width_px = max(widths_px) if widths_px else 0

    # add 5% padding
    max_width_px *= 1.04

    # convert px back to mm (96 dpi assumption)
    width_mm = max_width_px * 25.4 / 96

    return width_mm


functions_to_load = (GetDynamicItemHeight, GetDynamicItemWidth, GetDynamicItemPositionX,
                     GetDynamicItemPositionY, GetPageSizeWidth, GetPageSizeHeight,
                     CalcLabelHeight, CalcLabelWidth)

def registerFunction(isRegister=True):
    '''Register functions to be able to use them in QGIS'''
    for f in functions_to_load:
        QgsExpression.registerFunction(f)    

registerFunction()
