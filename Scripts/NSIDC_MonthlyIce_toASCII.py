# NSIDCMonthlyIcetoASCII.py
#
# Downloads raw U&V monthly icemotion BIN files from NSIDC ftp site and converts to ASCII file
#  for processing in E. Treml's circulation model.
#
# July 2016
# John.Fay@duke.edu

import sys, os, urllib
import numpy as np

#Path variables
scriptDir = os.path.dirname(sys.argv[0])
rootDir = os.path.dirname(scriptDir)
dataDir = os.path.join(rootDir,"Data")

#**Variables**
outFolder= os.path.join(dataDir,'NSIDC','ndisc0116_icemotion_vectors_v3','monthly_clim')

#URLs
monthlyURL = r'ftp://sidads.colorado.edu/pub/DATASETS/nsidc0116_icemotion_vectors_v3/data/north/monthly_clim/'
monthlyFile = 'icemotion.grid.monthlyclim.XX.n.v3.bin'

#Static variables
xDim = 361
yDim = 361
nGrids = 3
valSize = 16

#Loop through each month
for moNumber in range (1,13):
    #Convert the month number to a 2-character string
    mo = str(moNumber).zfill(2)
    
    #Set the ftp filename to download
    ftpFN = monthlyFile.replace("XX",mo)
    ftpURL = os.path.join(monthlyURL,ftpFN)
    
    #Create the save filename
    saveFN = os.path.join(outFolder,ftpFN)
    
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

    #Skip if already converted to ASCII
    if os.path.exists(outFN_u) and os.path.exists(outFN_v):
        print "ASCII files already exist. Skipping."
    else:
        #Convert to an array
        print "...Converting to array"
        arr = np.fromfile(saveFN, np.int16).reshape((xDim,yDim,nGrids))

        #Decompose to components
        arrU = arr[:,:,0]
        arrV = arr[:,:,1]
        arrMask = arr[:,:,2]

        #Convert mask to binary
        arrMask[arrMask > 0] = 1
        
        #Write the array to file
        print "...Saving as ASCII" 
        np.savetxt(outFN_u,arrU,fmt='%d')
        np.savetxt(outFN_v,arrV,fmt='%d')
        np.savetxt(outFN_m,arrMask,fmt='%d')
                




