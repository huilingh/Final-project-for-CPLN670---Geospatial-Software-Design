"""
THIS SCRIPT WILL:
A.  EXTRACT VALUES FROM RASTER (THE INDICATOR AND DECISION FACTORS OF FUI) AND SPATIAL JOIN THE VALUES TO EACH FISHNET GRID CELL
B.  RUN GWR ON EACH GRID CELL AND RECLASSIFY THE PREDICTED VALUES (PREDICTED NIGHTLIGHT CHANGES) INTO FOUR EQUAL INTERVALS

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
        study area          Feature Layer       Input  
        output              Feature Class       Output
        dependent raster    Raster Layer        Input
        predictor raster1   Raster Layer        Input
        predictor raster2   Raster Layer        Input
        predictor raster3   Raster Layer        Input
        predictor raster4   Raster Layer        Input
    
   To later revise any of this, right-click to the tool's name and select Properties.
"""

# Import external modules
import sys, os, string, math, arcpy, traceback, numpy
from arcpy import env

# Allow output to overwite any existing grid of the same name
arcpy.env.overwriteOutput = True


root = "E:/Study-18Fall/GeospaticialSoftware/EEProject_Data/shp_arcpy/"

def SpatialJoinFUI(target, dependent, predictor1, predictor2, predictor3, predictor4, output):
        inter1 = root + "inter1.shp"
        inter2 = root + "inter2.shp"
        inter3 = root + "inter3.shp"
        inter4 = root + "inter4.shp"

        # spatial join dependent variable
        fieldmappings1 = arcpy.FieldMappings()
        fieldmappings1.addTable(target)
        fieldmappings1.addTable(dependent)

        gridValue1 = fieldmappings1.findFieldMapIndex("grid_code")
        fieldmap1 = fieldmappings1.getFieldMap(gridValue1)

        field1 = fieldmap1.outputField
        field1.name = "DV"
        fieldmap1.outputField = field1

        fieldmap1.mergeRule = "mean"
        fieldmappings1.replaceFieldMap(gridValue1, fieldmap1)

        arcpy.SpatialJoin_analysis(target, dependent, inter1, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings1, "CONTAINS")


        # spatial join the first predictor
        fieldmappings2 = arcpy.FieldMappings()
        fieldmappings2.addTable(inter1)
        fieldmappings2.addTable(predictor1)

        gridValue2 = fieldmappings2.findFieldMapIndex("grid_code")
        fieldmap2 = fieldmappings2.getFieldMap(gridValue2)

        field2 = fieldmap2.outputField
        field2.name = "pre1"
        fieldmap2.outputField = field2

        fieldmap2.mergeRule = "mean"
        fieldmappings2.replaceFieldMap(gridValue2, fieldmap2)

        arcpy.SpatialJoin_analysis(inter1, predictor1, inter2, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings2, "CONTAINS")


        # spatial join the second predictor
        fieldmappings3 = arcpy.FieldMappings()
        fieldmappings3.addTable(inter2)
        fieldmappings3.addTable(predictor2)

        gridValue3 = fieldmappings3.findFieldMapIndex("grid_code")
        fieldmap3 = fieldmappings3.getFieldMap(gridValue3)

        field3 = fieldmap3.outputField
        field3.name = "pre2"
        fieldmap3.outputField = field3

        fieldmap3.mergeRule = "mean"
        fieldmappings3.replaceFieldMap(gridValue3, fieldmap3)

        arcpy.SpatialJoin_analysis(inter2, predictor2, inter3, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings3, "CONTAINS")


        # spatial join the third predictor
        fieldmappings4 = arcpy.FieldMappings()
        fieldmappings4.addTable(inter3)
        fieldmappings4.addTable(predictor3)

        gridValue4 = fieldmappings4.findFieldMapIndex("grid_code")
        fieldmap4 = fieldmappings4.getFieldMap(gridValue4)

        field4 = fieldmap4.outputField
        field4.name = "pre3"
        fieldmap4.outputField = field4

        fieldmap4.mergeRule = "mean"
        fieldmappings4.replaceFieldMap(gridValue4, fieldmap4)

        arcpy.SpatialJoin_analysis(inter3, predictor3, inter4, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings4, "CONTAINS")


        # spatial join the fourth predictor
        fieldmappings5 = arcpy.FieldMappings()
        fieldmappings5.addTable(inter4)
        fieldmappings5.addTable(predictor4)

        gridValue5 = fieldmappings5.findFieldMapIndex("grid_code")
        fieldmap5 = fieldmappings5.getFieldMap(gridValue5)

        field5 = fieldmap5.outputField
        field5.name = "pre4"
        fieldmap5.outputField = field5

        fieldmap5.mergeRule = "mean"
        fieldmappings5.replaceFieldMap(gridValue5, fieldmap5)

        arcpy.SpatialJoin_analysis(inter4, predictor4, output, "JOIN_ONE_TO_ONE", "KEEP_ALL", fieldmappings5, "CONTAINS")

        # Delete the intermediate shapefile
        arcpy.Delete_management(inter1)
        arcpy.Delete_management(inter2)
        arcpy.Delete_management(inter3)
        arcpy.Delete_management(inter4)

        return output




# If Spatial Analyst license is available, check it out
if arcpy.CheckExtension("spatial") == "Available":
    arcpy.CheckOutExtension("spatial")

    try:
        # read input
        inboundary = arcpy.GetParameterAsText(0)
        output = arcpy.GetParameterAsText(1)
        inraster1 = arcpy.GetParameterAsText(2)
        inraster2 = arcpy.GetParameterAsText(3)
        inraster3 = arcpy.GetParameterAsText(4)
        inraster4 = arcpy.GetParameterAsText(5)
        inraster5 = arcpy.GetParameterAsText(6)
        
        # convert raster to points
        rasterPoint1 = root + inraster1[:-4] + "_temp.shp"
        rasterPoint2 = root + inraster2[:-4] + "_temp.shp"
        rasterPoint3 = root + inraster3[:-4] + "_temp.shp"
        rasterPoint4 = root + inraster4[:-4] + "_temp.shp"
        rasterPoint5 = root + inraster5[:-4] + "_temp.shp"

        arcpy.RasterToPoint_conversion(inraster1, rasterPoint1, "VALUE")
        arcpy.RasterToPoint_conversion(inraster2, rasterPoint2, "VALUE")
        arcpy.RasterToPoint_conversion(inraster3, rasterPoint3, "VALUE")
        arcpy.RasterToPoint_conversion(inraster4, rasterPoint4, "VALUE")
        arcpy.RasterToPoint_conversion(inraster5, rasterPoint5, "VALUE")


        # spatial join points to fishnet and get the average values
        spatialJoin_result = root + "spaResult_FUI.shp"
        SpatialJoinFUI(inboundary, rasterPoint1, rasterPoint2, rasterPoint3, rasterPoint4, rasterPoint5, spatialJoin_result)



        # run GWR
        GWR_result = root + "GWR_resultFUI.shp"
        predictor = "pre1;pre2;pre3;pre4"
        arcpy.GeographicallyWeightedRegression_stats(spatialJoin_result, "DV", predictor, GWR_result, "ADAPTIVE", "BANDWIDTH PARAMETER","#", "40", "#", "#", "#", "#", "#", "#")
        

        # reclassify GWR predicted value and get the FUI classification
        # Replicate the GWR result
        GWR_reclassify = output
        arcpy.Copy_management(GWR_result, GWR_reclassify)
        arcpy.AddField_management(GWR_reclassify, "FUI", "DOUBLE", 20, 5)

        # get the min and max predicted values       
        GWR_min = GWR_reclassify[:-4] + "_min.shp"
        GWR_max = GWR_reclassify[:-4] + "_max.shp"

        arcpy.Sort_management(GWR_reclassify,GWR_min,[["Predicted", "ASCENDING"]])
        arcpy.Sort_management(GWR_reclassify,GWR_max,[["Predicted", "DESCENDING"]])
        
        enumeration_min = arcpy.SearchCursor(GWR_min)
        minValue = enumeration_min.next().getValue("Predicted")
        arcpy.AddMessage("Minimum predicted value:  " + str(minValue) + "\n")

        enumeration_max = arcpy.SearchCursor(GWR_max)
        maxValue = enumeration_max.next().getValue("Predicted")
        arcpy.AddMessage("Maximum predicted value:  " + str(maxValue) + "\n")

        increase = (maxValue - minValue)/4
        first = increase + minValue
        second = increase*2 + minValue
        third = increase*3 + minValue

        del enumeration_min
        del enumeration_max

        # Delete the intermediate shapefile
        arcpy.Delete_management(GWR_min)
        arcpy.Delete_management(GWR_max)
        
        # reclassify
        enumeration = arcpy.UpdateCursor(GWR_reclassify)
        
        for row in enumeration:
            predicted = row.getValue("Predicted")
            if predicted < first:
                row.setValue("FUI", 1)
            elif predicted >= first and predicted < second:
                row.setValue("FUI", 2)
            elif predicted >= second and predicted < third:
                row.setValue("FUI", 3)
            else:
                row.setValue("FUI", 4)
            
            enumeration.updateRow(row)


        # delete unnecessary fields
        dropFieldFUI = ["Observed", "Cond", "LocalR2", "Predicted", "Intercept", "C1_pre1", "C2_pre2", "C3_pre3", "C4_pre4",
                        "Residual", "StdError", "StdErr_Int", "StdErrC1_p", "StdErrC2_p", "StdErrC3_p", "StdErrC4_p", "StdResid"]
        arcpy.DeleteField_management(GWR_reclassify, dropFieldFUI)

        

        del row
        del enumeration

        # Delete the intermediate shapefile
        arcpy.Delete_management(rasterPoint1)
        arcpy.Delete_management(rasterPoint2)
        arcpy.Delete_management(rasterPoint3)
        arcpy.Delete_management(rasterPoint4)
        arcpy.Delete_management(rasterPoint5)

        
    except Exception as e:
        # If unsuccessful, end gracefully by indicating why
        arcpy.AddError('\n' + "Script failed because: \t\t" + e.message )
        # ... and where
        exceptionreport = sys.exc_info()[2]
        fullermessage   = traceback.format_tb(exceptionreport)[0]
        arcpy.AddError("at this location: \n\n" + fullermessage + "\n")
        
    # Check in Spatial Analyst extension license
    arcpy.CheckInExtension("spatial")      
else:
    print "Spatial Analyst license is " + arcpy.CheckExtension("spatial")
        
