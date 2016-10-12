; This procedure reads lon. and lat. for an arctic ice/ocean model in generalized 
;curvilinear coordinates, the angles between latitude line and grid x-coordinate line, 
;and the model's output of 2-D vector fields such as sea ice velocity, and plots 
;arctic sea ice velocity together with a map of the Arctic. Other 2-D vector fields 
;can be plotted in the same way.

; written by Jinlun Zhang, PSC/APL/UW, zhang@apl.washington.edu

ncol = 1 & nrow=1
data_source=1
n_month1=13
n_month=12
iregion=1      ;iregion=1, arctic; 2, antarctic; 3, global

scale=3.0*40.0*1000.0
scale=2500.0*scale

openfile0=strarr(data_source) & openfile00=strarr(data_source)
openfile=strarr(data_source) & openfile1=strarr(data_source)
openfile0=['grid.dat.pop']
openfile00=['alpha.fortran.dat']

;openfile=['icevel.H2004']
openfile=['uo1_10.H2012']
openfile1=['heff.H2004']

filestr1=strarr(data_source)
filestr1(0)='Sea-Ice Velocity!C'

filestr2=' '

nx=360 & ny=120 ;POIM

;initialize arrays
x1=fltarr(nx,ny, /NOZERO)
y1=fltarr(nx,ny, /NOZERO)
x2=fltarr(nx, /NOZERO)
y2=fltarr(ny, /NOZERO)
data0=fltarr(nx,ny, /NOZERO) & data1=fltarr(nx,ny, /NOZERO)
data3=fltarr(nx,ny, /NOZERO) & data4=fltarr(nx,ny, /NOZERO)
data2=fltarr(2,nx,ny)
alpha=fltarr(nx,ny, /NOZERO)
area_data=fltarr(data_source,n_month1,nx,ny)
vec_data=fltarr(data_source,n_month1,2,nx,ny)
kmt=intarr(nx,ny) & kmu=intarr(nx,ny) & kmt0=intarr(4)
lon=fltarr(nx,ny, /NOZERO) & lat=fltarr(nx,ny, /NOZERO)
vlon=fltarr(nx,ny, /NOZERO) & vlat=fltarr(nx,ny, /NOZERO)
;read files
       close,9 & openr, 9, openfile0(0) ;read grid.dat.pop
       readf, 9, lat, format='(10f8.2)' ;populate lat array from first 360 x 120 records
       readf, 9, lon, format='(10f8.2)' ;populate lon array from next 360 x 120 records
       close,9

       close,9 & openr, 9, openfile00(0) ;read alpha.fortran.dat
       readf, 9, alpha, format='(10f8.2)' ;populate alpha array with 360 x 120 records
       close,9

;for file_ct=0, data_source-1  do begin
 file_ct = 0
 openr, file_ct+1, openfile(file_ct), /swap_if_big_endian ;read icevel.H2004 with LUN 1
 openr, file_ct+10, openfile1(file_ct), /swap_if_big_endian ;read icevel.H2004 with LUN 2

       ;for iii=0,n_month-1 do begin
       iii=0
           readu, file_ct+1, data3 ;u-vectors?
           readu, file_ct+1, data4 ;v-vectors?
           readu, file_ct+10, data0

           vec_data(file_ct,iii,0,*,*)=data3*cos(-alpha*!pi/180.0) $
                                      +data4*sin(-alpha*!pi/180.0)
           vec_data(file_ct,iii,1,*,*)=data4*cos(-alpha*!pi/180.0) $
                                      -data3*sin(-alpha*!pi/180.0)

           for i=0,nx-1-1 do begin
            for j=0,ny-1-1 do begin
             area_data(file_ct,iii,i,j)=0.25*(data0(i,j)+data0(i+1,j) $
                                           +data0(i,j+1)+data0(i+1,j+1))
            endfor
           endfor
      vec_data(file_ct,n_month1-1,0,*,*)=vec_data(file_ct,n_month1-1,0,*,*) $
                                        +vec_data(file_ct,iii,0,*,*)
      vec_data(file_ct,n_month1-1,1,*,*)=vec_data(file_ct,n_month1-1,1,*,*) $
                                        +vec_data(file_ct,iii,1,*,*)
      area_data(file_ct,n_month1-1,*,*) =area_data(file_ct,n_month1-1,*,*) $ 
                                        +area_data(file_ct,iii,*,*)
            ;endfor
      vec_data(file_ct,n_month1-1,0,*,*)=vec_data(file_ct,n_month1-1,0,*,*)/12.0
      vec_data(file_ct,n_month1-1,1,*,*)=vec_data(file_ct,n_month1-1,1,*,*)/12.0
      area_data(file_ct,n_month1-1,*,*)=area_data(file_ct,n_month1-1,*,*)/12.0
;endfor

close,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,99

mask_value=99999.0

;slen=strlen(openfile)
;filestr=heffid(openfile, 21, slen-21)

month=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Annual']
;month=string(format='(i3)',indgen(n_month)+1)

; Define color table.
gun1=[  0, 60,  0,255,  0,  0,255,230,255]
gun2=[  0,180,  0,  0,255,  0,255,230,255]
gun3=[  0,240,  0,  0,  0,192,  0,230,255]
tvlct,gun1,gun2,gun3
white=8 & blue=1 & black=2 & red=3 & green=4 & darkblue=5 & yellow=6 & brown=7

; Define the extent of the map.  Note that 1000 km is about 9 degrees of lat.
xmin = -2600
xmax =  2700
ymin = -2300
ymax =  2200
dx=40.0
cells=3.0

openr,9,'io.dat_360_120.output'
  readf, 9, kmt,format='(360i2)'
close,9

for i=0,nx-2 do begin
for j=0,ny-2 do begin
    kmt0(0)=kmt(i,j)
    kmt0(1)=kmt(i+1,j)
    kmt0(2)=kmt(i,j+1)
    kmt0(3)=kmt(i+1,j+1)
    kmu(i,j)=min(kmt0)
endfor
endfor

kmu(*,ny-1)=1
kmu(*,ny-2)=1
;kmu(*,*)=1
;print ,kmu

; define user symbol, use psym=8 for user defined symbol
aa=findgen(16)*(!pi*2/16.)
;usersym, cos(aa),sin(aa), /fill
;usersym, cos(aa),sin(aa)
usersym, 0.4*cos(aa),0.4*sin(aa)
;usersym, 0.2*cos(aa),0.2*sin(aa)

; start big loop
;draw the vectorr plots

for flag=0,data_source-1 do begin
for count=0, n_month-1 do begin

    filestr=filestr1(flag) + month(count) + filestr2
    data2(*,*,*)=vec_data(flag,count,*,*,*)
    data0(*,*)=area_data(flag,count,*,*)

; Set up the plotting space with no margins or axes.

if iregion eq 1 then begin
;lat1=40 & lat2=90
lat1=50 & lat2=90
;;;;;map_set, 90, 66, -135, limit=[30,-180,90,180],latdel=20, londel=90, lonlab=60, /grid, /continents, /lamb, /noborder

map_set, 90, 0, -90, limit=[lat1,-180,lat2,180],latdel=10, londel=90, title=filestr, /grid, /continents, /lamb, /advance, /noborder

endif else if iregion eq 2 then begin
lat1=-90 & lat2=-40

;map_set, -90, -66, -135, limit=[-90,-180,lat2,180],latdel=20, londel=90, /grid, /continents, /lamb
;map_set, -90, 0, 0, limit=[lat1,-180,lat2,180],latdel=5, londel=90, title=filestr, /grid, /continents, /lamb, /advance, /noborder
map_set, -90, 0, 0, limit=[lat1,-180,lat2,180],latdel=5, londel=90, title=filestr, /grid, /continents, /lamb, /noborder

endif else begin
lat1=-90 & lat2=90
;map_set, limit=[lat1,-180,lat2,180],latdel=20, londel=20, /grid, /continents, /cyl, title=' '
map_set, limit=[lat1,-180,lat2,180],latdel=20, londel=20, /grid, /continents, /cyl, title=filestr
endelse

;for i=0,nx-1 do begin
;for j=0,ny-1 do begin
for i=0,nx-1,2 do begin
for j=0,ny-1,2 do begin
;for i=0,nx-1,3 do begin
;for j=0,ny-1,3 do begin

  if kmu(i,j) gt 0 and data0(i,j) gt 0.005 then begin
    if lat(i,j) ge lat1 and lat(i,j) le lat2 then begin

  xhead=lon(i,j)+data2(0,i,j)/6370000.0/cos(lat(i,j)/57.29578)*scale
  yhead=lat(i,j)+data2(1,i,j)/6370000.0*scale
  if yhead gt 90.0 then begin
  yhead=90.0-(yhead-90.0)
  xhead=xhead+180.0
  endif

  oplot, [lon(i,j),xhead], [lat(i,j),yhead], max_value=99990.0, color=black

if iregion eq 1 then begin
  LLtoXY, [lat(i,j),yhead], [lon(i,j),xhead], xx1, yy1, 0.0
  heads, xx1(0), yy1(0), xx1(1), yy1(1), xx3, yy3, xx4, yy4, len=0.3, ang=25
  XYtoLL, [xx3,xx4], [yy3,yy4], lat3, lon3, 0.0
  oplot, [lon3(0),xhead,lon3(1)], [lat3(0),yhead,lat3(1)], max_value=99990.0, color=black, thick=1.0
endif else if iregion eq 2 then begin
  LLtoXY_s, [lat(i,j),yhead], [lon(i,j),xhead], xx1, yy1, 0.0
  heads, xx1(0), yy1(0), xx1(1), yy1(1), xx3, yy3, xx4, yy4, len=0.3, ang=25
  XYtoLL_s, [xx3,xx4], [yy3,yy4], lat3, lon3, 0.0
  oplot, [lon3(0),xhead,lon3(1)], [lat3(0),yhead,lat3(1)], max_value=99990.0, color=black, thick=1.0
endif
    endif
  endif
endfor
endfor
jump2:

; do vector
for ivec=0,0 do begin
; Draw a vector scale
  if iregion eq 1 then begin
    xlon=90.0+5.5
    xlat=65.0
  endif
  if iregion eq 2 then begin
    xlon=180.0+35.0
    xlat=-86.0
  endif
  if iregion eq 3 then begin
    xlon=70.0
    xlat=-81.0
  endif

  xtail=xlon
  ytail=xlat

  if iregion eq 1 or iregion eq 2 then begin
  xhead=xlon-0.1/6370000.0/cos(xlat/57.29578)*scale
  endif else begin
  xhead=xlon+0.1/6370000.0/cos(xlat/57.29578)*scale
  endelse

  yhead=xlat

  oplot, [xtail,xhead], [ytail,yhead], $
         max_value=99990.0, color=black, thick=2

if iregion eq 1 then begin
  LLtoXY, [ytail,yhead], [xtail,xhead], xx1, yy1, 0.0
  heads, xx1(0), yy1(0), xx1(1), yy1(1), xx3, yy3, xx4, yy4, len=0.3, ang=25
  XYtoLL, [xx3,xx4], [yy3,yy4], lat3, lon3, 0.0
  oplot, [lon3(0),xhead,lon3(1)], [lat3(0),yhead,lat3(1)], max_value=99990.0, color=black, thick=2.0
endif else if iregion eq 2 then begin
  LLtoXY_s, [ytail,yhead], [xtail,xhead], xx1, yy1, 0.0
  heads, xx1(0), yy1(0), xx1(1), yy1(1), xx3, yy3, xx4, yy4, len=0.3, ang=25
  XYtoLL_s, [xx3,xx4], [yy3,yy4], lat3, lon3, 0.0
  oplot, [lon3(0),xhead,lon3(1)], [lat3(0),yhead,lat3(1)], max_value=99990.0, color=black, thick=2.0
endif

  if iregion eq 1 then begin
     xyouts, xlon+4.0, xlat+2.2, '0.1 m/s', color=black, $
          charsize=1.1, charthick=3
  endif
  if iregion eq 2 then begin
     xyouts, xlon-5.0, xlat+3.0, '0.1 m/s', color=black, $
          charsize=1.1, charthick=3
  endif
  if iregion eq 3 then begin
     xyouts, xlon-5.0, xlat-6.0, '0.1 m/s', color=black, $
          charsize=1.1, charthick=3
  endif

endfor

; Draw some characters
;xyouts, 110, 68, filestr, color=white, charsize=2.7, charthick=8, alignment=0.5
;xyouts, 110, 68, filestr, color=black, charsize=2.7, charthick=3, alignment=0.5
;xyouts, -50, 68, string(format='(f6.2)',vmean), color=black, charsize=1.0, charthick=2, alignment=0.5

endfor
endfor
; end of big loops

close,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,99

; Close up.
if keyword_set(ps) then begin
   device, /close_file
   set_plot, 'X'
;  set_plot, 'CGM' ; if current graphics device is CGM by typing: help,/device
endif else begin
   ;hak, /mesg
   ;wdelete, win
endelse

!p.multi = 0
end
