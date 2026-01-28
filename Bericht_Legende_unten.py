### Variablen ###
# Seitengrößen
custom_page_size_width_blu = 169.03  # mm
#custom_page_size_height_blu = 160  # mm            DEAKTIVIERT: Ergibt sich dynamisch aus Kartenhöhe und Legende
custom_map_height_blu = 120.535  # mm               Höhe der Karte
# Abstände zur Seite
custom_page_dist_left_blu = 3
custom_page_dist_right_blu = 3
custom_page_dist_top_blu = 3
custom_page_dist_bottom_blu = 3
# Abstände von Elementen zum Rahmen
custom_item_dist_left_blu = 3
custom_item_dist_right_blu = 3
custom_item_dist_top_blu = 3
custom_item_dist_bottom_blu = 3
# Liniendicke des Rahmens
custom_frame_line_width_blu = 0.3
# Abstand zwischen Titel und Text
custom_dist_title_text_blu = 2
# Breite der Rahmen
custom_frame_width_blu = 40
# Größe Nordpfeil
custom_north_arrow_width_blu = 5
custom_north_arrow_height_blu = 8
# Größe Maßstab
custom_scale_width_blu = 35
custom_scale_height_blu = 9
# Font
font = "Calibri"
font_size = 10
font_size_title = 10
font_size_metadata = 7
# Legend Symbol
legend_symbol_width = 6
legend_symbol_height = 3
legend_symbol_spacing_left = 0.4
legend_symbol_spacing = 3
legend_symbol_label_spacing = 2
custom_legend_column_count = 1  #                   DEAKTIVIERT: Bitte Column Count in QGIS setzen
# scale bar
custom_scale_segment_length = 100  #                Länge der Segmente in der Bar in Metern
custom_scale_label_space_blu = 2
custom_scale_bar_height_blu = 2
# Pfade
svg_path_north_arrow = r"C:\PATH\TO\NorthArrow.svg"
svg_path_municipality_logo = r"PATH\TO\LOGO.svg"
jpg_path_endura_logo = r"PATH\TO\LOGO.svg"


#################################################################
### Custom Variablen für Print Layout setzen
QgsProject.instance().setCustomVariables(
    {
        "custom_page_dist_left_blu": str(custom_page_dist_left_blu),
        "custom_page_dist_right_blu": str(custom_page_dist_right_blu),
        "custom_page_dist_top_blu": str(custom_page_dist_top_blu),
        "custom_page_dist_bottom_blu": str(custom_page_dist_bottom_blu),
        "custom_item_dist_left_blu": str(custom_item_dist_left_blu),
        "custom_item_dist_right_blu": str(custom_item_dist_right_blu),
        "custom_item_dist_top_blu": str(custom_item_dist_top_blu),
        "custom_item_dist_bottom_blu": str(custom_item_dist_bottom_blu),
        "custom_frame_line_width_blu": str(custom_frame_line_width_blu),
        "custom_dist_title_text_blu": str(custom_dist_title_text_blu),
        "custom_frame_width_blu": str(custom_frame_width_blu),
        "custom_north_arrow_width_blu": str(custom_north_arrow_width_blu),
        "custom_north_arrow_height_blu": str(custom_north_arrow_height_blu),
        "custom_scale_width_blu": str(custom_scale_width_blu),
        "custom_scale_height_blu": str(custom_scale_height_blu),
        "custom_scale_label_space_blu": str(custom_scale_label_space_blu),
        "custom_scale_bar_height_blu": str(custom_scale_bar_height_blu),
        "custom_page_size_width_blu": str(custom_page_size_width_blu),
        #"custom_page_size_height_blu": str(custom_page_size_height_blu),
        "custom_map_height_blu": str(custom_map_height_blu),
    }
)

#################################################################

# Get the current QGIS project instance
project = QgsProject.instance()

# Access the layout manager
layout_manager = project.layoutManager()

# Define a name for the new layout
layout_name = "Bericht_Legende_unten"

# Check if a layout with that name already exists and remove it if so (optional)
existing_layout = layout_manager.layoutByName(layout_name)
if existing_layout:
    layout_manager.removeLayout(existing_layout)

# Create a new layout
new_layout = QgsPrintLayout(project)
new_layout.initializeDefaults()  # Sets page size, etc.

# Set the layout name
new_layout.setName(layout_name)

# Add the layout to the project
layout_manager.addLayout(new_layout)

print(f"New layout '{layout_name}' has been added.")

page = new_layout.pageCollection().page(0)
page.dataDefinedProperties().setProperty(
    QgsLayoutItemPage.ItemWidth, QgsProperty.fromExpression(
        "@custom_page_size_width_blu"
    )
)
page.dataDefinedProperties().setProperty(
    QgsLayoutItemPage.ItemHeight, QgsProperty.fromExpression(
        "@custom_map_height_blu + GetDynamicItemHeight(@layout_name, 'legend_frame') + @custom_frame_line_width_blu"
    )
)

########################################################################

### Map ###
map = QgsLayoutItemMap(new_layout)
map.setId("map")
map.setFrameEnabled(True)
map.setFrameStrokeWidth(QgsLayoutMeasurement(custom_frame_line_width_blu))
map.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX, QgsProperty.fromExpression("@custom_frame_line_width_blu/2")
)
map.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY, QgsProperty.fromExpression("@custom_frame_line_width_blu/2")
)
map.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression("@custom_page_size_width_blu - (@custom_frame_line_width_blu)"),
)
map.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression(
        "@custom_map_height_blu"
    ),
)

canvas_extent = iface.mapCanvas().extent()
map.setExtent(canvas_extent)

new_layout.addLayoutItem(map)


### Legend Frame ###

legend_frame = QgsLayoutItemShape(new_layout)
legend_frame.setShapeType(QgsLayoutItemShape.Rectangle)
legend_frame.setId("legend_frame")
legend_frame.setFrameEnabled(True)
legend_frame.setFrameStrokeWidth(QgsLayoutMeasurement(custom_frame_line_width_blu))
legend_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX, QgsProperty.fromExpression("@custom_frame_line_width_blu/2")
)
legend_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetPageSizeHeight(@layout_name) -"
        "GetDynamicItemHeight(@layout_name, 'plan_content_frame') -"
        "GetDynamicItemHeight(@layout_name, 'metadata_frame') -"
        "@custom_frame_line_width_blu/2"
    ),
)
legend_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "@custom_page_size_width_blu - @custom_frame_width_blu - @custom_frame_line_width_blu"
    ),
)
# expr_legend_frame_height = "@custom_page_size_height_blu - @custom_map_height_blu"
expr_legend_frame_height = "GetDynamicItemHeight(@layout_name, 'metadata_frame') + GetDynamicItemHeight(@layout_name, 'plan_content_frame')"
legend_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight, QgsProperty.fromExpression(expr_legend_frame_height)
)

new_layout.addLayoutItem(legend_frame)


### Legend Title ###

legend_title = QgsLayoutItemLabel(new_layout)
legend_title.setText("Legende")
legend_title.setId("legend_title")
legend_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name ,'legend_frame') +"
        "(to_real(@custom_frame_line_width_blu)/2) +"
        "to_real(@custom_item_dist_left_blu)"
    ),
)
legend_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name ,'legend_frame') + "
        "@custom_frame_line_width_blu/2 + "
        "@custom_item_dist_top_blu"
    ),
)
legend_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "@custom_page_size_width_blu - @custom_frame_width_blu -"
        "2*to_real(@custom_frame_line_width_blu) - "
        "to_real(@custom_item_dist_right_blu) - "
        "to_real(@custom_item_dist_left_blu)"
    ),
)
legend_title.setFont(QFont(font, font_size_title, QFont.Bold))
legend_title.setMargin(0)
legend_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression("CalcLabelHeight(@layout_name, 'legend_title')"),
)

new_layout.addLayoutItem(legend_title)


### Legend ###

legend = QgsLayoutItemLegend(new_layout)
legend.setId("legend")
legend.setAutoUpdateModel(False)
legend.model().rootGroup().removeAllChildren()
legend.setResizeToContents(True)
legend.setLinkedMap(map)
legend.setWrapString('//')

legend.setStyleFont(QgsLegendStyle.Group, QFont(font, font_size))
legend.setStyleFont(QgsLegendStyle.Subgroup, QFont(font, font_size))
legend.setStyleFont(QgsLegendStyle.SymbolLabel, QFont(font, font_size))

legend.setSymbolWidth(legend_symbol_width)
legend.setSymbolHeight(legend_symbol_height)

# Hier wurde die Anzahl der Spalten an der gewünschten Spaltenbreite ermittelt. Bringt aber erst etwas, wenn man den automatischen Zeilenumbruch aktivieren kann, ab QGIS 3.44
# if custom_legend_column_count is not None:
#     no_of_cols = custom_legend_column_count
# else:
#     # Calculate the number of columns based on the width of the legend frame and frame width
#     no_of_cols = int((custom_page_size_width_blu - custom_frame_width_blu - custom_item_dist_right_blu) // (custom_frame_width_blu + custom_item_dist_left_blu))
legend.setColumnCount(custom_legend_column_count)
legend.setEqualColumnWidth(True)
legend.setSplitLayer(True)
legend.setWrapString("//")

styles = [
    QgsLegendStyle.Title,
    QgsLegendStyle.Group,
    QgsLegendStyle.Subgroup,
]

for style in styles:
    legend.rstyle(style).setMargin(0)

legend.setBoxSpace(0)
legend.setColumnSpace(custom_item_dist_left_blu)

legend.rstyle(QgsLegendStyle.Symbol).setMargin(
    QgsLegendStyle.Left, legend_symbol_spacing_left
)
legend.rstyle(QgsLegendStyle.Symbol).setMargin(
    QgsLegendStyle.Top, legend_symbol_spacing
)
legend.rstyle(QgsLegendStyle.SymbolLabel).setMargin(legend_symbol_label_spacing)

expr_legend_posX = "GetDynamicItemPositionX(@layout_name ,'legend_frame') + (to_real(@custom_frame_line_width_blu)/2) + to_real(@custom_item_dist_left_blu)"
legend.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX, QgsProperty.fromExpression(expr_legend_posX)
)

expr_legend_posY = (
    "GetDynamicItemPositionY(@layout_name ,'legend_frame') + "
    "to_real(@custom_frame_line_width_blu)/2 + "
    "to_real(@custom_item_dist_top_blu) + "
    "GetDynamicItemHeight(@layout_name,'legend_title') + "
    "to_real(@custom_dist_title_text_blu)"
)
legend.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY, QgsProperty.fromExpression(expr_legend_posY)
)

expr_legend_width = (
    "@custom_page_size_width_blu - @custom_frame_width_blu -"
    "2*to_real(@custom_frame_line_width_blu) - "
    "to_real(@custom_item_dist_right_blu) - "
    "to_real(@custom_item_dist_left_blu)"
)
legend.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression(expr_legend_width)
)

expr_legend_height = (
    "GetDynamicItemHeight(@layout_name,'legend_frame') -"
    "to_real(@custom_item_dist_top_blu) - "
    "to_real(@custom_frame_line_width_blu) - "
    "GetDynamicItemHeight(@layout_name,'legend_title') -"
    "to_real(@custom_dist_title_text_blu) -"
    "@custom_item_dist_bottom_blu"
)

legend.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight, QgsProperty.fromExpression(expr_legend_height)
)

# legend.dataDefinedProperties().setProperty(  # erst in V 3.44
#     QgsLegendSettings.autoWrapLinesAfter,
#     QgsProperty.fromExpression(expr_legend_width))


new_layout.addLayoutItem(legend)


### column width indicator ###
# Das ist ein Textfeld der Spaltenbreite, was den manuellen Zeilenumbruch erleichtern soll

column_width_indicator = QgsLayoutItemLabel(new_layout)
column_width_indicator.setText("Breite Legendenspalte plus Abstand. DEAKTIVIEREN")
column_width_indicator.setId("column_width_indicator")
column_width_indicator.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name ,'legend_frame') + (to_real(@custom_frame_line_width_blu)/2) + to_real(@custom_item_dist_left_blu)"
    ),
)
column_width_indicator.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name ,'legend_frame') + "
        "to_real(@custom_frame_line_width_blu)/2 + "
        "to_real(@custom_item_dist_top_blu) + "
        "GetDynamicItemHeight(@layout_name,'legend_title')"
    ),
)
column_width_indicator.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression("@custom_frame_width_blu + to_real(@custom_item_dist_left_blu)"),
)
column_width_indicator.setFont(QFont(font, 4))
column_width_indicator.setMargin(0)
column_width_indicator.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression("to_real(@custom_dist_title_text_blu)"),
)
column_width_indicator.setFontColor(QColor(255, 255, 255))
column_width_indicator.setBackgroundEnabled(True)
column_width_indicator.setBackgroundColor(QColor(0, 0, 0))

new_layout.addLayoutItem(column_width_indicator)


### plan content frame###
plan_content_frame = QgsLayoutItemShape(new_layout)
plan_content_frame.setShapeType(QgsLayoutItemShape.Rectangle)
plan_content_frame.setId("plan_content_frame")
plan_content_frame.setFrameEnabled(True)
plan_content_frame.setFrameStrokeWidth(QgsLayoutMeasurement(custom_frame_line_width_blu))
plan_content_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name ,'metadata_frame')"
    ),
)
plan_content_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name,'metadata_frame') - "
        "GetDynamicItemHeight(@layout_name,'plan_content_frame')"
    ),
)
plan_content_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("@custom_frame_width_blu")
)
expr_plan_content_frame_height = (
    "to_real(@custom_frame_line_width_blu) +"
    "to_real(@custom_item_dist_top_blu) + "
    "GetDynamicItemHeight(@layout_name,'plan_content_title') + "
    "to_real(@custom_dist_title_text_blu) + "
    "GetDynamicItemHeight(@layout_name,'plan_content') + "
    "to_real(@custom_item_dist_bottom_blu)"
)
plan_content_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression(expr_plan_content_frame_height),
)

new_layout.addLayoutItem(plan_content_frame)


### plan content title ###
plan_content_title = QgsLayoutItemLabel(new_layout)
plan_content_title.setText("Planinhalt")
plan_content_title.setId("plan_content_title")
plan_content_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name ,'plan_content_frame') + (to_real(@custom_frame_line_width_blu)/2) + to_real(@custom_item_dist_left_blu)"
    ),
)
plan_content_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name ,'plan_content_frame') + "
        "@custom_frame_line_width_blu/2 + "
        "@custom_item_dist_top_blu"
    ),
)
plan_content_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_width_blu) - "
        "2*to_real(@custom_frame_line_width_blu) - "
        "to_real(@custom_item_dist_right_blu) - "
        "to_real(@custom_item_dist_left_blu)"
    ),
)
plan_content_title.setFont(QFont(font, font_size_title, QFont.Bold))
plan_content_title.setMargin(0)
plan_content_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression("CalcLabelHeight(@layout_name, 'plan_content_title')"),
)

new_layout.addLayoutItem(plan_content_title)


### plan content ###
plan_content = QgsLayoutItemLabel(new_layout)
plan_content.setText("XXX")
plan_content.setId("plan_content")
plan_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name ,'plan_content_frame') + (to_real(@custom_frame_line_width_blu)/2) + to_real(@custom_item_dist_left_blu)"
    ),
)
plan_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY( @layout_name, 'plan_content_title') + "
        "GetDynamicItemHeight(@layout_name,'plan_content_title') + "
        "to_real(@custom_dist_title_text_blu)"
    ),
)
plan_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_width_blu) - "
        "2*to_real(@custom_frame_line_width_blu) - "
        "to_real(@custom_item_dist_right_blu) - "
        "to_real(@custom_item_dist_left_blu)"
    ),
)
plan_content.setFont(QFont(font, font_size))
plan_content.setMargin(0)
plan_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression("CalcLabelHeight(@layout_name, 'plan_content')"),
)

new_layout.addLayoutItem(plan_content)


### metadata_frame ###
metadata_frame = QgsLayoutItemShape(new_layout)
metadata_frame.setShapeType(QgsLayoutItemShape.Rectangle)
metadata_frame.setId("metadata_frame")
metadata_frame.setFrameEnabled(True)
metadata_frame.setFrameStrokeWidth(QgsLayoutMeasurement(custom_frame_line_width_blu))
metadata_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "@custom_page_size_width_blu - @custom_frame_width_blu - @custom_frame_line_width_blu/2"
    ),
)
metadata_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetPageSizeHeight(@layout_name) - "
        "GetDynamicItemHeight(@layout_name, 'metadata_frame') - "
        "@custom_frame_line_width_blu/2"
    ),
)
metadata_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("@custom_frame_width_blu")
)
expr_metadata_frame_height = (
    "to_real(@custom_frame_line_width_blu) +"
    "to_real(@custom_item_dist_top_blu) + "
    "GetDynamicItemHeight(@layout_name,'metadata') + "
    "to_real(@custom_item_dist_bottom_blu)"
)
metadata_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight, QgsProperty.fromExpression(expr_metadata_frame_height)
)

new_layout.addLayoutItem(metadata_frame)

### Metadata ###
metadata = QgsLayoutItemLabel(new_layout)
metadata.setText(
    "Datengrundlage: \n"
    + "© XXX \n"
    + "Hintergrundkarte: \n"
    + "© XXX \n"
    + "Sonstige Karteninhalte: \n"
    + "eigene Darstellung"
)
metadata.setFont(QFont(font, font_size_metadata))
metadata.setMargin(0)
metadata.setId("metadata")
metadata.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name ,'metadata_frame') + @custom_frame_line_width_blu/2 + @custom_item_dist_left_blu"
    ),
)
metadata.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name ,'metadata_frame') + "
        "@custom_frame_line_width_blu/2 + "
        "@custom_item_dist_top_blu"
    ),
)
metadata.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_width_blu) - "
        "2*to_real(@custom_frame_line_width_blu) - "
        "to_real(@custom_item_dist_right_blu) - "
        "to_real(@custom_item_dist_left_blu)"
    ),
)
metadata.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression("CalcLabelHeight(@layout_name, 'metadata')"),
)

new_layout.addLayoutItem(metadata)


### North Arrow ###
north_arrow = QgsLayoutItemPicture(new_layout)
north_arrow.setId("north_arrow")
north_arrow.setFrameEnabled(False)

north_arrow.setPicturePath(svg_path_north_arrow)

north_arrow.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "(to_real(@custom_frame_line_width_blu)) + to_real(@custom_item_dist_left_blu)"
    ),
)
north_arrow.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_line_width_blu) + to_real(@custom_item_dist_top_blu)"
    ),
)
north_arrow.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("@custom_north_arrow_width_blu")
)
north_arrow.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight, QgsProperty.fromExpression("@custom_north_arrow_height_blu")
)
north_arrow.setLinkedMap(map)
north_arrow.setNorthMode(0)  # 0 for grid north, 1 for true north

new_layout.addLayoutItem(north_arrow)


### Scale Bar ###
scale_bar = QgsLayoutItemScaleBar(new_layout)
scale_bar.setId("scale_bar")
scale_bar.setFrameEnabled(False)

scale_bar.setStyle("Single Box")
scale_bar.setBoxContentSpace(0)
scale_bar.setFont(QFont(font, font_size_metadata))
scale_bar.setLabelBarSpace(custom_scale_label_space_blu)
scale_bar.setLinkedMap(map)
scale_bar.setHeight(custom_scale_bar_height_blu)


scale_bar.setReferencePoint(QgsLayoutItem.LowerLeft)

scale_bar.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_line_width_blu) + to_real(@custom_item_dist_left_blu) - 0.4"
    ),
)
scale_bar.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemHeight(@layout_name, 'map') + to_real(@custom_frame_line_width_blu)/2 - to_real(@custom_item_dist_bottom_blu) + 0.525"
    ),
)
scale_bar.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression(
        f"to_real(@custom_scale_bar_height_blu) + to_real(@custom_scale_label_space_blu) + {int(font_size_metadata)}*0.352778"
    ),
)

scale_bar.setSegmentSizeMode(Qgis.ScaleBarSegmentSizeMode.Fixed)
scale_bar.setUnits(QgsUnitTypes.DistanceMeters)  # Set the units to meters
scale_bar.setMapUnitsPerScaleBarUnit(1)
scale_bar.setUnitsPerSegment(custom_scale_segment_length)
scale_bar.setNumberOfSegments(2)
scale_bar.setNumberOfSegmentsLeft(0)
scale_bar.setUnitLabel("m")

new_layout.addLayoutItem(scale_bar)


### Auftragsbox ###
municipality_box = QgsLayoutItemShape(new_layout)
municipality_box.setShapeType(QgsLayoutItemShape.Rectangle)
municipality_box.setId("municipality_box")
municipality_box.setBackgroundEnabled(False)
municipality_box.setSymbol(
    QgsFillSymbol.createSimple(
        {
            "color": "255, 255, 255, 155",
            "outline_color": "0, 0, 0, 0",
            "outline_width": str(custom_frame_line_width_blu),
        }
    )
)
municipality_box.setFrameEnabled(False)

municipality_box.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "@custom_page_size_width_blu - GetDynamicItemWidth(@layout_name, 'municipality_box') - @custom_frame_line_width_blu"
    ),
)
municipality_box.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY, QgsProperty.fromExpression("@custom_frame_line_width_blu/2")
)
municipality_box.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression("GetDynamicItemWidth(@layout_name, 'municipality_logo') + GetDynamicItemWidth(@layout_name, 'municipality_label') + @custom_frame_line_width_blu + (@custom_item_dist_left_blu * 2) + @custom_item_dist_right_blu"),
)
expr_municipality_box_height = "@custom_frame_line_width_blu / 2 + if(GetDynamicItemHeight(@layout_name, 'municipality_logo') > GetDynamicItemHeight(@layout_name, 'municipality_label'), GetDynamicItemHeight(@layout_name, 'municipality_logo'), GetDynamicItemHeight(@layout_name, 'municipality_label')) + @custom_item_dist_top_blu + @custom_item_dist_bottom_blu"
municipality_box.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight, QgsProperty.fromExpression(expr_municipality_box_height)
)

new_layout.addLayoutItem(municipality_box)

### Municipality Logo ###
municipality_logo = QgsLayoutItemPicture(new_layout)
municipality_logo.setId("municipality_logo")
municipality_logo.setFrameEnabled(False)

municipality_logo.setPicturePath(svg_path_municipality_logo)

municipality_logo.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name, 'municipality_box') + (to_real(@custom_frame_line_width_blu)/2) + to_real(@custom_item_dist_left_blu)"
    ),
)
municipality_logo.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name, 'municipality_box') + @custom_frame_line_width_blu/2 + @custom_item_dist_top_blu"
    ),
)
municipality_logo.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("9.5")
)
municipality_logo.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight, QgsProperty.fromExpression("10.256")
)

new_layout.addLayoutItem(municipality_logo)


### Municipality Label ###
municipality_label = QgsLayoutItemLabel(new_layout)
municipality_label.setId("municipality_label")
municipality_label.setFrameEnabled(False)
municipality_label.setText("Gemeinde/Stadt\nXX")
municipality_label.setFont(QFont(font, font_size))
municipality_label.setMargin(0)

municipality_label.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name, 'municipality_logo') + to_real(@custom_item_dist_left_blu) + GetDynamicItemWidth(@layout_name, 'municipality_logo')"
    ),
)
municipality_label.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name, 'municipality_box') + @custom_frame_line_width_blu/2 + @custom_item_dist_top_blu"
    ),
)
municipality_label.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "CalcLabelWidth(@layout_name, 'municipality_label')"
    ),
)
municipality_label.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression("CalcLabelHeight(@layout_name, 'municipality_label')"),
)

new_layout.addLayoutItem(municipality_label)
