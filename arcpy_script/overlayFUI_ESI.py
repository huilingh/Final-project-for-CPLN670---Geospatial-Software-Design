"""
THIS SCRIPT OVERLAY THE FUI AND ESI LAYER BY MULTIPLYING THE VALUES

To create an ArcToolbox tool with which to execute this script, do the following.
1   In  ArcMap > Catalog > Toolboxes > My Toolboxes, either select an existing toolbox
    or right-click on My Toolboxes and use New > Toolbox to create (then rename) a new one.
2   Drag (or use ArcToolbox > Add Toolbox to add) this toolbox to ArcToolbox.
3   Right-click on the toolbox in ArcToolbox, and use Add > Script to open a dialog box.
4   In this Add Script dialog box, use Label to name the tool being created, and press Next.
5   In a new dialog box, browse to the .py file to be invoked by this tool, and press Next.
6   In the next dialog box, specify the following inputs (using dropdown menus wherever possible)
    before pressing OK or Finish.
        DISPLAY NAME        DATA TYPE           PROPERTY>DIRECTION>VALUE    DEFAULT   
        FUI layer           Feature Layer       Input  
        ESI layer           Feature Layer       Input
        output              Feature Class       Output
    
   To later revise any of this, right-click to the tool's name and select Properties.
"""

# Import external modules
import sys, os, string, math, arcpy, traceback, numpy
from arcpy import env

# Allow output to overwite any existing grid of the same name
arcpy.env.overwriteOutput = True

root = "E:/Study-18Fall/GeospaticialSoftware/EEProject_Data/shp_arcpy/"

try:
        # read input
        inputFUI = arcpy.GetParameterAsText(0)
        inputESI = arcpy.GetParameterAsText(1)
        output = arcpy.GetParameterAsText(2)
        

        # tabular join
        join_table = arcpy.AddJoin_management(inputFUI, "Source_ID", inputESI, "Source_ID", "KEEP_COMMON")
        arcpy.CopyFeatures_management(join_table, output)


        # calculation
        arcpy.AddField_management(output, "FUI", "DOUBLE", 20, 5)
        arcpy.AddField_management(output, "ESI", "DOUBLE", 20, 5)
        arcpy.AddField_management(output, "Index", "DOUBLE", 20, 5)

        fieldnameFUI = inputFUI[:-3] + "_1"
        fieldnameESI = inputESI[:-3] + "_3"

        enumeration = arcpy.UpdateCursor(output)

        for row in enumeration:
            FUI = row.getValue(fieldnameFUI)
            ESI = row.getValue(fieldnameESI)
            row.setValue("FUI", FUI)
            row.setValue("ESI", ESI)
            
            index = FUI*ESI
            arcpy.AddMessage("FUI*ESI =  " + str(index))
            row.setValue("Index", index)
            
            enumeration.updateRow(row)


        del row
        del enumeration
        

        
except Exception as e:
        # If unsuccessful, end gracefully by indicating why
        arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
        # ... and where
        exceptionreport = sys.exc_info()[2]
        fullermessage   = traceback.format_tb(exceptionreport)[0]
        arcpy.AddError("at this location: \n\n" + fullermessage + "\n")
        
        
