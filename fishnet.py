"""
THIS SCRIPT CREATE A FISHNET OF THE STUDY REGION

To create an ArcToolbox tool with which to execute this script, do the following.
1   In  ArcMap > Catalog > Toolboxes > My Toolboxes, either select an existing toolbox
    or right-click on My Toolboxes and use New > Toolbox to create (then rename) a new one.
2   Drag (or use ArcToolbox > Add Toolbox to add) this toolbox to ArcToolbox.
3   Right-click on the toolbox in ArcToolbox, and use Add > Script to open a dialog box.
4   In this Add Script dialog box, use Label to name the tool being created, and press Next.
5   In a new dialog box, browse to the .py file to be invoked by this tool, and press Next.
6   In the next dialog box, specify the following inputs (using dropdown menus wherever possible)
    before pressing OK or Finish.
        DISPLAY NAME            DATA TYPE               PROPERTY>DIRECTION>VALUE    DEFAULT   
        Input study region      Feature Layer           Input  
        Output                  RFeature Class          Output  
    
   To later revise any of this, right-click to the tool's name and select Properties.
"""

# Import external modules
import sys, os, string, math, arcpy, traceback, numpy
from arcpy import env

# set spatial reference
env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984 World Mercator")

# Allow output to overwite any existing grid of the same name
arcpy.env.overwriteOutput = True

try:
        # read input
        inputfeature = arcpy.GetParameterAsText(0)
        output = arcpy.GetParameterAsText(1)

        originCoordinate = "12510695.68633178 2480781.535645782"
        yAxisCoordinate = "12510695.68633178 2480791.535645782"
        oppositeCoorner = "12759882.01763127 2728238.175390986"

        root = "E:/Study-18Fall/GeospaticialSoftware/EEProject_Data/shp_arcpy/"
        fishnet = root + "_fishnetboundary.shp"

        arcpy.CreateFishnet_management(fishnet, originCoordinate, yAxisCoordinate, "2500", "2500", "0", "0", oppositeCoorner, "NO_LABELS", "#", "POLYGON")

        arcpy.MakeFeatureLayer_management(fishnet, "fishnet_lyr")
        arcpy.SelectLayerByLocation_management("fishnet_lyr", "INTERSECT", inputfeature)
        arcpy.CopyFeatures_management("fishnet_lyr", output)

        arcpy.Delete_management(fishnet)

        

        
except Exception as e:
        # If unsuccessful, end gracefully by indicating why
        arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
        # ... and where
        exceptionreport = sys.exc_info()[2]
        fullermessage   = traceback.format_tb(exceptionreport)[0]
        arcpy.AddError("at this location: \n\n" + fullermessage + "\n")
        
