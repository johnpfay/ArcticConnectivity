#PIOMAS_ReadGrid.py
import sys, os
import numpy as np
import arcpy

workDir = os.path.dirname(sys.argv[0])
outFile = os.path.join(workDir,"data.shp")

arcpy.CheckOutExtension('spatial')
arcpy.env.overwriteOutput = 1

arcpy.env.scratchWorkspace = workDir

xDim = 120
yDim = 360
varType = np.float32

#Read the grid
with open("grid.dat.pop",'rt') as grdFile:
    flatArr = np.loadtxt(grdFile).reshape(-1,360,120)

latArr = flatArr[0,:,:]
lngArr = flatArr[1,:,:]
HTNArr = flatArr[2,:,:] #Lenghts of sides of grid cell in KM (NESW)
HTEArr = flatArr[3,:,:]
HUSArr = flatArr[4,:,:]
HUWArr = flatArr[5,:,:]
anglArr = flatArr[6,:,:] #Angle

#Read the data
with open("uo1_10.H2013",'rb') as grdFile:
    flatArr = np.fromfile(grdFile,dtype=varType).reshape(-1,360,120)

year = 0
sliceU = flatArr[year,:,:]
sliceV = flatArr[year+12,:,:]

#Create the output file
outFC = arcpy.CreateFeatureclass_management(workDir,"data.shp","POINT")
#Add fields
arcpy.AddField_management(outFC,"Angle","FLOAT",8,2)
arcpy.AddField_management(outFC,"U","FLOAT",8,2)
arcpy.AddField_management(outFC,"V","FLOAT",8,2)

#Add features
cursor = arcpy.da.InsertCursor(outFC,['SHAPE@XY','Angle','U','V'])
for x in range(yDim):
    for y in range(xDim):
        theLat = latArr[x,y]
        theLng = lngArr[x,y]
        #if theLng > 180: theLng = (theLng-180)
        theAngle = anglArr[x,y]
        theU = sliceU[x,y]
        theV = sliceV[x,y]
        theRec = ((theLng,theLat),theAngle,theU,theV)
        cursor.insertRow(theRec)
del cursor

arcpy.DefineProjection_management(outFC,arcpy.SpatialReference(4326))

###------------------------------------------
sys.exit(0)
with open("io.dat_360_120.output","rt") as grdFile:
    lineStrings = grdFile.readlines()
maskArr = np.empty((360,120),dtype=np.int32)
x=0;y=0
for lineString in lineStrings:
    x = 0
    for i in range(0,720,2):
        idx = i /2
        maskArr[x,y] = lineString[idx:idx+2]
        x += 1
    y += 1
        
