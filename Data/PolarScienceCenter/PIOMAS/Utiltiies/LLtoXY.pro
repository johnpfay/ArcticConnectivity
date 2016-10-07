;
;  Polar stereo projection of lat,lon onto an x,y grid in kilometers
;  (From Fortran subroutine rmaps.f)
;
;  NSIDC SSMI grids rotated 45 deg in Arctic and 0 in Antarctic
;  Roger C's basin rotated 60 deg
;
;  Here we assume northern hemisphere!
;  This version (Harry's edit of Erika's wave version) allows
;  vector arguments for lat and lon, with vectors x,y returned.
;
PRO LLtoXY, alat, alon, x, y, rot

   nel = n_elements(alat)
   x = fltarr(nel)
   y = fltarr(nel)
   t0 = fltarr(nel)
   rho = fltarr(nel)
   NP = lonarr(nel)
   XP = lonarr(nel)

;  Definition of constants

        re=6378.273		; Radius of earth (km)  -Hughes Ellipsoid
        e2=DOUBLE(0.006693883)	; Eccentricity of earth -Hughes Ellipsoid
        e=sqrt(e2)
        slat=70.		; Standard parallel

        NP = where(alat GE 89.995)
        XP = where(alat LT 89.995)

        if min(XP) NE -1 then begin   ; some points are below 89.995

;          t0 is a vector because alat is a vector
           t0(XP)=TAN((!DPI/4.)-(alat(XP)/(2.*!RADEG)))/     $
                  ((1.-e*SIN(!DTOR*alat(XP)))/               $
                   (1.+e*SIN(!DTOR*alat(XP))))^(e/2)
;          t1 is a scalar because slat is a scalar
           t1=    TAN((!DPI/4.)-(slat/(2.*!RADEG)))/         $
                  ((1.-e*SIN(!DTOR*slat))/                   $
                   (1.+e*SIN(!DTOR*slat)))^(e/2)
           cm=COS(!DTOR*slat)/SQRT(1.-e2*(SIN(!DTOR*slat)^2))
           rho(XP)=re*cm*t0(XP)/t1

           x(XP) =  rho(XP)*SIN(!DTOR*(alon(XP)+rot))
           y(XP) = -rho(XP)*COS(!DTOR*(alon(XP)+rot))

        endif

        if min(NP) NE -1 then begin   ; some points are above 89.995
           x(NP) = replicate(0.0, n_elements(NP))
           y(NP) = replicate(0.0, n_elements(NP))
        endif

	RETURN
	END
