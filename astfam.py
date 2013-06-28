#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: astfam.py
# author: Pedro Henrique A. Hasselmann
# date: August 2012

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

from os import path

home = path.expanduser("~")

class AsteroidFamilyStats:
  __version__ = 0.9

  '''
   Statistical Work with Asteroid Families.
   Magnitude and albedo taken from Nervorny Asteroid Families (PDS Dataset).
   Taxonomic Classifications are taken from Carvano et al. (2010).
   Geometric albedos are from preliminary data provided by NEOWISE.
  '''
##################################### INITIALIZATION
  def __init__(self,famfile="101_vesta"):

    self.paths = list()

     
    self.paths.append(path.join(home,"Projetos","Taxonomia SDSS","PDS Archiving",""))
    self.paths.append(path.join(home,"Dados","Catalogos",""))
    
    #print("initialization.....OK.")

##################################### LOAD MEMBERS AND MAGNITUDE
    import zipfile

    '''
       Load Nesvorny families from a zipped file.
       Make a dictionay of magnitudes of each member.
    '''

    # open Nesvorny Families:
    with zipfile.ZipFile(self.paths[-1]+"NESVORNY_FAMILIES_V2_0.zip", "r") as nesvorny_fam:
         fam = nesvorny_fam.open(os.path.join("EAR_A_VARGBDET_5_NESVORNYFAM_V2_0","data","families","")+famfile+".tab").readlines()
         members = [ID[7:13].strip() if int(ID[7:13]) != 0 else ID[14:24].strip() for ID in fam]
         magnitudes = [float(mag[53:58]) for mag in fam]
         #nesvorny_fam.printdir()
     
    print("Asteroid Family size:", len(members))
    
    #setting in self:
    self.mag_fam = dict(zip(members,magnitudes))

    del fam, members, magnitudes

    # Open Asteroid Albedos:
    #wise_alb = open(sys.path[-1]+"WISE_MBA_Pass1_2011.dat", "r")

##################################### LOAD CARVANO Classification:
  def LoadMOC(self):
    import zipfile
    from collections import Counter

    '''
      Load informations of member's observations from the SDSSMOC.
    '''

    with zipfile.ZipFile(self.paths[-1]+"SDSSMOC4_ID_V2.zip", "r") as sdss:
      obs = sdss.open("ADR4_ident2.dat","r")
      
      look_members = Counter(dict.keys(self.mag_fam))
      
      sdss_code=dict(); phase=dict()
      
      for entry in obs:
        if look_members[entry[244:251].strip()] == 1 or look_members[entry[252:272].strip()] == 1:        
          phase[entry[:6]] = float(entry[334:339])
          
          if entry[244:251].strip() != '0':
            sdss_code[entry[:6]] = str(entry[244:251]).strip()
          else:
            sdss_code[entry[:6]] = str(entry[252:272]).strip()
    
    look_members = Counter(dict.values(sdss_code))

    # setting in self:
    self.sdss_code = sdss_code
    self.phase_fam = phase

##################################### LOAD CARVANO Classification:
  def LoadTax(self):
    from collections import Counter 
    
    '''
      Make a dictionary of members with taxonomic classification by Carvano et al. (2010).
    '''

    carvano = open(self.paths[-2]+"SDSStax_ast_table.tab")

    look_members = Counter(dict.keys(self.mag_fam))

    # Correlate asteroid ID and classification:
    tax_fam = dict()
    for entry in carvano:
      if look_members[entry[:6].strip()] == 1 or look_members[entry[24:35].strip()] == 1:
       if int(entry[:6]) != 0: 
        tax_fam[entry[:6].strip()] = entry[36:38].strip()
       else:
        tax_fam[entry[24:35].strip()] = entry[36:38].strip()

    print("Family Members with SDSS classification:", len(dict.keys(tax_fam)))
    
    del carvano
    
    # setting in self:
    self.tax_fam = tax_fam
    
##################################### LOAD WISE Albedos and Diameter
  def LoadWISE(self):
    from numpy import genfromtxt
    from collections import Counter
    from math import isnan
    from packdesig import convert_design
    '''
      Make a dictionary of members with albedo and diameters.
    '''
    wise = map(list,genfromtxt(self.paths[-1]+"WISE_MBA_Pass1_2011.dat", dtype=None, skiprows=23))
    
    look_members = Counter(dict.keys(self.mag_fam))
    
    alb_fam = dict(); diam_fam= dict()
    n = 1
    for entry in wise:

      try:
       des = convert_design(entry[0].lstrip('0'))
      except IndexError:
       des = entry[0].lstrip('0')
   
      if look_members[des] == 1 and isnan(entry[1]) == False and isnan(entry[5]) == False:

        if alb_fam.has_key(des) == True:
          n+=1
          prev = des
          alb_fam[des] = alb_fam.get(des) + float(entry[5])
          diam_fam[des] = diam_fam.get(des) + float(entry[3])
        else:
          try:
           alb_fam[prev] = alb_fam.get(prev)/float(n)
           diam_fam[prev] = diam_fam.get(prev)/float(n)
           #print(prev,alb_fam.get(prev),n)
          except UnboundLocalError:
           pass

          alb_fam[des] = round(entry[5], 4)
          diam_fam[des] = round(entry[3], 4)

          n = 1

    alb_fam[prev] = alb_fam.get(prev)/float(n)
    diam_fam[prev] = diam_fam.get(prev)/float(n)

    print("Family Members with WISE albedo: ",len(dict.keys(alb_fam)))
    #print(alb_fam)
    del wise, entry

    # setting in self:
    self.alb_fam = alb_fam
    self.diam_fam = diam_fam         

##################################### Split In taxonomic classification
  def SplitInTax(self,par='magnitude',*taxs):
    from scipy.stats import gaussian_kde
    from collections import deque
    '''
      Split the physical parameters of family members in N groups of taxonomic classification.
      Choose the parameter that will be splitted.
      Choose the taxonomic groups according to Carvano et al. (2010).
    '''

    if par == 'magnitude': phys_par = self.mag_fam
    if par == 'albedo': phys_par = self.alb_fam
    if par == 'diameter': phys_par = self.diam_fam

    tax_fam = self.tax_fam
    alb_fam = self.alb_fam

    self.split =[deque() for n in xrange(len(taxs))]
    self.split_gkde =[list() for n in xrange(len(taxs))]

    for ast in dict.keys(tax_fam):
      for n, tax in enumerate(taxs):
        if tax_fam[ast] == tax and alb_fam.has_key(ast) == True:
          try:
            self.split[n].append(phys_par[ast])
          except KeyError:
            pass

    # gaussian density distribution
    #xmin = min(dict.values(phys_par))
    #xmax = max(dict.values(phys_par))
    for n, tax in enumerate(taxs):
      self.split[n] = list(self.split[n])
      print(tax+'-types: ',len(self.split[n]))
      self.split_gkde[n] = gaussian_kde(self.split[n])
    
    # setting in self:
    self.taxs = taxs
    self.par  = par


##################################### PLOT DISTRIBUTIONS
  def Plot(self,xmin=10,xmax=20,bins=80,lbl='Vestian'):
    import matplotlib.pyplot as plt
    from numpy import linspace
    
    '''
      Plot frequency distribution of a parameter of n taxonomic groups.
    '''

    try:
     self.taxs
    except NameError:
     print('Reload the SplitInTax() attribute.')

    x = linspace(xmin,xmax,bins)

    plt.figure(1,figsize=(10,8),dpi=70)
    
    [plt.plot(x,dist.evaluate(x),label=lbl+" "+self.taxs[n]+"-types") for n, dist in enumerate(self.split_gkde)]
    [plt.hist(dist,range=(xmin,xmax),normed=True,histtype='step',label=lbl+" "+self.taxs[n]+"-types") for n, dist in enumerate(self.split)]
    
    if self.par == 'magnitude': plt.xlabel("Absolute Magnitude")
    if self.par == 'albedo': plt.xlabel("Geometric Albedo")
    if self.par == 'diameter': plt.xlabel("Diameter")

    plt.ylabel("$f$")
    plt.legend()

    plt.show()

##################################### TWO-SAMPLE KS-TEST
  def KStest2(self,tax1,tax2):
    from scipy.stats import ks_2samp
    
    try:
     self.taxs
    except NameError:
     print('Reload the SplitInTax() attribute.')
    
    n1 = self.taxs.index(tax1)
    n2 = self.taxs.index(tax2)
    
    print('Two-Sample KS test: ',ks_2samp(self.split[n1],self.split[n2]))

##################################### SANITY TEST
  def Sanity(self,tax,per=0.2):
    from scipy.stats import ks_2samp
    import random as rd
    
    '''
      Testing the sanity of the two-sample KS test.
    '''
    
    test=list()
    test.extend(self.split[self.taxs.index(tax)])
    total = len(test)
    
    l=[[],[]]
    
    # Randomly sorting 20% of a previous splitted list.
    for n in [0,1]:
      i=0
      while i <= per*total:
      
        x = rd.choice(test)
        l[n].append(x)
        test.remove(x)
      
        i +=1

    print(len(test),len(l[0]),len(l[1]))
    print('Sanity Two-Sample KS test: ',ks_2samp(l[0],l[1]))



# END
