#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: X² vs Gaussian

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division
try:
   xrange = xrange
   # We have Python 2
except:
   xrange = range
   # We have Python 3

from scipy.stats import norm
from scipy.stats import chi2
import numpy as np
import matplotlib.pyplot as plt

plt.figure(figsize=(8,10),dpi=100)

plt.subplot(211)
plt.title("$f$ = 30")
plt.xlabel('X')
plt.ylabel('Frequência Normalizada')
rv1 = norm(loc=3, scale=8.2)

x1 = np.linspace(0, 40)
plt.plot(x1, rv1.pdf(x1)/np.amax(rv1.pdf(x1)),'r-',linewidth=2,label="Gaussiana")

rv2 = chi2(30,loc=-25)
x2 = np.linspace(0, 40)
plt.plot(x2, rv2.pdf(x2)/np.amax(rv2.pdf(x2)),'b-',linewidth=2,label="$\chi$²")

plt.legend()

##################################################################

plt.subplot(212)
plt.title("$f$ = 100")
plt.xlabel('X')
plt.ylabel('Frequência Normalizada')
rv1 = norm(loc=3, scale=15)

x1 = np.linspace(0, 50)
plt.plot(x1, rv1.pdf(x1)/np.amax(rv1.pdf(x1)),'r-',linewidth=2,label="Gaussiana")

rv2 = chi2(100,loc=-95)
x2 = np.linspace(0, 50)
plt.plot(x2, rv2.pdf(x2)/np.amax(rv2.pdf(x2)),'b-',linewidth=2,label="$\chi$²")

plt.legend()

plt.show()
