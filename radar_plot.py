#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: radar_plot.py
# author: Pedro Henrique A. Hasselmann
# date: August 2012

# Escrevendo em python3 e usando python2.7:
from __future__ import print_function, unicode_literals, absolute_import, division

from numpy import loadtxt, arange, mean, std
from os import path, sep

class RadarAnalysis:

      def __init__(self):
     
          if __name__ == '__main__':
             print("Main.")

          else:
             print("Imported.")

          pth = sep + path.join("home","hassel","Dados","Catalogos","RADAR_V18.zip")
           
          if path.isfile(pth):
             import zipfile

             with zipfile.ZipFile(pth, "r") as radarcat:
                  radardata = radarcat.open(path.join("EAR_A_5_DDR_RADAR_V18_0","data","radar.tab")).readlines()
                  astnum = [ID[0:7].strip() if int(ID[0:7]) != 0 else ID[25:35].strip() for ID in radardata]
                  cpol_ratio = [float(data[58:62]) for data in radardata]
                  cpol_error = [float(data[63:67]) for data in radardata]

          self.polratio = dict(zip(astnum,cpol_ratio))
          self.cpol_err = dict(zip(astnum,cpol_error))

      def LoadObjects(self,filename):

          pth = sep + path.join("home","hassel","Projetos","Curvas de Fase","Resurfacing",filename)

          if path.isfile(pth):
             objs = loadtxt(pth,dtype=str,delimiter=",")
           
          return objs
 
      def Plot(self,objlist,lbl):

          import matplotlib.pyplot as plt
          from scipy.stats import gaussian_kde

          sample = list()
          for ast in objlist:
              if self.polratio.has_key(ast) and self.polratio[ast] != 9.99: 
                 sample.append(self.polratio[ast])
                 print(ast, self.polratio[ast], self.cpol_err[ast])

          dist = gaussian_kde(sample)

          x = arange(0e0,0.7,0.01)
          #plt.hist(sample, bins = 7, normed=True, label=lbl)
          plt.plot(x,dist.evaluate(x)/max(dist.evaluate(x)),label=lbl)
          #plt.fill_between(x,dist.evaluate(x)/max(dist.evaluate(x)),0)
          plt.xlabel("SC/OC")
          plt.ylabel("Frequency")

          print(mean(sample), std(sample))
          return sample

      def view(self):
          import matplotlib.pyplot as plt
          plt.legend(loc=0)
          plt.ylim(0e0,1.2)
          plt.show()
      
      def KStest(self,s1,s2):
          from scipy.stats import ks_2samp
          print('Two-Sample KS test: ',ks_2samp(s1,s2)[1])
           
if __name__ == '__main__':
  
  a = RadarAnalysis()
  
  Qnum = a.LoadObjects("Qtypes_NEAs.txt")
  Snum = a.LoadObjects("Stypes_NEAs.txt")

  s1 = a.Plot(Qnum,"Q-types density distribution")
  s2 = a.Plot(Snum,"S-types density distribution")
  
  a.view()
  a.KStest(s1,s2)