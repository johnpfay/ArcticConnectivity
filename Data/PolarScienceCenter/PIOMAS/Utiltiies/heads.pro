; Input the coordinates of arrow tails and heads (4 vectors).
; Return the vectors x1,y1, x2,y2 giving the coordinates for making
; heads on the arrows.

; Keyword "len" is the length of the head as a fraction of the length
; of the shaft.  Default is 0.3.
; Keyword "ang" is the angle (in degrees) between the head and the shaft.
; Default is 20 degrees.

; Example:
; heads, xtail, ytail, xhead, yhead, x1, y1, x2, y2, len=0.4, ang=35
; for i = 0, n-1 do begin
;    plots, [xtail(i),xhead(i)], [ytail(i),yhead(i)]       ; Plot the shafts
;    plots, [x1(i),xhead(i),x2(i)], [y1(i),yhead(i),y2(i)] ; Plot the heads
; endfor

pro heads, xtail, ytail, xhead, yhead, x1, y1, x2, y2, len=len, ang=ang

if not keyword_set(len) then len = 0.3
if not keyword_set(ang) then ang = 20.0

n = n_elements(xtail)
x1 = fltarr(n)
y1 = fltarr(n)
x2 = fltarr(n)
y2 = fltarr(n)

dx = xtail - xhead
dy = ytail - yhead
mag = sqrt(dx*dx + dy*dy)
tol = 1.E-4
bad  = where(mag LT tol, Nsmall)
good = where(mag GE tol, Nbig)

if Nsmall GT 0 then begin
   x1(bad) = xhead(bad)
   y1(bad) = yhead(bad)
   x2(bad) = xhead(bad)
   y2(bad) = yhead(bad)
endif

if Nbig GT 0 then begin
;  (xunit,yunit) is unit vector from head to tail.
   xunit = dx(good) / mag(good)
   yunit = dy(good) / mag(good)
   length = len * mag(good)
   angle = ang * !pi / 180.0
   cc = cos(angle)
   ss = sin(angle)
   x1(good) = length * ( cc * xunit - ss * yunit) + xhead(good)
   y1(good) = length * ( ss * xunit + cc * yunit) + yhead(good)
   x2(good) = length * ( cc * xunit + ss * yunit) + xhead(good)
   y2(good) = length * (-ss * xunit + cc * yunit) + yhead(good)
endif

end
