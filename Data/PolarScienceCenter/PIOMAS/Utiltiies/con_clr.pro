;This procedure generates a color table for contour plots
;written by Jinlun Zhang, PSC/APL/UW

pro con_clr,nconts,r,g,b,white, black, brown, blue

rgbv = intarr(3,253)
kclrs= intarr(253)
i=0
for hue=270.0, 0.0, -1.2529644 do begin
	if(i le 216) then begin
	color_convert, hue, 1.0, 1.0, rgbv0, rgbv1, rgbv2, /hsv_rgb
	rgbv(0,i)=rgbv0
	rgbv(1,i)=rgbv1
	rgbv(2,i)=rgbv2
	endif
	i=i+1
endfor
for hue=360.0, 314.0, -1.25229644 do begin
	if(i le 252) then begin
	color_convert, hue, 1.0, 1.0, rgbv0, rgbv1, rgbv2, /hsv_rgb
	rgbv(0,i)=rgbv0
	rgbv(1,i)=rgbv1
	rgbv(2,i)=rgbv2
	endif
	i=i+1
endfor

ndisti = nconts-1
intinc = 251/ndisti
;print, intinc
kclrs(0) = 0
i = 0
for m = 1, ndisti do begin
	 i = i+intinc
	 kclrs(m) = i
;	 print, kclrs(m)
	 endfor
	  r=intarr(nconts+3)
	  g=intarr(nconts+3)
	  b=intarr(nconts+3)
	  for m = 0, ndisti do begin
	  r(m)=rgbv(0,kclrs(m))
	  g(m)=rgbv(1,kclrs(m))
	  b(m)=rgbv(2,kclrs(m))
	  endfor

	  r(nconts)=0
	  r(nconts+1)=255
;	  r(nconts+2)=fix(255*0.9)
;	  r(nconts+2)=fix(255*0.8)
	  r(nconts+2)=fix(255*0.7)
	  g(nconts)=0
	  g(nconts+1)=255
;	  g(nconts+2)=fix(255*0.9)
;	  g(nconts+2)=fix(255*0.8)
	  g(nconts+2)=fix(255*0.7)
	  b(nconts)=0
	  b(nconts+1)=255
;	  b(nconts+2)=fix(255*0.9)
;	  b(nconts+2)=fix(255*0.8)
	  b(nconts+2)=fix(255*0.7)
	  tvlct, r, g, b
          black=nconts & white=nconts+1 & brown=nconts+2 & blue=0

return
end
