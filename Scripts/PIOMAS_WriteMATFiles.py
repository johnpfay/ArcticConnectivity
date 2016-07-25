#PIOMAS_WriteMATFiles.py
#
# Writes MAT files for use in Eric's simulation. These include the mask
#
# July 2015
# John.Fay@duke.edu

import sys, os, gzip
import numpy as np
import arcpy


#Get folder locations, relative to this script (which should be in scripts folder)
scriptDir = os.path.dirname(sys.argv[0])
rootDir = os.path.dirname(scriptDir)
dataDir = os.path.join(rootDir,"Data","PolarScienceCenter","PIOMAS")
scratchDir = os.path.join(rootDir,"Scratch","Scratch.gdb")
rawDir = os.path.join(dataDir,"RawData")
outDir = os.path.join(dataDir,"Processed")

#Get extent feature class and raster
maskRaster = os.path.join(rootDir,"Data","General","PIOMAS_Mask.img")
arcpy.env.snapRaster = maskRaster
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = scratchDir
arcpy.CheckOutExtension('spatial')

##CREATE SAUSAGES
#Invert the mask
invMaskBin = arcpy.sa.IsNull(maskRaster)
#invMaskND = arcpy.sa.Con(invMaskBin,1)
#invMaskND.save(os.path.join(scratchDir,"UnMask"))
expandMask = arcpy.sa.Expand(invMaskBin,1,1)
border1 = arcpy.sa.ExtractByMask(expandMask,maskRaster)
border2 = arcpy.sa.Con(border1,1)
border2.save(os.path.join(scratchDir,"SausageZone"))