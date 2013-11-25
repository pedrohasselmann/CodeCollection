#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename:

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

import numpy as np
import matplotlib.pyplot as plt

SDSSID, tax = np.loadtxt(open('/home/hassel/Projetos/G-mode/Classification/gmode_c_q1.2_var0.01_SDSSMOC_3q.dat', 'r'), usecols=[1,2], delimiter=None, dtype=str, unpack=True)
moc4 = np.genfromtxt(open('/home/hassel/Projetos/G-mode/SDSSMOC/MOC4_3quartile.dat', 'r'), skiprows=1, delimiter=None, dtype=None)

filters=[0.36,0.47,0.62,0.75,0.89]

T9= [SDSSID[i] for i in range(len(SDSSID))  if tax[i] == 'T9']

plt.figure(figsize=(12,5),dpi=90)

for obs in moc4:
  for MBC in T9:
    if obs[2] == MBC:
      plt.errorbar(filters,list(obs)[3:8],yerr=list(obs)[8:],fmt='.',color='k',ecolor='k',linestyle='-',linewidth=1)

plt.xlabel("$\lambda$ ($\mu$ m)")
plt.ylabel('Refletância Normalizada')
plt.title("Candidates to Main Belt Comets")
plt.xlim(0.3,1.0)
plt.show()

