#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: binarytree.py
# Binary Tree
# Author: Pedro H. A. Hasselmann

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

from os import path, makedirs
import cPickle as pkl

home = path.expanduser("~")
#path.join(home,"Catalogues","RelabDB2012Dec.zip")

class Relab:

  import pandas as pd
  global pd

  def __init__(self, pth= path.join("D:","Catalogs","RelabDB2012Dec.zip")):
     import zipfile

     # Create a ZipFile Object for Relab Database:
     self.db = zipfile.ZipFile(pth)

  def retrieve_from(self, link, ft):
     ''' Retrieve paths inside a given folder.'''
     
     link = link.split("/")[0:-1]
     retrieve = dict()
     n = True     
     
     for pth in self.db.namelist():
         
        pth2 = pth.split("/")[0:-1]
        filename = pth.split("/")[-1][:-4]
        pth_ft = pth[-3:]
        
        if pth2 == link and n == True:
          if pth_ft == ft: 
            retrieve[filename] = pth
          n = True
          
        elif pth2 != link and n == False:
          n = False
          break
      
     return retrieve
           

  def dataframe(self, filename, missing=["   "], indexid="SampleID", extract=True):
     from numpy import genfromtxt, loadtxt
     import xlrd as excel

     #makedirs(filename[0:-4].replace("/","\ "))
         
     if extract: self.db.extract(filename, '.')
     
     loadexcel = excel.open_workbook(filename.replace("/","\\"), on_demand=True)
     #sheet = loadexcel.sheet_by_name(loadexcel.sheet_names()[0])
     #print(sheet.ncols, sheet.nrows)

     f = pd.read_excel(
                       filename.replace("/","\\"), 
                       loadexcel.sheet_names()[0], 
                       header=0,
                       index_col=indexid,
                       na_values=missing,
                       )
     return f
     
  def retrieve_spectra(self, samplename, spectraname):
    
     link = samplename.split("-")
     
     sampleloc = '/'.join(["data",link[-2],link[-3],spectraname])
     
     return self.db.open(sampleloc, 'r')

  def merging(self, cat1, cat2, **kwargs):

     return pd.merge(cat1, cat2, **kwargs)


if __name__ == '__main__':
  relab = Relab()
  cat = relab.retrieve_from("catalogues/", ft="xls")
  
  samplecat =  relab.dataframe(cat["Sample_Catalogue"], extract=False)
  spectracat = relab.dataframe(cat["Spectra_Catalogue"], extract=False)
  allcat = relab.merging(samplecat, spectracat, left_index=True, right_index=True)
  del samplecat, spectracat
  print(allcat.columns)
  meteorites = allcat[allcat["GeneralType"] == 'Meteorite']
  meteoritesVNIR = meteorites[meteorites["SpecCode"] == 'DHC-VNIR']
  
  spectrapaths = relab.retrieve_spectra(meteoritesVNIR.index, meteoritesVNIR.RelabFile)

# END