c Progrem to read sea ice thickness and velocity, can be used to read other scaler or vector fields
      parameter(nx1=360,ny1=120,nx=nx1,ny=ny1,imt=nx1,jmt=ny1)
      parameter(nyear1=1978,nyear2=2004)

      dimension heff(imt,jmt)
      dimension uice(imt,jmt),vice(imt,jmt)

      dimension clon(imt,jmt),clat(imt,jmt),kmt(imt,jmt)
      dimension ulat(imt,jmt),ulon(imt,jmt),HTN(imt,jmt),HTE(imt,jmt)
     &,HUS(imt,jmt),HUW(imt,jmt),angle(imt,jmt),dxt(imt,jmt)
     &,dyt(imt,jmt)

      character *80 fopen(5), f1,f2,f3
      character *4 cyear(1900:2100),cyear1(1900:2100)
      character *12 char
      integer SLEN

      f2='heff.H'
      f3='icevel.H'

c read lon and lat for scalar fields (like sea ice thickness and concentration)
      open(20,file='grid.dat')
      read(20,'(10f8.2)') ((clon(i,j),i=1,nx1),j=1,ny1)
      read(20,'(10f8.2)') ((clat(i,j),i=1,nx1),j=1,ny1)
      close(20)

c read lon and lat for vector fields (like sea ice and ocean veclocities)
      open(24,file='grid.dat.pop')
        read(24,'(10f8.2)') ((ulat(i,j),i=1,nx),j=1,ny)
        read(24,'(10f8.2)') ((ulon(i,j),i=1,nx),j=1,ny)
c HTN, HTE, HUS, HUW are lengths of the 4 sides of a grid cell in km
c HTN, HTE are lengths of the northern and eastern sides of a scaler grid cell in km, HTN*HTE is the area of a scaler grid cell in km**2 and can be used to calculate sea ice volume and volumes of other variables
c HUS, HUW are lengths of the southern and western sides of a vector grid cell in km
        read(24,'(10f8.2)') ((HTN  (i,j),i=1,nx),j=1,ny)
        read(24,'(10f8.2)') ((HTE  (i,j),i=1,nx),j=1,ny)
        read(24,'(10f8.2)') ((HUS  (i,j),i=1,nx),j=1,ny)
        read(24,'(10f8.2)') ((HUW  (i,j),i=1,nx),j=1,ny)
c angle is the angle between latitude line and  grid cell x-coordinate line, needed for plotting vecto
rs in spherical coordinate system
        read(24,'(10f8.2)') ((angle(i,j),i=1,nx),j=1,ny)
      close(24)

c read model grid mask; ocean levels > 0, land <= 0
      open(20,file='io.dat_360_120.output')
      read(20,'(360i2)') kmt
      close(20)

      do 999 iyear=nyear1,nyear2

      write(unit=cyear(iyear),fmt='(i4)') iyear
      i=slen(f2)
      open(2,file=f2(1:i)//cyear(iyear)
     &,access='direct',form='unformatted',recl=nx1*ny1*4
     &,status='unknown')

      i=slen(f3)
      open(3,file=f3(1:i)//cyear(iyear)
     &,access='direct',form='unformatted',recl=nx1*ny1*4
     &,status='unknown')


      do imon=1,12
      read(2)((heff(i,j),i=1,nx1),j=1,ny1)
      read(3)((uice(i,j),i=1,nx1),j=1,ny1)
      read(3)((vice(i,j),i=1,nx1),j=1,ny1)
      end do

      close(2)
      close(3)
999   continue

      stop
      end
      INTEGER FUNCTION slen (string)
C ---
C --- this function computes the length of a character string less
C --- trailing blanks
C --- slen > 0, length of string less trailing blanks
C ---      = 0, character string is blank
C ---
      CHARACTER*(*) string
      CHARACTER*1 cblank
      INTEGER i
      DATA cblank/' '/
C ---
      DO 50 i = LEN(string), 1, -1
         IF (string(i:i) .NE. ' ')  GO TO 100
50    CONTINUE
      i = 0
100   CONTINUE
      slen = i
      RETURN
      END

