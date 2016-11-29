#PIOMAS_CreateAngleAdjust.py
#
# Creates a csv file of of GOCC to EASE correction angles for each PIOMAS point
#
# Converts the PIOMAS grid.dat.pop data into a point feature class with lat,long,
#  and angle attributes. Then computes the near angle of these point features to
#  the center of the PIOMAS GOCC coordinate system. These near angles are saved
#  as a CSV file that can be used to correct angles in later scripts. 
#
# November 2015
# John.Fay@duke.edu

import sys, os, arcpy
import numpy as np

#Get folder locations, relative to this script (which should be in scripts folder)
##Input folders
scriptDir = os.path.dirname(sys.argv[0])                                #Folder containing this script
rootDir = os.path.dirname(scriptDir)                                    #Folder containing Scripts folder
dataDir = os.path.join(rootDir,"Data","PolarScienceCenter","PIOMAS")    #Root folder for PIOMAS data folders (in and out)
rawDir = os.path.join(dataDir,"RawData")                                #contains raw PIOMAS files

##Output folders
scratchDir = os.path.join(rootDir,"Scratch","Scratch.gdb")              #To hold scratch/temporary files
rawDir = os.path.join(dataDir,"RawData")                                #Folder containing raw PIOMAS files
outDir = os.path.join(dataDir,"Processed")
pointFCDir = os.path.join(dataDir,"Processed","PointFeatures")          #To hold output point files

##Input center of GOCC (in EASE coord sys)
#centerPt = os.path.join(dataDir,'GOCC_Center_EASEprj.shp')
centerPt = r'C:\Workspace\Gits\ArcticConnectivity\Data\EASE_Rotation\PIOMAS_Center.shp'

##Output file
convertToGeom = False
outCSV = os.path.join(rawDir,"EASEcorrection2.csv")

#ArcPy setup
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = scratchDir
srWGS84 = arcpy.SpatialReference(4326)#WGS 84
srEASE = arcpy.SpatialReference(3408) #NSIDC_EASE_Grid_North

#Setup for PIOMAS data
xDim = 120
yDim = 360
varType = np.float32

#Function to convert arithmetic angle to geographic angle
def CalcGeographicAngle(arith):
    if (arith >90 and arith <360):
        return (360-arith+90)
    elif (arith>=0 and arith <= 90):
        return (arith*(-1)+90)

#Read the grid.dat.pro data containing lat,long, and angle data
with open(os.path.join(rawDir,"grid.dat.pop"),'r') as grdFile:
    print "Reading in grid.data.pop data"
    flatArr = np.loadtxt(grdFile).reshape(-1,yDim,xDim)

#Slice into component arrays
print "Slicing data into lat/long/angle arrays"
latArr = flatArr[0,:,:]
lngArr = flatArr[1,:,:]
##HTNArr = flatArr[2,:,:] #Lengths of sides of grid cell in KM (NESW)- NOT USED
##HTEArr = flatArr[3,:,:]
##HUSArr = flatArr[4,:,:]
##HUWArr = flatArr[5,:,:]
anglArr = flatArr[6,:,:] #Angle

#Create a feature class of points
print "Constructing temporary feature class"
outFC = arcpy.CreateFeatureclass_management(scratchDir,"GOCCpts","POINT",spatial_reference=srWGS84)

#Add fields
arcpy.AddField_management(outFC,"Lat","FLOAT",10,8)
arcpy.AddField_management(outFC,"Lng","FLOAT",10,8)


#Loop through each data point and add ad features to the output feature class
print  "...adding features"
cursor = arcpy.da.InsertCursor(outFC,['SHAPE@XY','Lat','Lng'])
for x in range(yDim):
    for y in range(xDim):
        theLat = latArr[x,y]
        theLng = lngArr[x,y]
                    
        #Write values to the table and insert the row
        theRec = ((theLng,theLat),theLat,theLng)
        cursor.insertRow(theRec)
del cursor

#Compute near angles to center point
print "Computing near angles"
nearOut = arcpy.Near_analysis(outFC,centerPt,"","NO_LOCATION","ANGLE","PLANAR")

#Save as a csv file
print "Writing values to %s" %outCSV 
outFile = open(outCSV,'w')
with arcpy.da.SearchCursor(nearOut,"NEAR_ANGLE") as cursor:
    for rec in cursor:
        if convertToGeom:
            outAngle = CalcGeographicAngle(rec[0])
            outFile.write("%s\n" %outAngle)
        else:
            outFile.write("%s\n" %rec[0])

#Close the csv file
outFile.close()

#Delete the outFC
arcpy.Delete_management(outFC)

