### Variablen ###
# Seitengrößen
custom_page_size_width_vq = 297  # mm
custom_page_size_height_vq = 210  # mm
# Abstände zur Seite
custom_page_dist_left_vq = 3
custom_page_dist_right_vq = 3
custom_page_dist_top_vq = 3
custom_page_dist_bottom_vq = 3
# Abstände von Elementen zum Rahmen
custom_item_dist_left_vq = 3
custom_item_dist_right_vq = 3
custom_item_dist_top_vq = 3
custom_item_dist_bottom_vq = 3
# Liniendicke des Rahmens
custom_frame_line_width_vq = 0.3
# Abstand zwischen Titel und Text
custom_dist_title_text_vq = 2
# Breite der Rahmen
custom_frame_width_vq = 60
# Größe Nordpfeil
custom_north_arrow_width_vq = 9
custom_north_arrow_height_vq = 15
# Größe Maßstab
custom_scale_width_vq = 35
custom_scale_height_vq = 9
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
custom_scale_segment_length = 100  # Länge der Segmente in der Bar in Metern
custom_scale_label_space_vq = 2
custom_scale_bar_height_vq = 2
# Pfade
svg_path_north_arrow = r"C:\PATH\TO\NorthArrow.svg"
svg_path_municipality_logo = r"PATH\TO\LOGO.svg"
jpg_path_endura_logo = r"PATH\TO\LOGO.svg"


#################################################################
### Custom Variablen für Print Layout setzen
QgsProject.instance().setCustomVariables(
    {
        "custom_page_dist_left_vq": str(custom_page_dist_left_vq),
        "custom_page_dist_right_vq": str(custom_page_dist_right_vq),
        "custom_page_dist_top_vq": str(custom_page_dist_top_vq),
        "custom_page_dist_bottom_vq": str(custom_page_dist_bottom_vq),
        "custom_item_dist_left_vq": str(custom_item_dist_left_vq),
        "custom_item_dist_right_vq": str(custom_item_dist_right_vq),
        "custom_item_dist_top_vq": str(custom_item_dist_top_vq),
        "custom_item_dist_bottom_vq": str(custom_item_dist_bottom_vq),
        "custom_frame_line_width_vq": str(custom_frame_line_width_vq),
        "custom_dist_title_text_vq": str(custom_dist_title_text_vq),
        "custom_frame_width_vq": str(custom_frame_width_vq),
        "custom_north_arrow_width_vq": str(custom_north_arrow_width_vq),
        "custom_north_arrow_height_vq": str(custom_north_arrow_height_vq),
        "custom_scale_width_vq": str(custom_scale_width_vq),
        "custom_scale_height_vq": str(custom_scale_height_vq),
        "custom_scale_label_space_vq": str(custom_scale_label_space_vq),
        "custom_scale_bar_height_vq": str(custom_scale_bar_height_vq),
        "custom_page_size_width_vq": str(custom_page_size_width_vq),
        "custom_page_size_height_vq": str(custom_page_size_height_vq),
    }
)

#################################################################

# Get the current QGIS project instance
project = QgsProject.instance()

# Access the layout manager
layout_manager = project.layoutManager()

# Define a name for the new layout
layout_name = "Vollbildkarte_quer"

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
        "@custom_page_size_width_vq"
    )
)
page.dataDefinedProperties().setProperty(
    QgsLayoutItemPage.ItemHeight, QgsProperty.fromExpression(
        "@custom_page_size_height_vq"
    )
)

########################################################################

map = QgsLayoutItemMap(new_layout)
map.setId("map")
map.setFrameEnabled(True)
map.setFrameStrokeWidth(QgsLayoutMeasurement(custom_frame_line_width_vq))
map.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression("@custom_frame_line_width_vq/2 + @custom_page_dist_left_vq"),
)
map.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression("@custom_frame_line_width_vq/2 + @custom_page_dist_top_vq"),
)
map.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "(GetDynamicItemPositionX(@layout_name, 'legend_frame') - @custom_page_dist_left_vq - @custom_frame_line_width_vq) - GetDynamicItemPositionX(@layout_name, 'map')"
    ),
)
map.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression(
        "@custom_page_size_height_vq - @custom_frame_line_width_vq - @custom_page_dist_top_vq - @custom_page_dist_bottom_vq"
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
legend_frame.setFrameStrokeWidth(QgsLayoutMeasurement(custom_frame_line_width_vq))
legend_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "@custom_page_size_width_vq - @custom_page_dist_left_vq - @custom_frame_width_vq - @custom_frame_line_width_vq"
    ),
)
legend_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression("@custom_frame_line_width_vq/2 + @custom_page_dist_top_vq"),
)
legend_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("@custom_frame_width_vq")
)
expr_legend_frame_height = (
    "GetDynamicItemPositionY(@layout_name, 'municipality_frame') - "
    "GetDynamicItemPositionY(@layout_name, 'legend_frame')"
)
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
        "GetDynamicItemPositionX(  @layout_name ,'legend_frame') + (to_real(@custom_frame_line_width_vq)/2) + to_real(@custom_item_dist_left_vq)"
    ),
)
legend_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(  @layout_name ,'legend_frame') + "
        "@custom_frame_line_width_vq/2 + "
        "@custom_item_dist_top_vq"
    ),
)
legend_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_width_vq) - "
        "2*to_real(@custom_frame_line_width_vq) - "
        "to_real(@custom_item_dist_right_vq) - "
        "to_real(@custom_item_dist_left_vq)"
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
legend.setWrapString("//")

legend.setStyleFont(QgsLegendStyle.Group, QFont(font, font_size))
legend.setStyleFont(QgsLegendStyle.Subgroup, QFont(font, font_size))
legend.setStyleFont(QgsLegendStyle.SymbolLabel, QFont(font, font_size))

legend.setSymbolWidth(legend_symbol_width)
legend.setSymbolHeight(legend_symbol_height)

legend.setColumnCount(custom_legend_column_count)
legend.setEqualColumnWidth(True)
legend.setSplitLayer(True)

styles = [
    QgsLegendStyle.Title,
    QgsLegendStyle.Group,
    QgsLegendStyle.Subgroup,
]

for style in styles:
    legend.rstyle(style).setMargin(0)

legend.setBoxSpace(0)
legend.setColumnSpace(0)

legend.rstyle(QgsLegendStyle.Symbol).setMargin(
    QgsLegendStyle.Left, legend_symbol_spacing_left
)
legend.rstyle(QgsLegendStyle.Symbol).setMargin(
    QgsLegendStyle.Top, legend_symbol_spacing
)
legend.rstyle(QgsLegendStyle.SymbolLabel).setMargin(legend_symbol_label_spacing)

expr_legend_posX = "GetDynamicItemPositionX(  @layout_name ,'legend_frame') + (to_real(@custom_frame_line_width_vq)/2) + to_real(@custom_item_dist_left_vq)"
legend.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX, QgsProperty.fromExpression(expr_legend_posX)
)

expr_legend_posY = (
    "GetDynamicItemPositionY(  @layout_name ,'legend_frame') + "
    "to_real(@custom_frame_line_width_vq)/2 + "
    "to_real(@custom_item_dist_top_vq) + "
    "GetDynamicItemHeight(@layout_name,'legend_title') + "
    "to_real(@custom_dist_title_text_vq)"
)
legend.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY, QgsProperty.fromExpression(expr_legend_posY)
)

expr_legend_width = (
    "to_real(@custom_frame_width_vq) - "
    "2 *to_real(@custom_frame_line_width_vq) - "
    "to_real(@custom_item_dist_right_vq) - "
    "to_real(@custom_item_dist_left_vq)"
)
legend.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression(expr_legend_width)
)

# legend.dataDefinedProperties().setProperty(  # erst in V 3.44
#     QgsLegendSettings.autoWrapLinesAfter,
#     QgsProperty.fromExpression(expr_legend_width))


new_layout.addLayoutItem(legend)


### project frame###
project_frame = QgsLayoutItemShape(new_layout)
project_frame.setShapeType(QgsLayoutItemShape.Rectangle)
project_frame.setId("project_frame")
project_frame.setFrameEnabled(True)
project_frame.setFrameStrokeWidth(QgsLayoutMeasurement(custom_frame_line_width_vq))
project_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression("GetDynamicItemPositionX(@layout_name ,'legend_frame')"),
)
project_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name,'plan_content_frame') - "
        "GetDynamicItemHeight(@layout_name,'project_frame')"
    ),
)
project_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("@custom_frame_width_vq")
)
expr_project_frame_height = (
    "to_real(@custom_frame_line_width_vq) +"
    "to_real(@custom_item_dist_top_vq) + "
    "GetDynamicItemHeight(@layout_name,'project_title') + "
    "to_real(@custom_dist_title_text_vq) + "
    "GetDynamicItemHeight(@layout_name,'project_content') + "
    "to_real(@custom_item_dist_bottom_vq)"
)
project_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression(expr_project_frame_height),
)

new_layout.addLayoutItem(project_frame)


### project title ###
project_title = QgsLayoutItemLabel(new_layout)
project_title.setText("Projekt")
project_title.setId("project_title")
project_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(  @layout_name ,'project_frame') + (to_real(@custom_frame_line_width_vq)/2) + to_real(@custom_item_dist_left_vq)"
    ),
)
project_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(  @layout_name ,'project_frame') + "
        "@custom_frame_line_width_vq/2 + "
        "@custom_item_dist_top_vq"
    ),
)
project_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_width_vq) - "
        "2*to_real(@custom_frame_line_width_vq) - "
        "to_real(@custom_item_dist_right_vq) - "
        "to_real(@custom_item_dist_left_vq)"
    ),
)
project_title.setFont(QFont(font, font_size_title, QFont.Bold))
project_title.setMargin(0)
project_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression("CalcLabelHeight(@layout_name, 'project_title')"),
)

new_layout.addLayoutItem(project_title)


### plan content ###
project_content = QgsLayoutItemLabel(new_layout)
project_content.setText("XXX")
project_content.setId("project_content")
project_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(  @layout_name ,'project_frame') + (to_real(@custom_frame_line_width_vq)/2) + to_real(@custom_item_dist_left_vq)"
    ),
)
project_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY( @layout_name, 'project_title') + "
        "GetDynamicItemHeight(@layout_name,'project_title') + "
        "to_real(@custom_dist_title_text_vq)"
    ),
)
project_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_width_vq) - "
        "2*to_real(@custom_frame_line_width_vq) - "
        "to_real(@custom_item_dist_right_vq) - "
        "to_real(@custom_item_dist_left_vq)"
    ),
)
project_content.setFont(QFont(font, font_size))
project_content.setMargin(0)
project_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression("CalcLabelHeight(@layout_name, 'project_content')"),
)

new_layout.addLayoutItem(project_content)


### plan content frame###
plan_content_frame = QgsLayoutItemShape(new_layout)
plan_content_frame.setShapeType(QgsLayoutItemShape.Rectangle)
plan_content_frame.setId("plan_content_frame")
plan_content_frame.setFrameEnabled(True)
plan_content_frame.setFrameStrokeWidth(QgsLayoutMeasurement(custom_frame_line_width_vq))
plan_content_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression("GetDynamicItemPositionX(@layout_name ,'legend_frame')"),
)
plan_content_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name,'endura_frame') - "
        "GetDynamicItemHeight(@layout_name,'plan_content_frame')"
    ),
)
plan_content_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("@custom_frame_width_vq")
)
expr_plan_content_frame_height = (
    "to_real(@custom_frame_line_width_vq) +"
    "to_real(@custom_item_dist_top_vq) + "
    "GetDynamicItemHeight(@layout_name,'plan_content_title') + "
    "to_real(@custom_dist_title_text_vq) + "
    "GetDynamicItemHeight(@layout_name,'plan_content') + "
    "to_real(@custom_item_dist_bottom_vq)"
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
        "GetDynamicItemPositionX(  @layout_name ,'plan_content_frame') + (to_real(@custom_frame_line_width_vq)/2) + to_real(@custom_item_dist_left_vq)"
    ),
)
plan_content_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(  @layout_name ,'plan_content_frame') + "
        "@custom_frame_line_width_vq/2 + "
        "@custom_item_dist_top_vq"
    ),
)
plan_content_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_width_vq) - "
        "2*to_real(@custom_frame_line_width_vq) - "
        "to_real(@custom_item_dist_right_vq) - "
        "to_real(@custom_item_dist_left_vq)"
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
        "GetDynamicItemPositionX(  @layout_name ,'plan_content_frame') + (to_real(@custom_frame_line_width_vq)/2) + to_real(@custom_item_dist_left_vq)"
    ),
)
plan_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY( @layout_name, 'plan_content_title') + "
        "GetDynamicItemHeight(@layout_name,'plan_content_title') + "
        "to_real(@custom_dist_title_text_vq)"
    ),
)
plan_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_width_vq) - "
        "2*to_real(@custom_frame_line_width_vq) - "
        "to_real(@custom_item_dist_right_vq) - "
        "to_real(@custom_item_dist_left_vq)"
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
metadata_frame.setFrameStrokeWidth(QgsLayoutMeasurement(custom_frame_line_width_vq))
metadata_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression("GetDynamicItemPositionX(@layout_name ,'legend_frame')"),
)
metadata_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "@custom_page_size_height_vq - @custom_frame_line_width_vq - @custom_page_dist_bottom_vq - GetDynamicItemHeight(@layout_name,'metadata_frame')"
    ),
)
metadata_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("@custom_frame_width_vq")
)
expr_metadata_frame_height = (
    "to_real(@custom_frame_line_width_vq) +"
    "to_real(@custom_item_dist_top_vq) + "
    "GetDynamicItemHeight(@layout_name,'metadata') + "
    "to_real(@custom_item_dist_bottom_vq)"
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
    + "© XXX\n"
    + "Sonstige Karteninhalte: \n"
    + "eigene Darstellung"
)
metadata.setFont(QFont(font, font_size_metadata))
metadata.setMargin(0)
metadata.setId("metadata")
metadata.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(  @layout_name ,'metadata_frame') + @custom_frame_line_width_vq/2 + @custom_item_dist_left_vq"
    ),
)
metadata.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(  @layout_name ,'metadata_frame') + "
        "@custom_frame_line_width_vq/2 + "
        "@custom_item_dist_top_vq"
    ),
)
metadata.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_width_vq) - "
        "2*to_real(@custom_frame_line_width_vq) - "
        "to_real(@custom_item_dist_right_vq) - "
        "to_real(@custom_item_dist_left_vq)"
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
        "(GetDynamicItemWidth(@layout_name, 'map') + @custom_page_dist_left_vq) - @custom_item_dist_right_vq - @custom_north_arrow_width_vq"
    ),
)
north_arrow.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name, 'map') + @custom_item_dist_top_vq + @custom_frame_line_width_vq/2"
    ),
)
north_arrow.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("@custom_north_arrow_width_vq")
)
north_arrow.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight, QgsProperty.fromExpression("@custom_north_arrow_height_vq")
)
north_arrow.setLinkedMap(map)
north_arrow.setNorthMode(0)

new_layout.addLayoutItem(north_arrow)


### Scale Bar ###
scale_bar = QgsLayoutItemScaleBar(new_layout)
scale_bar.setId("scale_bar")
scale_bar.setFrameEnabled(False)

scale_bar.setStyle("Single Box")
scale_bar.setBoxContentSpace(0)
scale_bar.setFont(QFont(font, font_size_metadata))
scale_bar.setLabelBarSpace(custom_scale_label_space_vq)
scale_bar.setLinkedMap(map)
scale_bar.setHeight(custom_scale_bar_height_vq)


scale_bar.setReferencePoint(QgsLayoutItem.LowerLeft)

scale_bar.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name, 'map') + @custom_frame_line_width_vq/2 + @custom_item_dist_left_vq - 0.4"
    ),
)
scale_bar.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "(GetDynamicItemPositionY(@layout_name, 'map') + GetDynamicItemHeight(@layout_name, 'map')) - to_real(@custom_item_dist_bottom_vq) + 0.55"
    ),
)
scale_bar.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression(
        f"to_real(@custom_scale_bar_height_vq) + to_real(@custom_scale_label_space_vq) + {int(font_size_metadata)}*0.352778"
    ),
)

scale_bar.setSegmentSizeMode(Qgis.ScaleBarSegmentSizeMode.Fixed)
scale_bar.setUnits(QgsUnitTypes.DistanceMeters)
scale_bar.setMapUnitsPerScaleBarUnit(1)
scale_bar.setUnitsPerSegment(custom_scale_segment_length)  # Wie Lange die Bar sein soll
scale_bar.setNumberOfSegments(3)
scale_bar.setNumberOfSegmentsLeft(0)
scale_bar.setUnitLabel("m")

new_layout.addLayoutItem(scale_bar)


### Bearbeitungsbox ###
endura_frame = QgsLayoutItemShape(new_layout)
endura_frame.setShapeType(QgsLayoutItemShape.Rectangle)
endura_frame.setId("endura_frame")
endura_frame.setFrameEnabled(True)
endura_frame.setFrameStrokeWidth(QgsLayoutMeasurement(custom_frame_line_width_vq))
endura_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression("GetDynamicItemPositionX(@layout_name ,'legend_frame')"),
)
endura_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name,'metadata_frame') - "
        "GetDynamicItemHeight(@layout_name,'endura_frame')"
    ),
)
endura_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("@custom_frame_width_vq")
)
expr_endura_frame_height = "@custom_frame_line_width_vq + if((GetDynamicItemHeight(@layout_name, 'endura_logo') + 1.776) > GetDynamicItemHeight(@layout_name, 'endura_content'), (GetDynamicItemHeight(@layout_name, 'endura_logo') + 1.776), GetDynamicItemHeight(@layout_name, 'endura_content')) + @custom_item_dist_top_vq + @custom_item_dist_bottom_vq + GetDynamicItemHeight(@layout_name, 'endura_title') + @custom_dist_title_text_vq"
endura_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression(expr_endura_frame_height),
)

new_layout.addLayoutItem(endura_frame)

### endura title ###
endura_title = QgsLayoutItemLabel(new_layout)
endura_title.setText("Bearbeitung")
endura_title.setId("endura_title")
endura_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(  @layout_name ,'endura_frame') + (to_real(@custom_frame_line_width_vq)/2) + to_real(@custom_item_dist_left_vq)"
    ),
)
endura_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(  @layout_name ,'endura_frame') + "
        "@custom_frame_line_width_vq/2 + "
        "@custom_item_dist_top_vq"
    ),
)
endura_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_width_vq) - "
        "2*to_real(@custom_frame_line_width_vq) - "
        "to_real(@custom_item_dist_right_vq) - "
        "to_real(@custom_item_dist_left_vq)"
    ),
)
endura_title.setFont(QFont(font, font_size_title, QFont.Bold))
endura_title.setMargin(0)
endura_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression("CalcLabelHeight(@layout_name, 'endura_title')"),
)

new_layout.addLayoutItem(endura_title)

### endura logo ###
endura_logo = QgsLayoutItemPicture(new_layout)
endura_logo.setId("endura_logo")
endura_logo.setFrameEnabled(False)

endura_logo.setPicturePath(jpg_path_endura_logo)

endura_logo.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name, 'endura_frame') + (to_real(@custom_frame_line_width_vq)/2) + to_real(@custom_item_dist_left_vq) + 0.2"
    ),
)
endura_logo.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name, 'endura_frame') + @custom_frame_line_width_vq/2 + @custom_item_dist_top_vq + GetDynamicItemHeight(@layout_name, 'endura_title') + @custom_dist_title_text_vq + 1.776"
    ),
)
endura_logo.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("13")
)
endura_logo.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight, QgsProperty.fromExpression("6.5")
)

new_layout.addLayoutItem(endura_logo)


### endura Label ###
endura_content = QgsLayoutItemLabel(new_layout)
endura_content.setId("endura_content")
endura_content.setFrameEnabled(False)
endura_content.setText("endura kommunal GmbH\nEmmy-Noether-Straße 2\n79110 Freiburg")
endura_content.setFont(QFont(font, font_size))
endura_content.setMargin(0)

endura_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name, 'endura_logo') + to_real(@custom_item_dist_left_vq) + GetDynamicItemWidth(@layout_name, 'endura_logo')"
    ),
)
endura_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name, 'endura_frame') + @custom_frame_line_width_vq/2 + @custom_item_dist_top_vq + GetDynamicItemHeight(@layout_name, 'endura_title') + @custom_dist_title_text_vq"
    ),
)
endura_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "(GetDynamicItemPositionX(@layout_name, 'endura_frame') + @custom_frame_width_vq - @custom_item_dist_right_vq) - GetDynamicItemPositionX(@layout_name, 'endura_content')"
    ),
)
endura_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression("CalcLabelHeight(@layout_name, 'endura_content')"),
)

new_layout.addLayoutItem(endura_content)

### Auftragsbox ###
municipality_frame = QgsLayoutItemShape(new_layout)
municipality_frame.setShapeType(QgsLayoutItemShape.Rectangle)
municipality_frame.setId("municipality_frame")
municipality_frame.setFrameEnabled(True)
municipality_frame.setFrameStrokeWidth(QgsLayoutMeasurement(custom_frame_line_width_vq))
municipality_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression("GetDynamicItemPositionX(@layout_name ,'legend_frame')"),
)
municipality_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name,'project_frame') - "
        "GetDynamicItemHeight(@layout_name,'municipality_frame')"
    ),
)
municipality_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("@custom_frame_width_vq")
)
expr_municipality_frame_height = "@custom_frame_line_width_vq + if((GetDynamicItemHeight(@layout_name, 'municipality_logo')) > GetDynamicItemHeight(@layout_name, 'municipality_content'), (GetDynamicItemHeight(@layout_name, 'municipality_logo')), GetDynamicItemHeight(@layout_name, 'municipality_content')) + @custom_item_dist_top_vq + @custom_item_dist_bottom_vq + GetDynamicItemHeight(@layout_name, 'municipality_title') + @custom_dist_title_text_vq"
municipality_frame.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression(expr_municipality_frame_height),
)

new_layout.addLayoutItem(municipality_frame)

### municipality title ###
municipality_title = QgsLayoutItemLabel(new_layout)
municipality_title.setText("Auftraggeber")
municipality_title.setId("municipality_title")
municipality_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(  @layout_name ,'municipality_frame') + (to_real(@custom_frame_line_width_vq)/2) + to_real(@custom_item_dist_left_vq)"
    ),
)
municipality_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(  @layout_name ,'municipality_frame') + "
        "@custom_frame_line_width_vq/2 + "
        "@custom_item_dist_top_vq"
    ),
)
municipality_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "to_real(@custom_frame_width_vq) - "
        "2*to_real(@custom_frame_line_width_vq) - "
        "to_real(@custom_item_dist_right_vq) - "
        "to_real(@custom_item_dist_left_vq)"
    ),
)
municipality_title.setFont(QFont(font, font_size_title, QFont.Bold))
municipality_title.setMargin(0)
municipality_title.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression("CalcLabelHeight(@layout_name, 'municipality_title')"),
)

new_layout.addLayoutItem(municipality_title)

### municipality logo ###
municipality_logo = QgsLayoutItemPicture(new_layout)
municipality_logo.setId("municipality_logo")
municipality_logo.setFrameEnabled(False)

municipality_logo.setPicturePath(svg_path_municipality_logo)

municipality_logo.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name, 'municipality_frame') + (to_real(@custom_frame_line_width_vq)/2) + to_real(@custom_item_dist_left_vq) + 0.035"
    ),
)
municipality_logo.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name, 'municipality_frame') + @custom_frame_line_width_vq/2 + @custom_item_dist_top_vq + GetDynamicItemHeight(@layout_name, 'municipality_title') + @custom_dist_title_text_vq"
    ),
)
municipality_logo.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth, QgsProperty.fromExpression("13")
)
municipality_logo.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight, QgsProperty.fromExpression("14.083")
)

new_layout.addLayoutItem(municipality_logo)


### municipality Label ###
municipality_content = QgsLayoutItemLabel(new_layout)
municipality_content.setId("municipality_content")
municipality_content.setFrameEnabled(False)
municipality_content.setText("Gemeinde/Stadt\nXXX")
municipality_content.setFont(QFont(font, font_size))
municipality_content.setMargin(0)

municipality_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionX,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionX(@layout_name, 'municipality_logo') + to_real(@custom_item_dist_left_vq) + GetDynamicItemWidth(@layout_name, 'municipality_logo')"
    ),
)
municipality_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.PositionY,
    QgsProperty.fromExpression(
        "GetDynamicItemPositionY(@layout_name, 'municipality_frame') + @custom_frame_line_width_vq/2 + @custom_item_dist_top_vq + GetDynamicItemHeight(@layout_name, 'municipality_title') + @custom_dist_title_text_vq"
    ),
)
municipality_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemWidth,
    QgsProperty.fromExpression(
        "(GetDynamicItemPositionX(@layout_name, 'municipality_frame') + @custom_frame_width_vq - @custom_item_dist_right_vq) - GetDynamicItemPositionX(@layout_name, 'municipality_content')"
    ),
)
municipality_content.dataDefinedProperties().setProperty(
    QgsLayoutObject.ItemHeight,
    QgsProperty.fromExpression("CalcLabelHeight(@layout_name, 'municipality_content')"),
)

new_layout.addLayoutItem(municipality_content)
