Script descriptions (see script itself for more detail). Descriptions are written in the order in which the scripts should be executed. 

# PIOMAS_GetData.py #
	This script creates the PolarScienceCenter folders in the Data folders (if they don't already exist) and then downloads the datafiles required for the analysis. 

# PIOMAS_RawToASCII.py #
	This script processes the raw PIOMAS ocean velocity data, which should be located in the Data/PolarScienceCenter/PIOMAS/RawData, into point feature classes containing U and V vector values, and ASCII matrices of U and V vectors interpolated from these points.
	
# PIOMAS_WriteMatFiles.py #
	This script creates ASCII matrices representing the water mask, reefIDs, and reefProportions. 
	
# PIOMAS_MonthlyToDaily.py #
	This script interpolates daily timestep U and V matrices from the monthly values derived from the PIOMAS data. 
	
After these three scripts have been executed, all the data required to run the simulations should be available in the SimDir folder. 

July 2016
John.Fay@duke.edu