#Dispersinator.py
#
# Disperses values in an origin array using u/v arrays

import sys, os
import numpy as np
import arcpy

#Folders
scriptDir = os.path.dirname(sys.argv[0])
rootDir = os.path.dirname(scriptDir)
dataDir = os.path.join(rootDir,"Data","PolarScienceCenter","PIOMAS")
scratchDir = os.path.join(rootDir,"Scratch")
uvDir = os.path.join(dataDir,"Processed")

#Inputs
sourceRaster = os.path.join(scratchDir,"Source")
cellSize = 25000
arcpy.env.workspace = uvDir

#ArcPy stuff
arcpy.env.overwriteOutput = True
srEASE = arcpy.SpatialReference(3408)

#Get the list of rasters (for the current year
uvRasters = arcpy.ListRasters("uv2013*")

#Convert source raster to array
srcArr = arcpy.RasterToNumPyArray(sourceRaster)

#Create arrays from uv rasters
'''arrDict = {}
for uvRaster in uvRasters:
    month = int(uvRaster[-6:-4])
    uBand = os.path.join(uvRaster,"Layer_1")
    vBand = os.path.join(uvRaster,"Layer_2")
    uArr = arcpy.RasterToNumPyArray(uBand)
    vArr = arcpy.RasterToNumPyArray(vBand)
    arrDict[month] = (uArr,vArr)
print "{} arrays created".format(len(arrDict))'''

#Loop through time steps
for t in range(1,13):
    #Create array with end of time step contents
    newArr = srcArr.astype(np.float32)#srcArr.copy()
    
    #Get the array for the current time step
    uArr,vArr = arrDict[t]

    #Get coords of cells with larvae
    xArr,yArr = srcArr.nonzero()

    #Loop through each cell and create coordinate arrays
    for i in range(len(xArr)):
        x = xArr[i]
        y = yArr[i]
    
        #Get the contents at current cell
        cXY = srcArr[x,y]
        
        #Get U and V values at the coordinate 
        uXY = float(uArr[x,y]) #cm/s
        vXY = float(vArr[x,y])
        secPerMonth = 60 * 60 * 24 * 30
        uXYmo = uXY * secPerMonth / cellSize
        vXYmo = vXY * secPerMonth / cellSize

        #Calculate amounts moving to u and v directions
        v = float(abs(uXY) + abs(vXY))
        pU = abs(uXY) / v * cXY
        pV = abs(vXY) / v * cXY
        #uGo = abs(uXY); uStay = 1-uGO
        #vGo = abs(vXY); vStay = 1+vGO

        #Determine the coords of the receiving cells
        if uXY < 1: toX = x - 1
        else: toX = x + 1
        if vXY < 1: toY = y - 1
        else: toY = y + 1

        #Disperse contents to destination
        newArr[x,y] = srcArr[x,y] - pU - pV #Deduct stuff that left
        newArr[toX,y] = srcArr[x,y] + pU    #Move in U direction
        newArr[x,toY] = srcArr[x,y] + pV    #Move in V direction

        #Zero out negatives
        newArr[newArr < 0] = 0

    #write to a raster
    outRaster = arcpy.NumPyArrayToRaster(newArr,arcpy.Point(-4493750,-4493750),25000)
    arcpy.DefineProjection_management(outRaster,srEASE)
    outRaster.save(os.path.join(scratchDir,"step{}.img".format(t)))

    #update srcArr
    srcArr = newArr.copy()