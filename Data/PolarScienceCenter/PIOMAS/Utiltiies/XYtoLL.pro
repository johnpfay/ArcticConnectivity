;
;  REVERSE OF ...
;  Polar stereo projection of lat,lon onto an x,y grid in kilometers
;  (From Fortran subroutine rmaps.f)
;
;  NSIDC SSMI grids rotated 45 deg in Arctic and 0 in Antarctic
;  Roger C's basin rotated 60 deg
;
;  Here we assume northern hemisphere!
;  This version allows
;  vector arguments for x and y, with vectors alat,alon returned.
;
PRO XYtoLL, x, y, alat, alon, rot

   nel = n_elements(x)
   alat = fltarr(nel)
   alon = fltarr(nel)
   tt = fltarr(nel)
   chi = fltarr(nel)

;  Definition of constants

        re=6378.273		; Radius of earth (km)  -Hughes Ellipsoid
        e2=DOUBLE(0.006693883)	; Eccentricity of earth -Hughes Ellipsoid
        e=sqrt(e2)
        slat=70.		; Standard parallel

;   rho is a vector
        rho = sqrt(x*x + y*y)
;   cm and t are scalars
        cm=COS(!DTOR*slat)/SQRT(1.-e2*(SIN(!DTOR*slat)^2))
        t=TAN((!DPI/4.)-(slat/(2.*!RADEG)))/         $
          ((1.-e*SIN(!DTOR*slat))/                   $
           (1.+e*SIN(!DTOR*slat)))^(e/2)
;   tt and chi are vectors
        tt=rho*t/(re*cm)
        chi=(!DPI/2.0)-2.0*ATAN(tt)

        alat = chi + ((e2/2)+(5*(e2^2)/24)+((e2^3)/12)) * SIN(2*chi) $
                      + ((7*(e2^2)/48)+(29*(e2^3)/240)) * SIN(4*chi) $
                                       + (7*(e2^3)/120) * SIN(6*chi)
        alat = alat * !RADEG
        alon = ATAN(x,-y)*!RADEG - rot
        neg = where(alon LE -180.)
        if min(neg) NE -1 then alon(neg) = alon(neg) + 360.

	RETURN
	END
