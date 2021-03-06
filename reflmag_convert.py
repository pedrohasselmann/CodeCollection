#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: Flux function
# Funções para calcular as cores, fluxos e slopes das bandas u'g'r'i'z.

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

#### IMPORT MODULES #####

from numpy import array, zeros, sqrt, sinh, tanh, log, fabs

''' Sun Magnitudes for u'g'r'i'z' (SDSS.org):
      M(g)= +5.12  (+/-0.02)
      u-g = +1.43  (+/-0.05)
      g-r = +0.44  (+/-0.02)
      r-i = +0.11  (+/-0.02)   
      i-z = +0.03  (+/-0.02)
      u-g = +1.32
      g-r = +0.45
      g-i = +0.55
      g-z = +0.59 '''

#sunmag = array([-0.015, -0.026, -0.015, 0e0, 0.011, 0.009, 0.014, 0.012])
#sunmag_err = array([0e0, 0e0, 0e0, 0e0, 0e0, 0e0, 0e0, 0e0])

#___________________Normalized Reflectances_____________________________________________
def refl_pogson(mag,mag_err,norm):

    '''Calculate the refletances and its absolute errors from a list of magnitudes.
     Nomalized at [norm] band.
     The input must be a list. And [norm] is a integer number, locating where is 
     normalization band in the list.'''
    
    refl1 = 10.0**(0.4*((mag - mag[norm]) - (sunmag - sunmag[norm])))

    error=sqrt(mag_err**2 + mag_err[norm]**2 + sunmag_err[norm]**2 + sunmag_err**2)
    refl_err = (0.9210*error*(1.000 + 0.4605*error))

    return refl/refl[norm], refl_err

#___________________Log Reflectance (Carvano et al. 2010)_________________________________
def log_refl(mag,mag_err,sunmag,sunmag_err,norm,norm_value=1e0):

    '''Calculate the refletances and its absolute errors from a list of magnitudes.
     Nomalized at [norm] band.
     The input must be a list. And [norm] is a integer number, locating where is 
     normalization band in the list.'''

    color = - 0.4*((mag - mag[norm]) - (sunmag - sunmag[norm]))
    lr = color + norm_value
    lr_err = 0.4*sqrt(mag_err**2 + mag_err[norm]**2 + sunmag_err[norm]**2 + sunmag_err**2)

    return lr, lr_err

#___________________Log Reflectance to Reflectance (Carvano et al. 2010)_________________________________
def logr_to_r(logr,lr_err,norm_value=1e0):

    '''Transform log reflectance back to reflectance'''

    refl = 10**(logr - norm_value)

    # Relative errors (Roig et al. 2006)

    refl_err =  (0.9210/0.4)*lr_err*(1.000 + (0.4605/0.4)*lr_err)

    return refl, refl_err

#________________ SDSS asinh Reflectances (Lupton)_____________________________________
def SDSS_refl(mag, mag_err, sunmag, sunmag_err,norm):

    b = 1e-10*array([1.4,0.9,1.2,1.8,7.4])
    c = -0.4*log(10)

    refl_sun =  2e0*b*sinh(c*sunmag - log(b))
    refl     =  2e0*b*sinh(c*mag - log(b))/refl_sun


    refl_err_sun =  fabs( c*refl_sun*sunmag_err/ tanh(c*sunmag - log(b)) )
    refl_err     =  fabs( c*refl*mag_err/ tanh(c*mag - log(b)) )

    err = sqrt((refl_err/refl)**2 + (refl_err_sun/refl_sun)**2)
    
    return refl/refl[norm], err


        
