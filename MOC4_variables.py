#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: SDSSMOC4 fluxes
# Calcula os fluxos para o SDSSMOC4

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

from os import path
import zipfile

home = path.expanduser("~")

# Abertura dos arquivos:
with zipfile.ZipFile(path.join(home,"Dados","Catalogos","ADR4_ident_filtered.zip"), "r") as MOC4zip:
     MOC4 = MOC4zip.open("ADR4_ident_filtered.dat", 'r')
     
output=open('ADR4_logr+mags.dat', 'w').write

import myfuncs

for obs_moc4 in MOC4:

    try:
        data = obs_moc4.split()

        mag=[float(data[19+I]) for I in range(0,10,2)]
        mag_err=[float(data[20+I]) for I in range(0,10,2)]

        sunmag=[6.44,5.12,4.67,4.57,4.53]
        sunmag_err = [0.05,0.02,0.02,0.02,0.02]

        logr, logr_err =myfuncs.log_refl(mag,mag_err,sunmag,sunmag_err,1,0e0)

        write_refl=' {0[0]: .4f} {1[0]: .4f}  {0[1]: .4f} {1[1]: .4f}  {0[2]: .4f} {1[2]: .4f}  {0[3]: .4f} {1[3]: .4f} {0[4]: .4f} {1[4]: .4f}\n'.format(logr, logr_err)


        '''[0:6] --> SDSS asteroid ID
           [244:279] --> Number, code/name and flags
           [317:340] --> Heliocentric, Geocentric distances and phase angle
           [162:242] --> SDSS magnitudes
           [362:373] --> Absolute magnitude and Slope parameter
           [483:518] --> Proper orbital elements '''
        
        output(str(obs_moc4[0:6]+obs_moc4[244:279]+obs_moc4[361:373]+obs_moc4[317:340]+3*' '+obs_moc4[162:242]+3*' '+write_refl))
    except IndexError:
        pass

#END
