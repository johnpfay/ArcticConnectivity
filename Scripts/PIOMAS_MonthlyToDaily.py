#PIOMAS_MontlyToDaily.py
#
#Extrapolates a set of monthly averages to daily value


import sys, os, numpy as np

#Get folder locations, relative to this script (which should be in scripts folder)
scriptDir = os.path.dirname(sys.argv[0])
rootDir = os.path.dirname(scriptDir)
dataDir = os.path.join(rootDir,"Data","PolarScienceCenter","PIOMAS","Processed","ASCII")
dailyDir = os.path.join(dataDir,"Daily")
scratchDir = os.path.join(rootDir,"Scratch")
simDir = os.path.join(rootDir,"Scratch","SimDir")

#Days in month
dayDict = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

for mo in range(1,12):
    #Create month strings
    month0 = str(mo).zfill(2)
    month1 = str(mo+1).zfill(2)
    #Get days in month
    daysInMonth = dayDict[mo]
    #Create filenames
    fn0 = os.path.join(dataDir,"u2013{}.ASC".format(month0))
    fn1 = os.path.join(dataDir,"u2013{}.ASC".format(month1))
    #Read in monthly data as numpy arrays
    arr0 = np.loadtxt(fn0)
    arr1 = np.loadtxt(fn1)
    #Compute daily difference
    arrDiff = (arr1 - arr0) / daysInMonth

    for i in range(0,daysInMonth):
        dayNo = i + 15
        if daysInMonth - i >= 15 :
            dayNo = str(dayNo).zfill(2)
            outFN = os.path.join(dailyDir,"u2013{}{}.ASC".format(month0,dayNo))
        else:
            dayNo = str(dayNo - daysInMonth).zfill(2)
            outFN = os.path.join(dailyDir,"u2013{}{}.ASC".format(month1,dayNo))
        arrChange = i * arrDiff
        outArr = arr0 + arrChange
        print outFN, outArr[1,37]
        np.savetxt(outFN,outArr,fmt="%2.6f")


