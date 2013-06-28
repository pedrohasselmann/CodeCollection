#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename:

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

x = np.linspace(0,30,200)
import os

# Open files #########################################

if os.uname()[1] == 'Mentat':
  root = "H:\\"
elif os.uname()[1] == 'Desktop-ON':
  root = "/home/hassel"
else:
  root = "/media/E094-EC59"

path = os.path.join(root,"Projetos","G-mode","SDSSMOC","")

phase = np.loadtxt(open(path+'T9_q1.2_var0.01_SDSSMOC_entry.dat'), dtype=None, unpack=True, usecols=[44])

plt.figure(1,figsize=(10,8),dpi=70)

#gkde = stats.gaussian_kde(phase)
#plt.plot(x,gkde.evaluate(x),label="SDSS MBCs candidates")

plt.hist(phase,range=(0.0,30.0),normed=True,label="SDSS MBCs candidates")

plt.xlabel("Phase Angle")
plt.ylabel("$f$")
plt.legend()
plt.show()

