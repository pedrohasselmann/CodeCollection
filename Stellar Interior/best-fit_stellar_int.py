#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: best-fit_stellar_int.py

''' Best-fit to Stellar Interior Model parameters compared to a given tabel of another model parameters'''

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

# Modules

import numpy as np
import matplotlib.pyplot as plt
#import stellar_interior_mello as sim

###### FUNCTION #####

def model(m0, r0, vl0, t0, d0, x, z):
 import stellar_interior_mello as sim

 radius,mass,dens,pres,temp,lum,trans = sim.stellar_int(m0, r0, vl0, t0, d0, x, z)

 try:
   cut_low = list(radius).index(0.680)
   cut_up = list(trans).index(0)
 
   test =[radius,mass,pres,temp,lum,dens]
   test =[each[cut_low:cut_up-1] for each in test]
   #print(test)
 except ValueError:
   #print(1)
   test = None

 return test


def X2(test, fit_tabel):
 from numpy import polyval

 # Conditional Evaluation:
 i = 0
 for r, m in zip(test[0],test[1]):
    if (m < 0e0 and r >= 0.1) or (r < 0e0 and m >= 0.1): 
     i = 1
     break
    else:
     i = 0
     break

 ''' Calculate the X2 between the mello's model and novotny tabel parameters'''
 if i != 1 and len(test[0]) > 6:

   dev = lambda x, y: sum((x - y)**2)
   X2_sum = [dev(polyval(fit, test[0]), out) for fit, out in zip(fit_tabel,test[1:])]
   #print(X2_sum)

 else:
   #print(2)
   X2_sum = None

 return X2_sum

###### INPUT #####

#vm0, r0, vl0, t0, d0 = 15, 4.648, 20820, 32220, 0.0327
p0 = [15, 4.648, 20820, 32220, 0.0327]

M, R, P, T, L, pr = np.loadtxt('tabel_novotny.dat', skiprows=1, dtype=float, unpack=True)

M = M/15
R = R/4.648
P = P*10**17
T = T*10**6
L = L/20820

tabel = [R, M, P, T, L, pr]
#[print(R[j], M[j], P[j], T[j], L[j], pr[j]) for j in range(len(R))]
del M, R, P, T, L


###### FIT SPLINE ########
from numpy import polyfit, polyval

fit = [polyfit(tabel[0], phys_par, deg=7) for phys_par in tabel[1:]]

#plt.plot(tabel[0],tabel[-1],'k*',tabel[0],polyval(fit[-1],tabel[0]),'r-')
#plt.show()

#######  FORCE-BRUTE X2 TEST #######
from scipy import optimize as optm
arange = np.arange
np.all

#b = [(15,15),(4.1832,5.1128),(18738,22902),(28998,35442),(0e0,0.1)]

X2_min = [1e35  for j in range(len(tabel))]

for drad in arange(4.1832,5.1128,0.02):
  for dpr in arange(0e0,0.04,0.002):
   for dlum in arange(18738,22902,200):
    for dTeff in arange(28998,35442,200):

      test = model(15, drad, dlum, dTeff, dpr, 0.7, 0.02)

      if test != None: X2_test = X2(test, fit)

      if np.all(X2_test < X2_min) and X2_test != None:
       opt = (drad,dpr,dlum,dTeff,X2_test)
       print(opt)
       X2_min.extend(X2_test)

#opt = optm.fmin_slsqp(X2,x0=p0,bounds=b,args=fit, iter=1000)

print(opt)
# END