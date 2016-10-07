;This procedure generates a color table for contour plots
;written by Jinlun Zhang, PSC/APL/UW

pro redblue,nconts,r,g,b,white, black, brown, blue

rgbv = intarr(3,253)
kclrs= intarr(253)
r=intarr(nconts+3)
g=intarr(nconts+3)
b=intarr(nconts+3)

ndisti = nconts-1
intinc = 251/ndisti

nc1=nconts
nc12=fix(nc1/2)
print, 'nc1, nc12',nc1,nc12

if ((nc1 mod 2) eq 0) then begin
      for i=0, nc12-1 do begin
           xxxx=float(i)/float(nc12)*255.0
       	   rgbv(0,i)=xxxx
	   rgbv(1,i)=xxxx
	   rgbv(2,i)=1.0*255.0
      endfor
      for i=nc12, nc1-1 do begin
           xxxx=(1.0-float(i-nc12+1)/float(nc12))*255.0
       	   rgbv(0,i)=1.0*255.0
	   rgbv(1,i)=xxxx
	   rgbv(2,i)=xxxx
      endfor
endif else begin
      for i=0, nc12-1 do begin 
           xxxx=float(i)/float(nc12)*255.0
       	   rgbv(0,i)=xxxx
	   rgbv(1,i)=xxxx
	   rgbv(2,i)=1.0*255.0
      endfor

; set white 
;      	   rgbv(0,nc12)=1.0*255.0
;	   rgbv(1,nc12)=1.0*255.0
;	   rgbv(2,nc12)=1.0*255.0

; set green 
      	   rgbv(0,nc12)=0.0*255.0
	   rgbv(1,nc12)=1.0*255.0
           rgbv(2,nc12)=0.0*255.0

      for i=nc12+1,nc1-1 do begin 
           xxxx=(1.0-float(i-nc12)/float(nc12))*255.0
       	   rgbv(0,i)=1.0*255.0
	   rgbv(1,i)=xxxx
	   rgbv(2,i)=xxxx
      endfor
endelse
       
for m = 0, ndisti do begin
    r(m)=rgbv(0,m)
    g(m)=rgbv(1,m)
    b(m)=rgbv(2,m)
    print, r(m), g(m), b(m)
endfor

	  r(nconts)=0
	  r(nconts+1)=255
	  r(nconts+2)=fix(255*0.9)
	  g(nconts)=0
	  g(nconts+1)=255
	  g(nconts+2)=fix(255*0.9)
	  b(nconts)=0
	  b(nconts+1)=255
	  b(nconts+2)=fix(255*0.9)
	  tvlct, r, g, b
          black=nconts & white=nconts+1 & brown=nconts+2 & blue=0

return
end
