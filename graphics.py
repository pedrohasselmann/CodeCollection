#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: color_graphics.py
# Gráficos no espaço cor-cor.

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division
try:
   xrange = xrange
   # We have Python 2
except:
   xrange = range
   # We have Python 3

# Importar Modulos:
import pg
import math as mth
import statistics as stc
import scipy.stats as stats
import matplotlib.pyplot as mpt
import sys
sys.path.append("/home/usuario/Dados_Astronomicos/Catalogos/")

# Abertura de arquivos:
astDys=open(sys.path[-1]+"astdys_numbered.pro", "r").readlines()

''' data[0] --> Number
    data[1] --> Semi-major axis
    data[2] --> eccentricity
    data[3] --> sine of inclination '''

a=[]; ecc=[]; sinI=[]; num=[]; mag=[]
for data in astDys:
  data=data.split()
  try:
    num.append(int(data[0]))
    a.append(float(data[1]))
    ecc.append(float(data[2]))
    sinI.append(float(data[3]))
    mag.append(float(data[9]))
  except ValueError:
    pass

del astDys

###################################################################################################

answer1=raw_input("Plot the orbital elements distribution (Default=no)? (y/n) ")

if answer1=='y':
 mpt.figure(1,figsize=(11,8),dpi=100)
 mpt.suptitle("Orbital Elements Distribution")

 mpt.subplot(311)
 mpt.hexbin(a,sinI,gridsize=200,bins='log',mincnt=1)
 mpt.xlabel("$a'$ (AU)")
 mpt.ylabel("$sin(i')$")
  
 mpt.subplot(312)
 mpt.hexbin(a,ecc,gridsize=200,bins='log',mincnt=1)
 mpt.xlabel("$a'$ (AU)")
 mpt.ylabel("$e'$")

 mpt.subplot(313)
 mpt.hexbin(sinI,ecc,gridsize=200,bins='log',mincnt=1)
 mpt.xlabel("$e'$ (AU)")
 mpt.ylabel("$sin(i')$")
 cb=mpt.colorbar(orientation='horizontal',fraction=0.10,pad=0.3,drawedges=False)
 cb.set_label('log10(N)')

###################################################################################################

answer2=raw_input("Plot the magnitude distribution (Default=no)? (y/n) ")

if answer2=='y':
 mpt.figure(1,figsize=(11,7),dpi=100)
 mpt.suptitle("Magnitude Distribution")
 mpt.subplot(211)
 mpt.hexbin(a,mag,gridsize=200,bins='log',mincnt=1)
 mpt.xlabel("$a'$ (AU)")
 mpt.ylabel("$Magnitudes$")
 
 mpt.subplot(212)
 dist, mag_dist = stc.pdf(mag)
 mpt.plot(mag_dist, dist,'r-',linewidth=2)
 mpt.hist(mag,bins=200,normed=True)
 mpt.xlim(3,20)
 mpt.xlabel("$Magnitudes$")
 mpt.ylabel("$f$")

# Completeza:
 mpt.plot([17,17],[0,0.5],'b--')
 mpt.plot([15.55,15.55],[0,0.5],'r--')

###################################################################################################

answer3=raw_input("Plot the taxonomic distribution (Default=no)? (y/n) ")

if answer3=='y':
 tax_class=['O','V','A','S','Q','L','D','X','C']
 tax_type={'L':'mo','A':'ro','V':'go','S':'bo','Q':'yo','O':'y*','D':'r*','X':'k*','C':'ko'}
 lmt={'L':120,'A':10,'V':55,'S':500,'Q':35,'O':10,'D':35,'X':40,'C':400}
 tax_type3={'L':'m','A':'r','V':'g','S':'b','Q':'y','O':'y','D':'r','X':'k','C':'k'}
 obs_class=[[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]]]
 
# Selecionando os asteróides do MOC4 classificados taxonomicamente do banco de dados do Postgress => SDSSTax:
 SDSSTax=pg.DB('SDSSTax')
 data=SDSSTax.query("SELECT bclass,bscore,ap,ep,sinip FROM ONLY sdsstax_asttable4 WHERE bclass<>'U' AND bscore>50 \
 AND ap<>0.0 AND ep<>0.0 AND sinip<>0.0;").dictresult()
 print(len(data))
 
 for obs in data:
   for n in range(len(tax_class)):
     if obs['bclass'].strip()==tax_class[n]:
       obs_class[n][0].append(obs['ap'])
       obs_class[n][1].append(obs['ep'])
       obs_class[n][2].append(obs['sinip'])
 print(len(obs_class))
 print(obs_class[0])

# sin(i) X Semi-major axis distribution:
 for n in range(len(tax_class)):
   N=311+n
   if n <= 2:
     N=311+n
     mpt.figure(1,figsize=(11,7),dpi=100)
     mpt.subplot(N)
     mpt.plot(obs_class[n][0],obs_class[n][2],tax_type[tax_class[n]],label=tax_class[n])
#     mpt.hexbin(obs_class[n][0],obs_class[n][1],gridsize=200,bins='log',mincnt=1,label=tax_class[n])
     mpt.legend(loc=4)
     mpt.xlabel("$a'$ (UA)")
     mpt.ylabel("$e'$")
# Ressonâncias:
     mpt.plot([2.5,2.5],[0,0.5],'k-',[2.82,2.82],[0,0.5],'k-',[3.27,3.27],[0,0.5],'k-',[2.96,2.96],[0,0.5],'k-',linewidth=3)
   if n > 2 and n <= 5:
     N=311+n-3
     mpt.figure(2,figsize=(11,7),dpi=100)
     mpt.subplot(N)
     mpt.plot(obs_class[n][0],obs_class[n][1],tax_type[tax_class[n]],label=tax_class[n])
#     mpt.hexbin(obs_class[n][0],obs_class[n][1],gridsize=200,bins='log',mincnt=1,label=tax_class[n])
     mpt.legend(loc=4)
     mpt.xlabel("$a'$ (UA)")
     mpt.ylabel("$e'$")
# Ressonâncias:
     mpt.plot([2.5,2.5],[0,0.5],'k-',[2.82,2.82],[0,0.5],'k-',[3.27,3.27],[0,0.5],'k-',[2.96,2.96],[0,0.5],'k-',linewidth=3)
   if n > 5:
     N=311+n-6
     mpt.figure(3,figsize=(11,7),dpi=100)
     mpt.subplot(N)
     mpt.plot(obs_class[n][0],obs_class[n][1],tax_type[tax_class[n]],label=tax_class[n])
#     mpt.hexbin(obs_class[n][0],obs_class[n][1],gridsize=200,bins='log',mincnt=1,label=tax_class[n])
     mpt.legend(loc=4)
     mpt.xlabel("$a'$ (UA)")
     mpt.ylabel("$e'$")
# Ressonâncias:
     mpt.plot([2.5,2.5],[0,0.5],'k-',[2.82,2.82],[0,0.5],'k-',[3.27,3.27],[0,0.5],'k-',[2.96,2.96],[0,0.5],'k-',linewidth=3)

 mpt.suptitle("Taxonomic Distribution")

# Histograms:
 for n in range(len(tax_class)):
   if n <= 2:
     N=311+n
     mpt.figure(4,figsize=(11,7),dpi=100)
     mpt.subplot(N)
     mpt.hist(obs_class[n][0],bins=50,histtype='stepfilled',color=tax_type3[tax_class[n]],label=tax_class[n])
     mpt.legend(loc=4)
     mpt.ylabel("$N$")
     mpt.xlabel("$a'$ (AU)")
# Ressonâncias:
     mpt.plot([2.5,2.5],[0,lmt[tax_class[n]]],'k-',[2.82,2.82],[0,lmt[tax_class[n]]],'k-',[3.27,3.27],[0,lmt[tax_class[n]]],'k-',[2.96,2.96],[0,lmt[tax_class[n]]],'k-',linewidth=3)
   if n > 2 and n <= 5:
     N=311+n-3
     mpt.figure(5,figsize=(11,7),dpi=100)
     mpt.subplot(N)
     mpt.hist(obs_class[n][0],bins=50,histtype='stepfilled',color=tax_type3[tax_class[n]],label=tax_class[n])
     mpt.legend(loc=4)
     mpt.ylabel("$N$")
     mpt.xlabel("$a'$ (AU)")
# Ressonâncias:
     mpt.plot([2.5,2.5],[0,lmt[tax_class[n]]],'k-',[2.82,2.82],[0,lmt[tax_class[n]]],'k-',[3.27,3.27],[0,lmt[tax_class[n]]],'k-',[2.96,2.96],[0,lmt[tax_class[n]]],'k-',linewidth=3)
   if n > 5:
     N=311+n-6
     mpt.figure(6,figsize=(11,7),dpi=100)
     mpt.subplot(N)
     mpt.hist(obs_class[n][0],bins=50,histtype='stepfilled',color=tax_type3[tax_class[n]],label=tax_class[n])
     mpt.legend(loc=4)
     mpt.ylabel("$N$")
     mpt.xlabel("$a'$ (AU)")
# Ressonâncias:
     mpt.plot([2.5,2.5],[0,lmt[tax_class[n]]],'k-',[2.82,2.82],[0,lmt[tax_class[n]]],'k-',[3.27,3.27],[0,lmt[tax_class[n]]],'k-',[2.96,2.96],[0,lmt[tax_class[n]]],'k-',linewidth=3)

###################################################################################################

answer4=raw_input("Plot the albedo distribution (Default=no)? (y/n) ")

if answer4=='y':
 data=open(sys.path[-1]+'albedos.tab', 'r').readlines()

 TRIAD=[]; IMPS=[]; POLR=[]; POLZ=[]; RADAR=[]
 for item in data:
   item=item.split()
   if item[4] != '9':
     TRIAD.append([int(item[0]),float(item[3])])
   if item[7] != '0':
     IMPS.append([int(item[0]),float(item[5]),float(item[6])])
   if item[11] != '-9':
     POLR.append([int(item[0]),float(item[8]),float(item[9])])
     POLZ.append([int(item[0]),float(item[10])])
   if item[14] != '-9':
     RADAR.append([int(item[0]),float(item[12]),float(item[13])])

 print(len(IMPS))
 mpt.figure(1,figsize=(11,8),dpi=100)
 mpt.suptitle("Geometric Albedo Distribution")
 
 alb=[]; a1=[]; Diam=[]
 for n in range(len(num)):
   for obs in IMPS:
     if num[n]==obs[0]:
       D=(1329/mth.sqrt(obs[1]))*10**(-0.2*mag[n])
       a1.append(a[n])
       Diam.append(D)
       alb.append(obs[1])
      
 mpt.subplot(311)
# mpt.errorbar(a[n],obs[1],fmt='ko')
 mpt.hexbin(a1,alb,gridsize=100,bins='log',mincnt=1)
 mpt.xlabel("$a'$ (AU)")
 mpt.ylabel("Geometric Albedo")
 mpt.subplot(312)
 mpt.hist(alb,bins=80,normed=True)
 mpt.ylabel("$f$")
 mpt.xlabel("Geometric Albedo")
 mpt.subplot(313)
# mpt.errorbar(obs[1],D,fmt='ko')
 mpt.hexbin(alb,Diam,gridsize=100,bins='log',mincnt=1)
 mpt.ylim(0,300)
 mpt.ylabel("$Diameter$ (km)")
 mpt.xlabel("Geometric Albedo")

###################################################################################################

answer5=raw_input("Plot the size distribution (Default=no)? (y/n) ")

if answer5=='y':
 data=open(sys.path[-1]+'albedos.tab', 'r').readlines()

 diam=[]; ap=[]; diam_er=[]; alb=[]
 for item in data:
   item=item.split()
   if item[7] != '0':
     alb.append([int(item[0]),float(item[5]),float(item[6])])
 del data

 for i in range(len(num)):
   for j in range(len(alb)):
     if alb[j][0]==num[i]:
       diam.append((1329/mth.sqrt(alb[j][1]))*10**(-0.2*mag[i]))
       diam_er.append((1329/2)*mth.sqrt((alb[j][2])*(alb[j][1]**(-3)))*10**(-0.2*mag[i]))
       ap.append(a[i])

 mpt.figure(1,figsize=(11,8),dpi=100)
 mpt.suptitle("Size Distribution")
 mpt.subplot(211)
 mpt.hexbin(ap,diam,gridsize=200,bins='log',mincnt=1)
 mpt.xlabel("$a'$ (AU)")
 mpt.ylabel("$Diameter$ (km)")
 mpt.ylim(0,300)
       
 mpt.subplot(212)
 dist, size_dist = stc.pdf(diam,h=stc.bandwidth(diam))
 mpt.plot(size_dist, dist,'r-',linewidth=2)
 mpt.hist(diam,bins=80,normed=True)
 mpt.xlim(0,250)
 mpt.xlabel("$Diameter$ (km)")
 mpt.ylabel("$f$")

###################################################################################################

answer6=raw_input("Plot the period distribution (Default=no)? (y/n) ")

if answer6=='y':
 data=open(sys.path[-1]+'LC_database.TXT', 'r').readlines()

 period=[]; diam=[]; mag2=[]; period_small=[]; period_big=[]
 for item in data:
   try:
     if item[105:114]!='         ':
      diam.append(float(item[72:78]))
      mag2.append(float(item[83:88]))
      period.append(float(item[105:114]))
      if float(item[72:78]) <= 10:
        period_small.append(float(item[105:114]))
      if float(item[72:78]) >= 40:
	period_big.append(float(item[105:114]))
   except ValueError:
     pass

 print(len(period),len(diam),len(mag2))
 mpt.figure(1,figsize=(11,8),dpi=100)
 mpt.suptitle("Period Distribution")

 mpt.subplot(311)
 mpt.loglog(diam,period,'k.')
 mpt.ylim(1000,0)
 mpt.ylabel("$Period$ $Rotation$ (hours)")
 mpt.xlabel("$Diameter$ (km)")
 
 mpt.subplot(312)
 mpt.hist(period_small,bins=300, label="Small Asteroids (D < 10 km)")
 mpt.xlim(0,80)
 mpt.ylabel("$N$")
 mpt.xlabel("$Period$ $Rotation$ (hours)")
 mpt.legend(loc=4)
 
 
 mpt.subplot(313)
 mpt.hist(period_big,bins=200, label="Large Asteroids (D > 40 km)")
 mpt.xlim(0,80)
 mpt.ylabel("$N$")
 mpt.xlabel("$Period$ $Rotation$ (hours)")
 mpt.legend(loc=4)

###################################################################################################

answer7=raw_input("Plot the spin vector distribution (Default=no)? (y/n) ")

if answer7=='y':
 data=open(sys.path[-1]+'asteroid_spin_vector.tab', 'r').readlines()

 mpt.figure(1,figsize=(11,8),dpi=100)
 mpt.suptitle("Spin Vector Distribution")
 
 spin=[]
 
 for item in data:
   item=item.split()
   if item[1]=='-':
     for n in range(4,13,3):
       if item[n] != '-99':
         spin.append(float(item[n]))

 print(len(spin))
 mpt.hist(spin,bins=10)
 mpt.ylim(0, 35)
 mpt.ylabel("$N$")
 mpt.xlabel("Spin Latitude")
 

#Mostrar:
mpt.show()

# END