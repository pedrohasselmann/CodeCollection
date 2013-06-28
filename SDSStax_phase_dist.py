#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: SDSStax_phase_dist.py

''' The phase angle distribution of the SDSSMOC classified sample'''

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

import numpy as np
import os

# Open files #########################################

if os.uname()[1] == 'Mentat':
  root = "H:\\"
elif os.uname()[1] == 'Desktop-ON':
  root = "/home/hassel"
else:
  root = "/media/E094-EC59"

path1 = os.path.join(root,"Projetos","Taxonomia SDSS","PDS Archiving","")
path2 = os.path.join(root,"Dados","Catalogos","")

sdss_obs = open(path1+"SDSStax_obs_table.tab").readlines()
sdss_ast = open(path1+"SDSStax_ast_table.tab").readlines()
sdss_id, phase = np.loadtxt(path2+"ADR4_refl+mags.dat", dtype=str, unpack=True, usecols=(0,9))

# Input parameters #####################################

types = set([obs[36:37].rstrip() for obs in sdss_obs])

print(types)

tax = ['Q','S','V']

#types = list(types) - tax

# ap, ep, sinip
region_max = [2.5,0.13,0.14] #[3.3,0.8,0.8] 
region_min = [2.25,0.07,0.1] #[2.1,0.0,0.0] 

# Chosen region ###################################################################

region = []
for ast in sdss_ast:
  proper_elem = [float(ast[73:79]),float(ast[80:86]),float(ast[87:93])] # ap, ep, sinip
  if (int(ast[0:6]) != 0) and np.all(proper_elem <= region_max) and np.all(proper_elem >= region_min):
    region.append(ast[0:6].lstrip())

  elif (int(ast[0:6]) == 0) and np.all(proper_elem <= region_max) and np.all(proper_elem >= region_min):
    region.append(ast[24:35].rstrip())

# family member taxonomic classifications #########################################

sdss_region =[(obs[44:50],obs[36:38]) for obs in sdss_obs if region.count(obs[0:6].lstrip()) != 0]

# SDSS Observation phase angle ####################################################

sdss_phase = dict(zip(sdss_id,map(float,phase)))

del sdss_obs, sdss_ast, sdss_id, phase, region

# Do search for taxonomic groups ##################################################

import scipy.stats as stats
import matplotlib.pyplot as plt

x = np.linspace(0,30,200)

plt.figure(1,figsize=(10,8),dpi=70)

for each in tax:
  region_types = [obs[0] for obs in sdss_region if  obs[1].count(each) != 0 and obs[1].count(' ') != 0]

  print(len(region_types))

# select phase angles for your taxonomic groups ###################################

  region_phase = [sdss_phase[identity] for identity in region_types if sdss_phase.has_key(identity) == True]

# gaussian density distribution ###################################################


  region_gkde = stats.gaussian_kde(region_phase)

# Plot ##

  #plt.plot(x,region_gkde.evaluate(x),label="SDSS "+each+"-types")
  plt.hist(region_phase,range=(0.0,30.0),normed=True,histtype='step',label="SDSS "+each+"-types")

plt.xlabel("Phase Angle")
plt.ylabel("$f$")
plt.legend()

plt.show()

# END








