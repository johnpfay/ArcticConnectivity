#MonthlyIceToGrids
#
# Processes ice vector data and converts to rasters
#
# July 2015
# John.Fay@duke.edu

import os, arcpy
import numpy as np

#Variables
outWorkspace = r'C:\workspace\ArcticConnectivity\scratch'

#ArcPy settings
arcpy.CheckOutExtension('spatial')
arcpy.env.scratchWorkspace = outWorkspace
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3408)

#URLs
monthlyURL = r'ftp://sidads.colorado.edu/pub/DATASETS/nsidc0116_icemotion_vectors_v3/data/north/monthly_clim/'
monthlyFile = 'icemotion.grid.monthlyclim.XX.n.v3.bin'

#Data folder
dataFldr = r'C:\workspace\ArcticConnectivity\Data\NSIDC\ndisc0116_icemotion_vectors_v3\monthly_clim'
dataFile = os.path.join(dataFldr,'icemotion.grid.monthlyclim.XX.n.v3.bin')

#Convert each one
mo = "02"
moFile = dataFile.replace("XX",mo)
xDim = 361
yDim = 361
nGrids = 3
valSize = 16
lowerleft = arcpy.Point(-8987500/2,-8987500/2)
outRaster = r"C:\workspace\ArcticConnectivity\Scratch\scratch.gdb\Monthly"+mo

with open(moFile,'rb') as inFile:
    arr = np.fromfile(inFile, np.int16).reshape((xDim,yDim,nGrids))

band1 = arcpy.NumPyArrayToRaster(arr[:,:,0],lowerleft,25000,25000)
band2 = arcpy.NumPyArrayToRaster(arr[:,:,1],lowerleft,25000,25000)
band3 = arcpy.NumPyArrayToRaster(arr[:,:,2],lowerleft,25000,25000,0)

band1x = arcpy.sa.ExtractByMask(band1,band3)
band2x = arcpy.sa.ExtractByMask(band2,band3)

arcpy.CompositeBands_management([band1x,band2x],outRaster)


