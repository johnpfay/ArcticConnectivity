# ArcticConnectivity
<H2>Models to visualize connectivity in the Arctic Ocean</H2>

This ArcGIS workspace translates <A href="http://psc.apl.washington.edu/zhang/IDAO/model.html"> PIOMAS</a> ocean velocity data from the Polar Science Center into a set of matrices for us in Eric Treml's dispersal models. The <A href="http://psc.apl.washington.edu/zhang/IDAO/data_piomas.html">PIOMAS data</a> are distributed as annual binary matrix data with the matrix holding montly U and V circulation vectors at 10 depth levels over a set of coordinates crossing the Arctic region. 

The scripts in this workspace extract these coordinate data from their binary matrix files into ArcGIS point feature classes, projects them to the EASE Arctic coordinate system, and interpolates a 2500 x 2500 km raster surface of monthy U and V values spanning the Arctic Ocean. Only the surface layer (of the 10 depths available) was modeled. 

These interpolated rasters are then reformatted into stacks of ASCII files - one for each month of each year in the PIOMAS datasets (1978-2013) for use in Treml's models. We also create an ocean mask (ocean = 1, land/no data = 0), and a raster dataset of dispersal sources and sinks to use in modeling. The source/sink raster was created by isolating the line cells at the edge of the ocean and splitting them into roughly 500 km segments, each individually labelled. 
