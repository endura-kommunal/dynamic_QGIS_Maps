'''
Place this Script in 'AppData\Roaming\QGIS\QGIS3' to have the functions available on startup.
'''

from PyQt5.QtGui import QFont, QFontMetricsF
from qgis.core import *
from qgis.gui import *
from qgis.utils import qgsfunction


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
    Berechnet die benötigte Höhe eines QgsLayoutItemLabel.

    Berücksichtigt:
    - harte Zeilenumbrüche
    - automatischen Zeilenumbruch
    - Data-Defined-Schriftgröße aus QgsTextFormat
    - Projekt-, Layout- und Layout-Item-Variablen
    """

    project = QgsProject.instance()
    manager = project.layoutManager()
    layout = manager.layoutByName(str(layout_name))

    if not layout:
        return 0.0

    item = layout.itemById(str(item_name))

    if not isinstance(item, QgsLayoutItemLabel):
        return 0.0

    text = item.text()

    if not text or not text.strip():
        return 0.0

    width_mm = item.sizeWithUnits().width()

    if width_mm <= 0:
        return 0.0

    # ---------------------------------------------------------
    # Eigenen featurefreien Expression-Kontext erstellen
    # ---------------------------------------------------------

    context = QgsExpressionContext()

    context.appendScope(
        QgsExpressionContextUtils.globalScope()
    )

    context.appendScope(
        QgsExpressionContextUtils.projectScope(project)
    )

    context.appendScope(
        QgsExpressionContextUtils.layoutScope(layout)
    )

    context.appendScope(
        QgsExpressionContextUtils.layoutItemScope(item)
    )

    # ---------------------------------------------------------
    # Textformat und Basis-Font auslesen
    # ---------------------------------------------------------

    text_format = item.textFormat()
    font = text_format.font()

    base_size = text_format.size()

    if base_size <= 0:
        base_size = font.pointSizeF()

    if base_size <= 0:
        base_size = 10.0

    evaluated_size = float(base_size)

    # ---------------------------------------------------------
    # Data-Defined-Schriftgröße auswerten
    # ---------------------------------------------------------

    properties = text_format.dataDefinedProperties()

    size_property = properties.property(
        QgsPalLayerSettings.Size
    )

    if size_property.isActive():

        # Expression selbst auslesen, z. B.:
        # @font_size_vq
        size_expression_string = size_property.expressionString()

        if size_expression_string:

            size_expression = QgsExpression(
                size_expression_string
            )

            value = size_expression.evaluate(context)

            if (
                not size_expression.hasParserError()
                and not size_expression.hasEvalError()
                and value is not None
            ):
                try:
                    numeric_value = float(value)

                    if numeric_value > 0:
                        evaluated_size = numeric_value

                except (TypeError, ValueError):
                    pass

        else:
            # Falls die Property einen statischen Wert enthält
            static_value = size_property.staticValue()

            try:
                numeric_value = float(static_value)

                if numeric_value > 0:
                    evaluated_size = numeric_value

            except (TypeError, ValueError):
                pass

    # Die tatsächlich ausgewertete Größe auf den Font übertragen
    font.setPointSizeF(evaluated_size)

    # ---------------------------------------------------------
    # Maße berechnen
    # ---------------------------------------------------------

    width_px = width_mm * 96.0 / 25.4
    metrics = QFontMetricsF(font)

    lines = []
    paragraphs = text.split("\n")

    for paragraph in paragraphs:

        # Explizite Leerzeile
        if paragraph.strip() == "":
            lines.append(" ")
            continue

        words = paragraph.split(" ")
        current_line = ""

        for word in words:
            if current_line:
                test_line = current_line + " " + word
            else:
                test_line = word

            test_width = metrics.horizontalAdvance(test_line)

            if test_width > width_px:

                if current_line:
                    lines.append(current_line)
                current_line = word

            else:
                current_line = test_line

        if current_line:
            lines.append(current_line)

    # ---------------------------------------------------------
    # Höhe aller Zeilen berechnen
    # ---------------------------------------------------------

    total_height_px = 0.0

    for line in lines:
        line_height_px = metrics.lineSpacing()

        total_height_px += (
            line_height_px * line_spacing
        )

    height_mm = total_height_px * 25.4 / 96.0

    return float(height_mm)


@qgsfunction(args="auto", group="Custom")
def CalcLabelWidth(layout_name, item_id, feature, parent):
    """
    Berechnet die benötigte Breite eines QgsLayoutItemLabel.

    Berücksichtigt:
    - harte Zeilenumbrüche
    - Data-Defined-Schriftgröße aus QgsTextFormat
    - Projekt-, Layout- und Layout-Item-Variablen
    """

    project = QgsProject.instance()
    manager = project.layoutManager()
    layout = manager.layoutByName(str(layout_name))

    if not layout:
        return 0.0

    item = layout.itemById(str(item_id))

    if not isinstance(item, QgsLayoutItemLabel):
        return 0.0

    text = item.text()

    if not text or not text.strip():
        return 0.0

    # ---------------------------------------------------------
    # Eigenen featurefreien Expression-Kontext erstellen
    # ---------------------------------------------------------

    context = QgsExpressionContext()

    context.appendScope(
        QgsExpressionContextUtils.globalScope()
    )

    context.appendScope(
        QgsExpressionContextUtils.projectScope(project)
    )

    context.appendScope(
        QgsExpressionContextUtils.layoutScope(layout)
    )

    context.appendScope(
        QgsExpressionContextUtils.layoutItemScope(item)
    )

    # ---------------------------------------------------------
    # Textformat und Basis-Font auslesen
    # ---------------------------------------------------------

    text_format = item.textFormat()
    font = text_format.font()

    base_size = text_format.size()

    if base_size <= 0:
        base_size = font.pointSizeF()

    if base_size <= 0:
        base_size = 10.0

    evaluated_size = float(base_size)

    # ---------------------------------------------------------
    # Data-Defined-Schriftgröße auswerten
    # ---------------------------------------------------------

    properties = text_format.dataDefinedProperties()

    size_property = properties.property(
        QgsPalLayerSettings.Size
    )

    if size_property.isActive():

        # Expression auslesen, beispielsweise:
        # @custom_font_size_blu
        size_expression_string = size_property.expressionString()

        if size_expression_string:

            size_expression = QgsExpression(
                size_expression_string
            )

            value = size_expression.evaluate(context)

            if (
                not size_expression.hasParserError()
                and not size_expression.hasEvalError()
                and value is not None
            ):
                try:
                    numeric_value = float(value)

                    if numeric_value > 0:
                        evaluated_size = numeric_value

                except (TypeError, ValueError):
                    pass

        else:
            # Falls die Property einen statischen Wert enthält
            static_value = size_property.staticValue()

            try:
                numeric_value = float(static_value)

                if numeric_value > 0:
                    evaluated_size = numeric_value

            except (TypeError, ValueError):
                pass

    # Tatsächlich ausgewertete Schriftgröße übernehmen
    font.setPointSizeF(evaluated_size)

    # ---------------------------------------------------------
    # Breite berechnen
    # ---------------------------------------------------------

    font_metrics = QFontMetricsF(font)

    widths_px = [
        font_metrics.horizontalAdvance(line)
        for line in text.split("\n")
    ]

    max_width_px = max(widths_px) if widths_px else 0.0

    # add 5% padding 
    max_width_px *= 1.04

    # convert px back to mm (96 dpi assumption)
    width_mm = max_width_px * 25.4 / 96.0

    return float(width_mm)


# ##########################################################
# Register functions to be able to use them in QGIS
# ##########################################################
functions_to_load = (GetDynamicItemHeight, GetDynamicItemWidth, GetDynamicItemPositionX,
                     GetDynamicItemPositionY, GetPageSizeWidth, GetPageSizeHeight,
                     CalcLabelHeight, CalcLabelWidth)

def registerFunction(isRegister=True):
    '''Register functions to be able to use them in QGIS'''
    for f in functions_to_load:
        QgsExpression.registerFunction(f)    

registerFunction()


# ##########################################################
# Add helper functions for layout creation
# ##########################################################
def create_text_format(
    font_family,
    variable_name,
    bold=False
):
    """
    # Add helper functions for layout creation
    """
    # Properties that can be set: listed in API Doku section Property of 'Class: QgsPalLayerSettings'
    fmt = QgsTextFormat()

    fmt.setFont(
        QFont(
            font_family,
            -1,
            QFont.Bold if bold else QFont.Normal
        )
    )

    fmt.dataDefinedProperties().setProperty(
        QgsPalLayerSettings.Size,
        QgsProperty.fromExpression(
            f"@{variable_name}"
        )
    )

    return fmt
