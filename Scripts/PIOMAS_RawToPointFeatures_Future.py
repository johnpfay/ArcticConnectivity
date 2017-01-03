#PIOMAS_RawToPointFeatures_Future.py
#
# Reads data in from two sets of files: grid.dat.pop and the monthly
#  sea ice velocity vectors (u,v) for years 2017-2051, and converts
#  these data into multipoint feature classes in the EASE projection.
#
# Data are from the Polar Science Center's IDAO project site 
#  (ftp://pscftp.apl.washington.edu/zhang/IDAO/future_projection, )
#
# Inputs are the folder containing the grid.dat.pop file and the monthly ocean velocity
#  files for each year (uo.H<yyyy>). These can be downloaded from:
#  ftp://pscftp.apl.washington.edu/zhang/PIOMAS/utilities/grid.dat.pop and
#  ftp://pscftp.apl.washington.edu/zhang/PIOMAS/data/v2.1/other/
#
# Output files are saved in the "Processed" folder 
#
# January 2017
# John.Fay@duke.edu

import sys, os, gzip, arcpy
import numpy as np

#Set output options
startYear = 2017
endYear = 2051
createASCII = True
writeRasters = False

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

##Create output folders, if not present
for theDir in (outDir,pointFCDir):
    if not os.path.exists(theDir):
        print "Creating {}".format(theDir)
        os.mkdir(theDir)

##Create scratch file geodatabase, if not present
if not os.path.exists(scratchDir):
    arcpy.CreateFileGDB_management(os.path.dirname(scratchDir),"Scratch.gdb")

#ArcPy setup
arcpy.env.overwriteOutput = True
arcpy.env.scratchWorkspace = scratchDir
srWGS84 = arcpy.SpatialReference(4326)#WGS 84
srEASE = arcpy.SpatialReference(3408) #NSIDC_EASE_Grid_North

#Setup for PIOMAS data
xDim = 120
yDim = 360
varType = np.float32

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

#Read in EASE correction values
easeCSV = os.path.join(rawDir,'EASEcorrection.csv')
easeArr = np.loadtxt(easeCSV).reshape(yDim,xDim)

#Loop through years
for year in range(startYear,endYear):
    print "Processing data for {}".format(year)
    yearFN = os.path.join(rawDir,"uo.H{}.gz".format(year))
    #Read the entire annual data (all levels) into array
    with gzip.open(yearFN,'rb') as grdFile:
        grdData = grdFile.read()
        flatArr = np.frombuffer(grdData,dtype=varType).reshape(-1,yDim,xDim)
        ## This will be an array 240 x 360 x 120;
        ## the 1st dimension is further subset into: Month/Depth Level/U-V slices

    #Loop through the 12 months of data in the yearly data file
    for month in range(12):
        strMonth = str(month+1).zfill(2)
        print "...processing month {}".format(strMonth)
        
        #Get the data for the current month
        ##There are 60 records for each month; the 1st 30 are u values for the 30 depths
        ##and the remaining 30 are v values for the 30 depths. We just one the 1st depth
        ##so we want 0,60,120,...,660 for u values and 30,90,150,...690 for v values. 
        sliceU = flatArr[month*60,:,:]
        sliceV = flatArr[month*60 + 30,:,:]
        
        #Create the output point file
        outFN = "FPts{}{}.shp".format(year,strMonth)
        outFC2 = os.path.join(outDir,"PointFeatures",outFN)
        if arcpy.Exists(os.path.join(outDir,outFC2)):
            print "Already created, skipping."
            #continue
        print "   ...Creating point file for month: {}".format(strMonth)
        outFC = arcpy.CreateFeatureclass_management("in_memory","tmp","POINT",spatial_reference=srWGS84)
        
        #Add fields
        print "   ...Adding fields"
        arcpy.AddField_management(outFC,"Lat","FLOAT",10,8)
        arcpy.AddField_management(outFC,"Lng","FLOAT",10,8)
        arcpy.AddField_management(outFC,"Angle","FLOAT",8,2)
        arcpy.AddField_management(outFC,"U","FLOAT",8,2)            #Native U value (GOCC)
        arcpy.AddField_management(outFC,"V","FLOAT",8,2)            #Native V value (GOCC)
        arcpy.AddField_management(outFC,"NearAngle","FLOAT",8,2)    #Near angle between PIOMAS point and GOCC center
        arcpy.AddField_management(outFC,"NAT_Dir","FLOAT",8,2)      #Bearing based on Zhangs U/V
        arcpy.AddField_management(outFC,"NAT_Mag","FLOAT",8,2)      #Magnitude based on Zhangs U/V
        arcpy.AddField_management(outFC,"EASE_Dir","FLOAT",8,2)     #Adjusted bearing (EASE)
        arcpy.AddField_management(outFC,"EASE_U","FLOAT",8,2)           #Adjusted U (EASE)
        arcpy.AddField_management(outFC,"EASE_V","FLOAT",8,2)           #Adjusted V (EASE)

        #Loop through each data point and add ad features to the output feature class
        cursor = arcpy.da.InsertCursor(outFC,['SHAPE@XY','Lat','Lng','Angle','NearAngle','U','V',
                                              "NAT_Dir","NAT_Mag","EASE_Dir","EASE_U","EASE_V"])
        for x in range(yDim):
            for y in range(xDim):
                theLat = latArr[x,y]
                theLng = lngArr[x,y]
                theAngle = anglArr[x,y]
                U = sliceU[x,y] 
                V = sliceV[x,y]
                nearAngle = easeArr[x,y]    #Angle from EASRCorrection.csv
                
                #If the U and V are both zero, do not add the point
                if U == 0 and V == 0: continue
                
                #Compute the bearings (in degrees) in GOCC from U and V 
                NAT_DIR = math.degrees(math.atan2(V,U)) 
                EASE_DIR = NAT_DIR - 90 + nearAngle
                
                #Compute the magnitude (Pythagorean theorem)
                magnitude = math.sqrt(U**2 + V**2)
                
                #Decompose bearing 2 back into U and V
                EASE_U = math.cos(math.radians(EASE_DIR))*magnitude
                EASE_V = math.sin(math.radians(EASE_DIR))*magnitude
                
                #Write values to the table and insert the row
                theRec = ((theLng,theLat),theLat,theLng,theAngle,nearAngle,U,V,
                          NAT_DIR,magnitude,EASE_DIR,EASE_U,EASE_V)
                cursor.insertRow(theRec)

        del cursor
        
        #Reproject to EASE grid
        #print "   ...reprojecting to EASE projection"
        #outFC2 = arcpy.Project_management(outFC,outFC2,srEASE)
        outFC2 = arcpy.CopyFeatures_management(outFC,outFC2)


        
        