      PROGRAM ADR4_SELECTING

      implicit none

      REAL rowc,colc,time,RA,DEC,lamb,beta,phi,vmu,vmuE,vnu,vnuE,
     *vlamb,vbeta,u,uE,g,gE,r,rE,i,iE,z,zE,a,aE,V,B,comp1,comp2,comp3,
     *R1,geoc,phase,H,G1,epoch,a1,e1,i1,lan,arg,M,ap,exc,sinI,
     *betaG,alfaG,the,betaN,alfaN,latgal,longal

      INTEGER run,col,field,obj,iflag,num,detc,tdetc,arc,N,N1,X,J

      CHARACTER moID*6,code*15,cat*15,pcat*17,bflag1*64,bflag2*64,
     *flags*8,ADR3_ID(67637)*6

c Abertura dos arquivos.
         open(10, file='ADR4_ident.dat', status='old')
         open(11, file='ADR3_ident.dat', status='old')
         open(12, file='ADR4_ident2.dat', access='append')

      J=1

2     read(11,200,end=112) ADR3_ID(J)

      J=J+1
      GO TO 2
112   CONTINUE

200   format(a6)

      N=J


c Mechanismo:

      betaG=(3.141592654*27.1283361)/180           ! declinacao do polo norte galactico
      alfaG=(3.141592654*192.8595083)/180          ! ascencao reta do polo norte galactico
      the=(3.141592654*(32.932))/180               ! PGL

       X=1; J=0; N1=0

1     read(10,100,end=111) moID,run,col,field,obj,rowc,colc,time,RA,
     *DEC,lamb,beta,phi,vmu,vmuE,vnu,vnuE,vlamb,vbeta,u,uE,g,gE,r,rE,
     *i,iE,z,zE,a,aE,V,B,iflag,num,code,detc,tdetc,flags,comp1,comp2,
     *comp3,R1,geoc,phase,cat,H,G1,arc,epoch,a1,e1,i1,lan,arg,M,pcat,
     *ap,exc,sinI,bflag1,bflag2

      N1=0          

      IF ((u.EQ.99.99).OR.(uE .EQ.9.99).OR.(g.EQ.99.99).OR.
     *(gE .EQ.9.99).OR.(r.EQ.99.99).OR.(rE .EQ.9.99).OR.(i.EQ.99.99)
     *.OR.(iE .EQ.9.99).OR.(z.EQ.99.99).OR.(zE .EQ.9.99)) THEN
     
      ELSE     

      DO J=1, N
       IF (moID .EQ. ADR3_ID(J)) THEN
       
       write(12,100) moID,run,col,field,obj,rowc,colc,time,RA,
     *DEC,lamb,beta,phi,vmu,vmuE,vnu,vnuE,vlamb,vbeta,u,uE,g,gE,r,rE,i,
     *iE,z,zE,a,aE,V,B,iflag,num,code,detc,tdetc,flags,comp1,comp2,
     *comp3,R1,geoc,phase,cat,H,G1,arc,epoch,a1,e1,i1,lan,arg,M,
     *pcat,ap,exc,sinI,bflag1,bflag2   
     
       GO TO 3      
       
       ELSE
       
       N1=N1+1
       
       END IF
3     END DO
    
      IF (N1 .EQ. N) THEN
      
      betaN=(3.141592654*DEC)/180    ! transformando Dec em radianos 
      alfaN=(3.141592654*RA)/180     ! transformando RA  em radianos

c Calculando b(latitude) e l (longitude)

      latgal=asin(0.4559798929D0 * sin(betaN) + 
     *0.8899900771D0 * cos(betaN)* cos(alfaN - 0.3365867463D1))

      longal=the + atan((tan(betaN)*cos(betaG) - 
     *cos(alfaN-alfaG)*sin(betaG)) / (sin(alfaN - alfaG)))

      IF ((latgal .LT. 0).AND.(abs(DEC) .LT. 1.26)) THEN

        ELSE

         write(12,100) moID,run,col,field,obj,rowc,colc,time,RA,
     *DEC,lamb,beta,phi,vmu,vmuE,vnu,vnuE,vlamb,vbeta,u,uE,g,gE,r,rE,i,
     *iE,z,zE,a,aE,V,B,iflag,num,code,detc,tdetc,flags,comp1,comp2,
     *comp3,R1,geoc,phase,cat,H,G1,arc,epoch,a1,e1,i1,lan,arg,M,
     *pcat,ap,exc,sinI,bflag1,bflag2
     
      print*, X     

      END IF
       END IF
      
      END IF

      X=X+1
      GO TO 1
111   CONTINUE

      print*, X

100   format(a6,2x,i4,1x,i1,1x,i4,2x,i4,2(1x,f8.3),3x,f12.6,
     *4(1x,f10.6),1x,f11.6,2x,2(f7.4,1x,f6.4,1x),f7.4,1x,f7.4,2x,
     *5(f5.2,1x,f4.2,1x),f5.2,1x,f4.2,2x,2(f5.2,1x),i1,1x,i7,1x,
     *a15,7x,i1,2x,i1,1x,a8,2x,f10.6,2x,f9.6,1x,f5.2,4x,f5.3,3x,
     *f5.3,1x,f5.2,2x,a15,6x,f5.2,1x,f4.2,1x,i5,2x,f12.6,3x,f10.8,1x,
     *f10.8,4(1x,f10.6),2x,a17,6x,f10.8,1x,f10.8,3x,f8.6,a64,a64)

      END 