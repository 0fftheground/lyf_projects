import arcpy
import os
database = r'E:\路径展示\route_display.gdb'
arcpy.env.workspace = database
arcpy.env.overwriteOutput = True
#arcpy.Copy_management("climate.shp", "climateXYpts.shp")
#arcpy.AddXY_management("climateXYpts.shp")
#arcpy.AddXY_management
arcpy.management.XYTableToPoint(r"E:\workplace\py36\0914\_converted_route_11.csv","store"
                                "mapX", "mapY", arcpy.SpatialReference(4326))