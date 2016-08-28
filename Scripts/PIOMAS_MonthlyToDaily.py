#PIOMAS_MontlyToDaily.py
#
# Extrapolates daily time step data from each monthly ASCII file for a given year.
# Results are sent to the simDir folder (set within the project's Data folder).
#
#July 2015
#John.Fay@duke.edu

import sys, os, numpy as np

#Get folder locations, relative to this script (which should be in scripts folder)
scriptDir = os.path.dirname(sys.argv[0])
rootDir = os.path.dirname(scriptDir)
dataDir = os.path.join(rootDir,"Data","PolarScienceCenter","PIOMAS","Processed","ASCII")
simDir = os.path.join(rootDir,"Data","SimDir")
scratchDir = os.path.join(rootDir,"Scratch")

#Ensure the output folders exist in the SimDir folder
for theFldr in ('uAtSurface','vAtSurface','uAtDepth','vAtDepth'):
    theFldrName = os.path.join(simDir,theFldr)
    if not os.path.exists(theFldrName):
        print "Creating {}".format(theFldrName)
        os.mkdir(theFldrName)

#Days in month
dayDict = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

#Loop through each year
for year in range(1978,2014):
    print "Processing year: {}".format(year)
    #Look through each month
    for mo in range(1,13):
        #Create month strings, padded to two characters (e.g. "01")
        month0 = str(mo).zfill(2)
        month1 = str(mo+1).zfill(2)
        #Fix if month 13 (Jan of following year)
        #if month1 == '13':
        #    month1 = '01'
        #    year += 1
        #Get days in month from the dictionary
        daysInMonth = dayDict[mo]
        #If feb in a leap year, set days to 29
        if (year % 4 == 0) and (mo == 2): daysInMonth = 29
        print "[Year: {}]...processing month {} to {}".format(year,month0,month1)
        ##--PROCESS U VECTORS---
        for direction in ("u","v"):
            print "   ...processing {} vectors".format(direction)
            #Create filenames for the current month (T0) and the following month (T1)
            if mo == 1: #If January, set T0 to the previous year's December month
                if year == 1978: continue #Skip; don't have December 1986 data
                fn0 =os.path.join(dataDir,"{}s_{}_12.ASC".format(direction,year-1,12))
                fn1 =os.path.join(dataDir,"{}s_{}_01.ASC".format(direction,year,12))
            elif mo == 12: #If December, set the T1 to the next year's January
                if year == 2013: continue #Skip: don't have Jan 2014 data
                fn0 =os.path.join(dataDir,"{}s_{}_12.ASC".format(direction,year,12))
                fn1 =os.path.join(dataDir,"{}s_{}_01.ASC".format(direction,year+1,"01"))
            else:
                fn0 = os.path.join(dataDir,"{}s_{}_{}.ASC".format(direction,year,month0)) #Current month
                fn1 = os.path.join(dataDir,"{}s_{}_{}.ASC".format(direction,year,month1)) #Next month
                
            #Read in monthly data as numpy arrays
            arr0 = np.loadtxt(fn0)
            arr1 = np.loadtxt(fn1)
            
            #Compute daily difference
            arrDiff = (arr1 - arr0) / float(daysInMonth)

            for i in range(0,daysInMonth):
                dayNo = i + 15
                if daysInMonth - i >= 15 :
                    dayNo = str(dayNo).zfill(2)
                    outFN = os.path.join(simDir,"{}AtSurface".format(direction),"{}s_{}_{}_{}_120000.ASC".format(direction,year,month0,dayNo))
                else:
                    dayNo = str(dayNo - daysInMonth).zfill(2)
                    if month1 <> '13':
                        outFN = os.path.join(simDir,"{}AtSurface".format(direction),"{}s_{}_{}_{}_120000.ASC".format(direction,year,month1,dayNo))
                    else:
                        outFN = os.path.join(simDir,"{}AtSurface".format(direction),"{}s_{}_{}_{}_120000.ASC".format(direction,year+1,"01",dayNo))
                arrChange = i * arrDiff
                outArr = arr0 + arrChange
                np.savetxt(outFN,outArr,fmt="%2.6f")

