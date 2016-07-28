Files included here: 


**General folder**
PIOMAS_Mask.*
	IMG format raster showing areas included in the arctic circulation data. This is a 235 x 253 raster dataset projected to the NSIDC EASE Grid North (http://spatialreference.org/ref/epsg/3408/) with a cell size of 25km and a lower left coordinate of (-3567696.94076, -2743739.54274). Values of 1 indicate ocean areas where circulation data exist; all other cells are coded as NoData.
	
Pts201312.shp
	Multipoint feature class (shapefile) containing PIOMAS circulation data locations with u and v data for December 2013. THe point features were build from raw PIOMAS data files in geographic coordinates and then projected to the NSIDC EASE Grid North coordinate system. Spline interpolation on these data were used to derive the monthly U and V rasters. 

**PolarScienCecenter/PIOMAS folder/RawData**
	Unprocessed files from PIOMAS download site

**PolarScienCecenter/PIOMAS folder/Processed/ASCII**
	Interpolated ASCII matrices of u and v vector values for each month from 1978 to 2013

**PolarScienCecenter/PIOMAS folder/Processed/PointFeatures**
	Point features extracted from PIOMAS data files

**PolarScienCecenter/PIOMAS folder/Processed/Rasters**
	Select raster (img format) of interpolated U and V vector values for each month

**Sim dir**
uAtSurface, vAtSurface
	Zipped folder of monthly u-v data for the years 1978-2013 in raw ASCII format. Each ACSII file is a 235 x 253 matrix of values aligned to the cells in the PIOMAS_Mask.img data file (columns are data in the X direction, rows in the Y direction, with the top left value in the ACSII matrix corresponding to the upper left XY coordinate)
	
MASK.ASC
	ASCII format water mask matrix containing 1s and 0s (1=water; 0=land or areas with no data). As above, this is a 235 x 253 matrix of values with the top left value corresponding to the upper left XY coordinate. 
	
ReefIDs.ASC
	ASCII format matrix of "reef" IDs, that is, unique values for 500 km segments lining coastal areas within the modeled portion of the Arctic ocean. As above, this is a 235 x 253 matrix. 
	
ReefProps.ASC
	ASCII format matrix of "reef" proportions, set to 1 for all "reef" cells identified in the ReefIDs.ASC file above. Same 235 x 253 size and format.  
	

**SimDir/GISFiles folder**
Segments500.img
	IMG format raster of 500km segments along the coast of the arctic oceans. Source of the ReefsIDs.ASC and ReefProps.ASC files.
	
Segments500FC.shp
	Polyline shapefile of the 500m segments.