#GridToVectors.py
#
# Converts a 2-band raster of U and V values to a vector file to serve as the basis
#  for a network dataset to map connectity within the Arctic.
#
# July 2016
# John.Fay@duke.edu

import os
import numpy as np
import arcpy

#Folder structure
scriptDir = os.path.dirname(sys.argv[0])
rootDir = os.path.dirname(scriptDir)
dataDir = os.path.join(rootDir,"Data")
scratchDir = os.path.join(rootDir,"Scratch")
scratchGDB = os.path.join(scratchDir,"Scratch.gdb")

#Data vars (replace XX with month to get the monthly file...)
monthlyDir = os.path.join(dataDir,"NSIDC","ndisc0116_icemotion_vectors_v3","monthly_clim")
templateFN = os.path.join(monthlyDir,'icemotion.grid.monthlyclim.XX.n.v3.bin')

#File specs
xDim = 361
yDim = 361
nGrids = 3
valType = np.int16
lowerleft = arcpy.Point(-4493750,-4493750)

#Arcpy environment settings
arcpy.CheckOutExtension('spatial')
arcpy.env.overwriteOutput = 1
arcpy.env.scratchWorkspace = scratchDir
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3408) #NSIDC_EASE_Grid_North 

##---FUNCTIONS---
def msg(txt,severity=''):
    print txt
    if severity == 'warning':
        arcpy.AddWarning(txt)
    elif severity == 'error':
        arcpy.AddError(txt)
    else: arcpy.AddMessage(txt)

##--PROCEDURES---
#Set the month (OR LOOP THROUGH ALL MONTHS)
mo = str(1).zfill(2)
msg("Processing month: {}".format(mo))
    
#Output Variables
netFC = os.path.join(scratchDir,"Vectors{}.shp".format(mo))
msg("...Output will be set to: ".format(netFC))

#Get the monthly filename (from the templateFN)
monthlyFN = templateFN.replace("XX",mo)
#Convert icemotion file to numpy array
with open(monthlyFN,'rb') as inFile:
    arrMO = np.fromfile(monthlyFN,valType).reshape((xDim,yDim,nGrids))
msg("...Data extracted to array")

#Extract u/v arrays and reshape to 1D data vectors
msg("...extracting u, v components")
uValues = arrMO[:,:,0].reshape(-1).astype(np.float)
vValues = arrMO[:,:,1].reshape(-1).astype(np.float)

#Compute magnitudes (via pythagorean theorem); * 10 to preserve precision
msg("...computing magnitudes")
mValues = np.sqrt(np.square(uValues) + np.square(vValues)) * 10

#Create a mask from the 3rd band
msg("...creating mask raster")
maskRaster = arcpy.NumPyArrayToRaster(arrMO[:,:,2],lowerleft,25000,25000,0)
arcpy.env.mask = maskRaster

#Compute the arctan of above to get the angle, in radians
msg("...converting u,v to angles")
thetaRadians = np.arctan2(vValues,uValues)

#Reclassify to flow direction values
msg("...creating flow direction from angles")
pi8 = np.pi / 8.0
fdirVals = np.copy(thetaRadians)
fdirVals[thetaRadians > (7 * pi8)] = 16     #W
fdirVals[thetaRadians <= (7 * pi8)] = 32    #NW
fdirVals[thetaRadians <= (5 * pi8)] = 64    #N
fdirVals[thetaRadians <= (3 * pi8)] = 128   #NE
fdirVals[thetaRadians <= (1 * pi8)] = 1     #E
fdirVals[thetaRadians <= (-1 * pi8)] = 2    #SE
fdirVals[thetaRadians <= (-3 * pi8)] = 4    #S
fdirVals[thetaRadians <= (-5 * pi8)] = 8    #SW
fdirVals[thetaRadians <= (-7 * pi8)] = 16   #W

#Reshape the flow direction array (as integers) and convert to an ArcGIS raster
msg("...creating raster from flow direction array")
fdirArr = fdirVals.reshape(361,361).astype(np.int16)
fdirRaster = arcpy.NumPyArrayToRaster(fdirArr,lowerleft,25000)

#Create stream raster from magnitudes
msg("...creating magnitude raster from magnitude array")
strmArr = mValues.reshape(361,361).astype(np.int16)
strmRaster = arcpy.NumPyArrayToRaster(strmArr,lowerleft,25000)

#Create netfeature class
msg("...Creating polyline vector file via StreamToFeature tool")
arcpy.sa.StreamToFeature(strmRaster,fdirRaster,netFC,"FALSE")

#Add time field (hours consumed traveling across feature
arcpy.AddField_management(netFC,"Days","FLOAT",8,2)
#...Select records with GRID_CODE (cm*10/s) > 0
tmpLyr = arcpy.MakeFeatureLayer_management(netFC,"tmpLyr","GRID_CODE > 0")
#...Convert to hours required to span the feature
calcString = "!shape.length! / (0.001 * 86400 * !GRID_CODE!)" #Converts cm*100/sec to m/day to km
calcString = "!shape.length! * 1000.0 * (1.0 / !GRID_CODE!) * (1/3600.0)"
arcpy.CalculateField_management(tmpLyr,"Days",calcString,"PYTHON")

#Cleanup
arcpy.Delete_management(fdirRaster)
arcpy.Delete_management(strmRaster)