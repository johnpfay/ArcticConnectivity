#PIOMAS_Ice2Point.py
#
# Reads data in from two sets of files: grid.dat.pop and the monthly
#  sea ice velocity vectors (u,v) for years 1979-2013, and converts
#  these data into multipoint feature classes and then interpolated
#  (spline) raster datasets in the EASE projection.
#
# Data are from the Polar Science Center's PIOMAS project site 
#  (http://psc.apl.uw.edu/research/projects/arctic-sea-ice-volume-anomaly/data/model_grid)
#
# Inputs are the folder containing the grid.dat.pop file and the monthly ocean velocity
#  files for each year (uo1_10.H<yyyy>). These can be downloaded from:
#  ftp://pscftp.apl.washington.edu/zhang/PIOMAS/utilities/grid.dat.pop and
#  ftp://pscftp.apl.washington.edu/zhang/PIOMAS/data/v2.1/other/
#
# Output files are saved in the "Processed" folder and are constrained to the extent
#  of the PIOMAS_Mask.img raster dataset, which was created by creating a 1-NoData mask
#  from values in a fully interpolated output clipped to the extent of the MaskPoly.shp
#  feature class.
#
# July 2015
# John.Fay@duke.edu

import sys, os, gzip, arcpy, math
import numpy as np
import pandas as pd

#Define ll2xy function
def ll2xy(alat,alng):
    '''convert tuples of latitude and longitudes into X and Y
    re = 6378.273       #Radius of the earth
    e2 = 0.006693883    #Eccentricity of earth -Hughes ellipsoide
    e = math.sqrt(e2)
    sLat = 70.0         #Standard parallel
    XP = (
    t0 = math.tan((math.pi/4.0) - alat/(math.degrees(2))'''

#Set output options
createASCII = False
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
rasterDir = os.path.join(dataDir,"Processed","Raster")                  #To hold output raster files
ASCIIDir = os.path.join(dataDir,"Processed","ASCII")                    #To hold output ASCII u and v files (monthly)

##Create output folders, if not present
for theDir in (outDir,pointFCDir,rasterDir,ASCIIDir):
    if not os.path.exists(theDir):
        print "Creating {}".format(theDir)
        os.mkdir(theDir)

##Create scratch file geodatabase, if not present
if not os.path.exists(scratchDir):
    arcpy.CreateFileGDB_management(os.path.dirname(scratchDir),"Scratch.gdb")

#Get extent feature class and raster
maskRaster = os.path.join(rootDir,"Data","General","PIOMAS_Mask.img")
arcpy.env.snapRaster = maskRaster

#ArcPy setup
arcpy.CheckOutExtension('spatial')
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

#Loop through years
for year in range(2004,2005):
    print "Processing data for {}".format(year)
    yearFN = os.path.join(rawDir,"icevel.H{}.gz".format(year))
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
        ##There are 2 records for each month; the 1st 10 are u values for the 10 depths
        ##and the remaining 10 are v values for the 10 depths. We just one the 1st depth
        ##so we want 0,20,40,...,220 for u values and 10,30,50,...230 for v values. 
        sliceU = flatArr[month * 2,:,:]
        sliceV = flatArr[month * 2 + 1,:,:]
        
        #Create the output point file
        outFN = "IceVel_Pts{}{}.shp".format(year,strMonth)
        outFC2 = os.path.join(outDir,"PointFeatures",outFN)
        if arcpy.Exists(os.path.join(outDir,outFC2)):
            print "Already created, skipping."
            #continue
        print "   ...Creating point file for month: {}".format(strMonth)
        outFC = arcpy.CreateFeatureclass_management("in_memory","tmp","POLYLINE",spatial_reference=srWGS84)
        
        #Add fields
        print "   ...Adding fields"
        arcpy.AddField_management(outFC,"Lat","FLOAT",10,8)
        arcpy.AddField_management(outFC,"Lng","FLOAT",10,8)
        arcpy.AddField_management(outFC,"Angle","FLOAT",8,2)
        arcpy.AddField_management(outFC,"U","FLOAT",8,2)
        arcpy.AddField_management(outFC,"V","FLOAT",8,2)
        arcpy.AddField_management(outFC,"Mag","FLOAT",8,2)
        arcpy.AddField_management(outFC,"Bearing_1","FLOAT",8,2) #Computed from U/V
        arcpy.AddField_management(outFC,"Bearing_2","FLOAT",8,2) #Adjusted by addng angle
        arcpy.AddField_management(outFC,"U1","FLOAT",8,2)
        arcpy.AddField_management(outFC,"V1","FLOAT",8,2)
        
        #Loop through each data point and add ad features to the output feature class
        cursor = arcpy.da.InsertCursor(outFC,['SHAPE@','Lng','Lat','Angle','U','V','Mag','Bearing_1','Bearing_2','U1','V1'])
        for x in range(yDim):
            for y in range(xDim):
                theLat = latArr[x,y]
                theLng = lngArr[x,y]
                theAngle = anglArr[x,y]
                theU = sliceU[x,y]
                theV = sliceV[x,y]
                if theU == 0 and theV == 0: continue
                #Compute the bearings (in degrees) in GOCC from U and V 
                bearing1 = math.degrees(math.atan2(theV,theU)) 
                bearing2 = bearing1 + theAngle
                #Compute the magnitude
                magnitude = math.sqrt(theU**2 + theV**2)
                #Decompose bearing 2 back into U and V
                U1 = math.sin(math.radians(bearing2))*magnitude
                V1 = math.cos(math.radians(bearing2))*magnitude
                #From Zhang's script ###SAME AS ATAN2(v,u)###
                alpha = -1.0 * math.radians(theAngle)
                vec0 = theU * math.cos(alpha) + theV * math.sin(alpha)
                vec1 = theV * math.cos(alpha) - theU * math.sin(alpha)
                #From Zhang's script, lines 189
                scale = 3.0*40.0*1000.0*25.0
                xhead = theLng+U1/637000.0/math.cos(theLat/57.29578*scale)
                yhead = theLat+V1/637000.0*scale
                if yhead > 90:
                    yhead = 90 - (yhead - 90)
                    xhead = xhead + 180
                #Create line from theLng,theLat to xhead,yhead
                lineArr=arcpy.Array([arcpy.Point(theLng,theLat),arcpy.Point(xhead,yhead)])
                theLine = arcpy.Polyline(lineArr)
                #Write values to the table and insert the row
                #theRec = ((theLng,theLat),theLng,theLat,theAngle,theU,theV,bearing1,bearing2,xhead,yhead)
                theRec = (theLine,theLng,theLat,theAngle,theU,theV,magnitude,bearing1,bearing2,U1,V1)
                cursor.insertRow(theRec)
        del cursor

        #Save the raster
        print "   ...Saving raster"
        outFC2 = arcpy.CopyFeatures_management(outFC, outFC2)

        #DEBUG EXIT
        sys.exit(0)
        
        #Reproject to EASE grid
        print "   ...reprojecting to EASE projection"
        outFC2 = arcpy.Project_management(outFC,outFC2,srEASE)
    
        #Interpolate U and V values to raster
        print "   ...Interpolating to raster"
        #Create u and v rasters via Spline method
        uBand = outSpline = arcpy.sa.Spline(outFC2,"U",25000, "REGULARIZED", 0.1)
        vBand = outSpline = arcpy.sa.Spline(outFC2,"V",25000, "REGULARIZED", 0.1)

        #Remove data outside of mask
        uBand2 = arcpy.sa.ExtractByMask(uBand,maskRaster)
        vBand2 = arcpy.sa.ExtractByMask(vBand,maskRaster)
             
        #Convert to ASCII files
        if createASCII:
            print "    ...Saving as ASCII files"
            outUFN = os.path.join(outDir,"ASCII","us_{}_{}.ASC".format(year,strMonth))
            outVFN = os.path.join(outDir,"ASCII","vs_{}_{}.ASC".format(year,strMonth))      
            uArr = arcpy.RasterToNumPyArray(uBand2,nodata_to_value=0)
            vArr = arcpy.RasterToNumPyArray(vBand2,nodata_to_value=0)
            np.savetxt(outUFN,uArr,fmt='%8.6f')
            np.savetxt(outVFN,vArr,fmt='%8.6f')
                       
        #Composite to output raster and set projection to EASE
        if writeRasters:
            outRaster = os.path.join(outDir,"uv_{}_{}.img".format(year,strMonth))
            arcpy.CompositeBands_management((uBand2,vBand2),outRaster)
            arcpy.DefineProjection_management(outRaster,srEASE)
        
        #Clean up
        arcpy.Delete_management(uBand)
        arcpy.Delete_management(vBand)
        arcpy.Delete_management(uBand2)
        arcpy.Delete_management(vBand2)