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

def ajust(wv, 
          refl, 
          par,
          norm = None,
          coefs= None, 
          ):

    from numpy import polyval, polyfit

    poly_coefs = polyfit(wv, refl, deg=par)
    if coefs ==  None: coefs = poly_coefs
        
    if norm: 
      spectra = lambda x : polyval(poly_coefs, x)/polyval(coefs,norm)
    else:
      spectra = lambda x : polyval(poly_coefs, x)
      
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
    
    if wv == None: 
      wv = arange(*step)
      self.step = step
    else:
      self.step = (wv[0],wv[-1], wv[0]-wv[1])

    # Fit a polynomial over the spectra:
    self.fit, coef = ajust(wv, refl, par, norm=norm)
    if error != None: self.std = spline(wv, error, s=s)
    

  def converter(self,
                wv_band,
                sens,
                ):

   ''' Calibrated continuum spectra converted to a discreet photometric system. '''

   from scipy import integrate as intg
   from numpy import argmin, fabs
   
   wv_band = 1e-4*wv_band

   low, up = 0,  len(wv_band)
   if self.step[0] > wv_band[0]:  low = argmin(fabs(wv_band - self.step[0]))
   if self.step[1] > wv_band[-1]:  up = argmin(fabs(wv_band - self.step[1]))

   # Convolution of the spectra with each bandpass (sensitivity):
   sens, wv_band = sens[low:up], wv_band[low:up]
   # Integral of sensitivity
   band_integral = intg.simps(y=sens,x=wv_band)

   # Filter convolution
   conv_profile = self.fit(wv_band)*sens
   if getattr(self, 'std', None): 
     conv_spread  = self.std(wv_band)*sens

   # Calculate Reflectance:
   refl_band = intg.simps(y=conv_profile,x=wv_band)/band_integral
   
   if getattr(self, 'std', None): 
     std_band = intg.simps(y=conv_spread,x=wv_band)/band_integral               
     return refl_band, std_band
     
   else:
     return refl_band


if __name__ == "__main__":
  pass

# END
  