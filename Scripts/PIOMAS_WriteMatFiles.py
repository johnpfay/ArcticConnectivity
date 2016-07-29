#PIOMAS_WriteMATFiles.py
#
# Writes ASCII files for use in developing Eric's simulations. This script must be run 
# afterthe PIOMAS_ReadGrid.py script that extracts the UV vector point data for all
# survey years and interpolates them into 2-band (U and V) rasters projected to the
# EASE North coordinate system. This script also requires a polygon feature class
# of the study extent.
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
dataDir = os.path.join(rootDir,"Data")
scratchDir = os.path.join(rootDir,"Scratch")
simDir = os.path.join(dataDir,"SimDir")

#Create SimDir if it doesn't exist
if not os.path.exists(simDir):
    os.mkdir(simDir)

#Get extent feature class and raster, located in the Data/General folder
extentFC = os.path.join(rootDir,"Data","General","MaskPoly.shp")
maskRaster = os.path.join(rootDir,"Data","General","PIOMAS_Mask.img")

#Out raster, segment features, and ASCII arrays
segmentsFC = os.path.join(simDir,"GISFiles","Segments500FC.shp")
outRaster = os.path.join(simDir,"GISFiles","Segments500.img")
maskASCII = os.path.join(simDir,"MASK.ASC")
reefIdASCII = os.path.join(simDir,"ReefIDs.ASC")
reefPropsASCII = os.path.join(simDir,"ReefProps.ASC")

#Set arcpy environments
arcpy.env.snapRaster = maskRaster
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = scratchDir
arcpy.env.cellSize = maskRaster
arcpy.env.extent = maskRaster

##CREATE COASTAL SEGMENTS
#Convert edge cells in PIOMAS_Mask.img to a polyline feature class
print "Converting edge cells in mask to polyline feature class"
edgelineFC = arcpy.RasterDomain_3d(maskRaster,"in_memory/tmpLines","LINE")

#Convert to single part features
edgelinesFC = arcpy.MultipartToSinglepart_management(edgelineFC,"in_memory/Edgelines")

#Eliminate those ;ines along the edge
borderFC = arcpy.FeatureToLine_management(extentFC,"in_memory/borderLine")
edgelines2FC = arcpy.Erase_analysis(edgelinesFC,borderFC,"in_memory/edgelines2","15000 meters")

#Generate points along the line
print "Creating points every 500km"
linePointsFC = arcpy.GeneratePointsAlongLines_management(edgelines2FC,"in_memory/Pts500km","DISTANCE","500 kilometers")

#Split lines using above points
print "Splitting lines every 500 km"
arcpy.SplitLineAtPoint_management(edgelines2FC,linePointsFC,segmentsFC,"500 meters")
arcpy.CalculateField_management(segmentsFC,"ORIG_FID","[FID]")

#Convert to raster
print "Saving raster to {}".format(outRaster)
arcpy.PolylineToRaster_conversion(segmentsFC,"FID",outRaster)

##Write output ASCII files
#Create ASCII array from Mask
rawArr = arcpy.RasterToNumPyArray(maskRaster,nodata_to_value=0)
np.savetxt(maskASCII,rawArr,fmt='%i')

#Create reefIDs array from sausages
reefIDArr = arcpy.RasterToNumPyArray(outRaster,nodata_to_value=0)
np.savetxt(reefIdASCII,reefIDArr,fmt='%i')

#Create reefProps array by coding IDs to 1s
reefPropsArr = reefIDArr.copy()
reefPropsArr[reefIDArr > 0] = 1
np.savetxt(reefPropsASCII,reefPropsArr,fmt='%i')

