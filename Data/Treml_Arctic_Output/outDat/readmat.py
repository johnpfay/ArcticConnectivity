from scipy import io
import numpy as np
import sys, os, arcpy

arcpy.env.scratchWorkspace = r'C:\Workspace\Gits\ArcticConnectivity\Scratch'
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension('spatial')

file = 'Arctic_Feb1978_100day_Test_out.mat'
outGDB = r'C:\Workspace\Gits\ArcticConnectivity\Scratch\output.gdb'

llCorner = arcpy.Point(-3567696.94076,-2743739.54274)
srEASE = arcpy.SpatialReference(3408) #NSIDC_EASE_Grid_North

matFile = io.loadmat(file)

dispMat = matFile['dispMat']
denMat = matFile['denMat']

for i in range(101):
    tmpRaster = arcpy.NumPyArrayToRaster(denMat[:,:,i],llCorner,25000)
    tmpRaster2 = arcpy.sa.SetNull(stepRaster,stepRaster,"VALUE = 0")
    arcpy.DefineProjection_management(tmpRaster2,srEASE)
    outName = os.path.join(outGDB,"day{}".format(i))
    tmpRaster2.save(outName)


