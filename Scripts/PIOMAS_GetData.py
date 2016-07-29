#PIOMAS_GetData.py
#
# Downloads data from PIOMAS ftp site to RawData folder.
#
# July 2016
# John Fay

import sys, os, urllib

#URL info
theBaseURL = 'ftp://pscftp.apl.washington.edu/zhang/PIOMAS/data/v2.1/other/uo1_10.HYYYY.gz'
theUtilURL = 'ftp://pscftp.apl.washington.edu/zhang/PIOMAS/utilities/'

#Folder structure
scriptDir = os.path.dirname(sys.argv[0])
rootDir = os.path.dirname(scriptDir)
dataDir = os.path.join(rootDir,"Data")
polarDir = os.path.join(dataDir,"PolarScienceCenter")
piomasDir = os.path.join(polarDir,"PIOMAS")
rawDir = os.path.join(piomasDir,"RawData")

#Create folders if they don't exist
for theFldr in (polarDir,piomasDir,rawDir):
    if not os.path.exists(theFldr):
        print "Creating {}".format(theFldr)
        os.mkdir(theFldr)

#Download the utility files
theIODatURL = theUtilURL + "io.dat_360_120.output"
theIODatFN = os.path.join(rawDir,os.path.basename(theIODatURL))
if not os.path.exists(theIODatFN):
    print "Fetching {}".format(theIODatURL),
    response = urllib.urlretrieve(theIODatURL,theIODatFN)
    print "...Done!"
else:
    print "{} already nabbed".format(theIODatFN)
    
theGridDatPopURL = theUtilURL + "grid.dat.pop"
theGridDatPopFN = os.path.join(rawDir,os.path.basename(theGridDatPopURL))
if not os.path.exists(theGridDatPopFN):
    print "Fetching {}".format(theGridDatPopURL),
    response = urllib.urlretrieve(theGridDatPopURL,theGridDatPopFN)
    print "...Done!"
else:
    print "{} already nabbed".format(theGridDatPopFN)

#Download the yearly files
for year in range(1978,2014):
    #print "Grabbing file for year {}".format(year)
    theURL = theBaseURL.replace("YYYY",str(year))
    theOutFN = os.path.join(rawDir,os.path.basename(theURL))
    if not os.path.exists(theOutFN):
        print "Fetching {}".format(theURL),
        response = urllib.urlretrieve(theURL,theOutFN)
        print "...Done!"
    else:
        print "{} already downloaded; skipping".format(os.path.basename(theOutFN))