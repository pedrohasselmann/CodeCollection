#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: Spectrophotometric_converter.py
# author: Pedro Henrique A. Hasselmann
# date: November 2013

# Escrevendo em python3 e usando python2.7:
from __future__ import print_function, unicode_literals, absolute_import, division

### MODULES ####
from os import path
import cPickle as pkl

home = path.expanduser("~")

def pickle(query):
   
    output = open("bus_templates.pkl",'wb')   
    pkl.dump(query,output, 2)
    output.close()

def unpickle(filename="bus_templates.pkl"):  

    inputed = open(filename,'rb')  
    rec = pkl.load(inputed)   
    inputed.close()   
    return rec

def ajust(wv, 
          refl, 
          par, 
          coefs=None, 
          norm
          ):

    from numpy import polyval, polyfit

    poly_coefs = polyfit(wv, refl, deg=par)
    if coefs ==  None: coefs = poly_coefs
    spectra = lambda x : polyval(poly_coefs, x)/polyval(coefs,norm)
    return spectra, poly_coefs

class Spectro:


  def __init__(self, 
               wv, 
               refl,
               error=None,
               norm=0.55, 
               step=(0.4350,0.9250,0.0025),
               par=9,
               s=0,
               ):

    from scipy.interpolate import UnivariateSpline as spline
    
    if wv == None: wv = arange(*step)

    # Fit a polynomial over the spectra:
    self.fit, coef = ajust(wv, refl, par, norm=norm)
    self.std = spline(wv, error, s=s)
    
    self.step = step
    

  def __iter__(self,
               bandpass, 
               ):

   ''' Calibrated continuum spectra converted to a discreet photometric system. '''

   from scipy import integrate as intg
   from numpy import loadtxt
   

   # Convolution of the spectra with each bandpass (sensitivity):

   wv_band, sens = *bandpass

   if wv_band[0] > self.step[0] and wv_band[-1] < self.step[1]: # Criteria to check either filters are inside the spectral region or not.

     # Integral of sensitivity
     wv_band = 1e-4*wv_band
     band_integral = intg.simps(y=sens[:len(wv_band)],x=wv_band)

     # Filter convolution
     conv_profile = self.fit(wv_band)*sens
     conv_spread  = self.std(wv_band)*sens
     
   else:
     return

   # Calculate Reflectance:
   refl_band = intg.simps(y=conv_profile,x=wv_band)/band_integral
   std_band = intg.simps(y=conv_spread,x=wv_band)/band_integral               

   return refl_band, std_band


if __name__ == "__main__":
  spectro = Spectro()

# END
  