#LLtoEASE.py
#
# Converts LatLong to EASE Coordinates
# Source: https://nsidc.org/data/ease/ease_grid.html
# Also: https://www.mathworks.com/help/map/ref/vec2mtx.html
#http://www.cesbio.ups-tlse.fr/SMOS_blog/wp-content/uploads/TOOLS/geo2easeGridV2.m

import math

#From Z_pts201201; record 9392
lat = 72.77
lng = 37.38
angle = 26.53
u = 2.96338
v = 3.2284

#EASE
lambda = math.radians(lng)  #Lng in radians
phi = math.radians(lat)     #Lat in radians
R = 6371.228                #Radius of the earth 
C = 2500                    #Cell size
r0 = 0                        #Map origin column
s0 = 0                       #Map origin row

r = 2*R/C * math.sin(lambda) * sin(math.pi/4 - phi/2) + r0 #Column coord
s = 2*R/C * math.cos(lambda) * sin(math.pi/4 - phi/2) + s0 #Row cord
h = math.cos(math.pi/4 - phi/2) # Particular scale along meridians (u?)
k = math.sec(math.pi/4 - phi/2) # Particular scale along parallels (v?)

#ZHANG
rot = 45 #Or 60?
re=6378.273		# Radius of earth (km)  -Hughes Ellipsoid
e2=0.006693883	# Eccentricity of earth -Hughes Ellipsoid
e=math.sqrt(e2)
slat=70.0       #Standard parallel

rho = math.sqrt(u**2 + v**2)
cm = math.cos(math.radians(slat))/math.sqrt(1.0 - e2*(math.sin(math.radians(slat))**2))
t = math.tan((math.pi)/4) - (slat/ math.degrees(2))