#PIOMAS_WriteMATFiles.py
#
# Writes MAT files for use in Eric's simulation. This script must be run after
# the PIOMAS_ReadGrid.py script that extracts the UV vector point data for all
# survey years and interpolates them into 2-band (U and V) rasters projected to
# the EASE North coordinate system. This script also requires a polygon feature 
# class of the study extent.
#
# July 2015
# John.Fay@duke.edu

import sys, os, gzip, arcpy
import numpy as np

#Check out the spatial analyst extension
arcpy.CheckOutExtension('spatial')
arcpy.CheckOutExtension('3D')

#Get folder locations, relative to this script (which should be in scripts folder)
scriptDir = os.path.dirname(sys.argv[0])
rootDir = os.path.dirname(scriptDir)
dataDir = os.path.join(rootDir,"Data","PolarScienceCenter","PIOMAS")
scratchDir = os.path.join(rootDir,"Scratch","Scratch.gdb")
rawDir = os.path.join(dataDir,"RawData")
outDir = os.path.join(dataDir,"Processed")

#Get extent feature class and raster, located in the Data/General folder
extentFC = os.path.join(rootDir,"Data","General","MaskPoly.shp")
maskRaster = os.path.join(rootDir,"Data","General","PIOMAS_Mask.img")

#Out raster
outRaster = os.path.join(scratchDir,"Sausages")

#Set arcpy environments
arcpy.env.snapRaster = maskRaster
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = scratchDir
arcpy.env.cellSize = maskRaster

##CREATE SAUSAGES
#Convert edge cells in PIOMAS_Mask.img to a polyline feature class
print "Converting edge cells in mask to polyline feature class"
edgelineFC = arcpy.RasterDomain_3d(maskRaster,"in_memory/tmpLines","LINE")
#Convert to single part features
print "Converting to singlepart features"
edgelinesFC = arcpy.MultipartToSinglepart_management(edgelineFC,"in_memory/Edgelines")
#Generate points along the line
linePointsFC = arcpy.GeneratePointsAlongLines_management(edgelinesFC,"in_memory/Pts500km","DISTANCE","500 kilometers")
#Split lines using above points
segmentsFC = arcpy.SplitLineAtPoint_management(edgelinesFC,linePointsFC,"in_memory/LineSegments","500 meters")
#Convert to raster
print "Saving raster"
outRaster = arcpy.PolylineToRaster_conversion(segmentsFC,"OID",outRaster)