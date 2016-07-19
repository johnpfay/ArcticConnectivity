#WindToArray.py
#
# Pulls daily wind data from:
# ftp://sidads.colorado.edu/pub/DATASETS/nsidc0116_icemotion_vectors_v3/data/north/wind/
# and reformats it into a 1805 x 1805 array for processing with Treml's circulation models.
#
# July 2016
# John.Fay@duke.edu

import sys, os, urllib
import numpy as np
import arcpy

#Folder structure
scriptDir = os.path.dirname(sys.argv[0])
rootDir = os.path.dirname(scriptDir)
dataDir = os.path.join(rootDir,"Data")
scratchDir = os.path.join(rootDir,"Scratch")
scratchGDB = os.path.join(scratchDir,"Scratch.gdb")

#File specs
lowerleft = arcpy.Point(-4493750,-4493750)

#Arcpy environment settings
arcpy.CheckOutExtension('spatial')
arcpy.env.overwriteOutput = 1
arcpy.env.scratchWorkspace = scratchDir
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3408) #NSIDC_EASE_Grid_North 

#Storage location
theRootFldr = os.path.join(dataDir,"NSIDC","ndisc0116_icemotion_vectors_v3","wind")

#Data vars (replace XX with month to get the monthly file...)
theURL = 'ftp://sidads.colorado.edu/pub/DATASETS/nsidc0116_icemotion_vectors_v3/data/north/wind/'
theFileName = 'icemotion.vect.wind.{}{}.n.v3.txt' #YYYY=year;DD=day

#Set the year, month, and filename
year = str(2014)

#Create the year folder, if not there already
outYearFolder = os.path.join(theRootFldr,year)
if not os.path.exists(outYearFolder):
    print "Creating output folder for {}".format(year)
    os.mkdir(outYearFolder)
        
day = "100"

#Retrieve the data, if not there already

for dayNumber in range (100,101):
    #Convert the month number to a 2-character string
    day = str(dayNumber).zfill(3)
    
    #Set the ftp filename to download
    ftpFN = theFileName.format(year,day)
    ftpURL = "{}/{}/{}".format(theURL,year,ftpFN)
    
    #Create the save filename
    saveFN = os.path.join(outYearFolder,ftpFN)
    
    #Create the output filename (replace extension with ASC)
    outFN_u = saveFN[:-3] + "_u.asc"
    outFN_v = saveFN[:-3] + "_v.asc"
    outFN_m = saveFN[:-3] + "_mask.asc"
    
    #Skip if file has already been downloaded
    if os.path.exists(saveFN):
        print "{} already downloaded. Skipping.".format(ftpFN)
        
    else:
        #Fetch the file
        print "Fetching {}".format(ftpFN)
        response = urllib.urlretrieve(ftpURL,saveFN)
        print "...successfully downloaded"

#Read in the ftpFile as array, skipping the first line
arr = np.genfromtxt(saveFN,skip_header=1)
xVals = arr[:,1].astype(np.int16) #x/y seems backwards, but it works.
yVals = arr[:,0].astype(np.int16)

#Create empty 2D arrays
uArr = np.nan * np.empty((1805,1805))
vArr = np.nan * np.empty((1805,1805))

#Fill values with data in columns
uArr[xVals,yVals] = arr[:,2]
vArr[xVals,yVals] = arr[:,3]

#Create rasters
outName = os.path.join(scratchGDB,"wind{}{}".format(year,day))
if arcpy.Exists(outName) and 1 == 0:
    print "{} raster exists; skipping.".format("wind{}{}.img".format(year,day))
else:
    uBand = arcpy.NumPyArrayToRaster(uArr,lowerleft,5000,5000,0)
    vBand = arcpy.NumPyArrayToRaster(vArr,lowerleft,5000,5000,0)
    #uBand.save("uVals")
    #vBand.save("vVals")
    arcpy.CompositeBands_management((uBand,vBand),outName)
    arcpy.Delete_management(uBand)
    arcpy.Delete_management(vBand)
        

        


