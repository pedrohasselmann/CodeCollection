#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: SDSSMOC4 fluxes
# Calcula os fluxos para o SDSSMOC4

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

from os import path
import zipfile
from numpy import array, sqrt, sinh, tanh, log, fabs

def SDSS_refl(mag, mag_err, sunmag, sunmag_err,norm=1):

    b = 1e-10*array([1.4,0.9,1.2,1.8,7.4])
    c = -0.4*log(10)

    refl_sun =  2e0*b*sinh(c*sunmag - log(b))
    refl     =  2e0*b*sinh(c*mag - log(b))/refl_sun


    refl_err_sun =  fabs( c*refl_sun*sunmag_err/ tanh(c*sunmag - log(b)) )
    refl_err     =  fabs( c*refl*mag_err/ tanh(c*mag - log(b)) )

    err = sqrt((refl_err/refl)**2 + (refl_err_sun/refl_sun)**2)
    
    return refl/refl[norm], err

home = path.expanduser("~")

sunmag= array([6.44,5.12,4.67,4.57,4.53])
sunmag_err = array([0.05,0.02,0.02,0.02,0.02])

# Abertura dos arquivos:
with zipfile.ZipFile(path.join(home,"Dados","Catalogos","ADR4_ident_filtered.zip"), "r") as MOC4zip:
     MOC4 = MOC4zip.open("ADR4_ident_filtered.dat", 'r')
     
output=open('ADR4_refl+mags2.dat', 'w').write

bad_flags = [5, 6, 13, 20, 25, 26, 33, 34, 36, 40, 46, 55]

for obs_moc4 in MOC4:

    try:
        data = obs_moc4.split()

        mag = array(map(float, data[19:29]))

        r, r_err = SDSS_refl(mag[::2],mag[1::2],sunmag,sunmag_err,1)
        
        flags = data[60:]
        
        if all([flags[bad] != '1' for bad in bad_flags]):
           write_refl=' {0[0]: .4f} {1[0]: .4f}  {0[1]: .4f} {1[1]: .4f}  {0[2]: .4f} {1[2]: .4f}  {0[3]: .4f} {1[3]: .4f} {0[4]: .4f} {1[4]: .4f}\n'.format(r, r_err)


           '''[0:6] --> SDSS asteroid ID
           [244:279] --> Number, code/name and flags
           [317:340] --> Heliocentric, Geocentric distances and phase angle
           [162:242] --> SDSS magnitudes
           [362:373] --> Absolute magnitude and Slope parameter
           [483:518] --> Proper orbital elements '''
        
           output(str(obs_moc4[0:6]+obs_moc4[244:279]+obs_moc4[361:373]+obs_moc4[317:340]+3*' '+obs_moc4[162:242]+3*' '+write_refl))
    except ValueError:
        pass

#END
