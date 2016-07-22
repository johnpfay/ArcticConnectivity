#PIOMAS_ReadGrid.py
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
# Output files are saved in the "Processed" folder
#
# July 2015
# John.Fay@duke.edu

debug = True
createASCII = False
writeRasters = True

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
extentFC = os.path.join(rootDir,"Data","General","MaskPoly.shp")
extentGrd = os.path.join(rootDir,"Data","General","StudyArea.img")
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

#Read the io.dat_360_120.output mask file into an array
with open(os.path.join(rawDir,'io.dat_360_120.output'),'rt') as grdFile:
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
for year in range(2013,2014):
    print "Processing data for {}".format(year)
    yearFN = os.path.join(rawDir,"uo1_10.H{}.gz".format(year))
    #Read the entire annual data (all levels) into array
    with gzip.open(yearFN,'rb') as grdFile:
        grdData = grdFile.read()
        flatArr = np.frombuffer(grdData,dtype=varType).reshape(-1,yDim,xDim)
        #This will be an array 240 x 360 x 120;
        # the 1st dimension is the Jan U vals; the 12th dimension is the V vals

    for month in range(12):
        strMonth = str(month+1).zfill(2)
        print "...processing month {}".format(strMonth)
        
        #Get the data for the current month
        ##There are 20 records for each month; the 1st 10 are u values for the 10 depths
        ##and the remaining 10 are v values for the 10 depths. We just one the 1st depth
        ##so we want 0,20,40,...,220 for u values and 10,30,50,...230 for v values. 
        sliceU = flatArr[month*20,:,:]
        sliceV = flatArr[month*20 + 10,:,:]
        
        #Create the output file
        outFN = "Pts{}{}.shp".format(year,strMonth)
        if arcpy.Exists(os.path.join(outDir,outFN)) and not debug:
            print "Already created, skipping."
            continue
        print "   ...Creating point file for month: {}".format(strMonth)
        
        #outFC = arcpy.CreateFeatureclass_management(outDir,outFN,"POINT",spatial_reference=srWGS84)
        outFC = arcpy.CreateFeatureclass_management("in_memory","tmp","POINT",spatial_reference=srWGS84)
        #Add fields
        print "   ...Adding fields"
        arcpy.AddField_management(outFC,"Angle","FLOAT",8,2)
        arcpy.AddField_management(outFC,"U","FLOAT",8,2)
        arcpy.AddField_management(outFC,"V","FLOAT",8,2)

        #Add features
        cursor = arcpy.da.InsertCursor(outFC,['SHAPE@XY','Angle','U','V'])
        for x in range(yDim):
            for y in range(xDim):
                theLat = latArr[x,y]
                theLng = lngArr[x,y]
                theAngle = anglArr[x,y]
                theU = sliceU[x,y]
                theV = sliceV[x,y]
                theRec = ((theLng,theLat),theAngle,theU,theV)
                cursor.insertRow(theRec)
        del cursor
        
        #Reproject to EASE grid
        print "   ...reprojecting to EASE projection"
        outFC2 = os.path.join(outDir,outFN)
        outFC2 = arcpy.Project_management(outFC,outFC2,srEASE)
    
        #Interpolate U and V values to raster
        print "   ...Interpolating to raster"
        #Create u and v rasters
        uBand = outSpline = arcpy.sa.Spline(outFC2,"U",25000, "REGULARIZED", 0.1)
        vBand = outSpline = arcpy.sa.Spline(outFC2,"V",25000, "REGULARIZED", 0.1)
        ##uBand = arcpy.sa.NaturalNeighbor(outFC2,"U",25000)
        ##vBand = arcpy.sa.NaturalNeighbor(outFC2,"V",25000)
        #Set zeros to NoData
        ##arcpy.env.mask = extentGrd
        ##uBand2 = arcpy.sa.SetNull(uBand,uBand,"Value = 0")
        ##vBand2 = arcpy.sa.SetNull(vBand,vBand,"Value = 0")
        #Remove data outside of mask
        uBand2 = arcpy.sa.ExtractByMask(uBand,maskRaster)
        vBand2 = arcpy.sa.ExtractByMask(vBand,maskRaster)
             
        #Convert to ASCII files
        if createASCII:
            print "    ...Saving as ASCII files"
            outUFN = os.path.join(outDir,"u{}{}.ASC".format(year,strMonth))
            outVFN = os.path.join(outDir,"v{}{}.ASC".format(year,strMonth))      
            uArr = arcpy.RasterToNumPyArray(uBand2,nodata_to_value=0)
            vArr = arcpy.RasterToNumPyArray(vBand2,nodata_to_value=0)
            np.savetxt(outUFN,uArr,fmt='%8.6f')
            np.savetxt(outVFN,vArr,fmt='%8.6f')
                       
        #Composite to output raster and set projection to EASE
        if writeRasters:
            outRaster = os.path.join(outDir,"uv{}{}.img".format(year,strMonth))
            arcpy.CompositeBands_management((uBand2,vBand2),outRaster)
            arcpy.DefineProjection_management(outRaster,srEASE)
        
        #Clean up
        arcpy.Delete_management(uBand)
        arcpy.Delete_management(vBand)
        arcpy.Delete_management(uBand2)
        arcpy.Delete_management(vBand2)