#!/usr/bin/python
# -*- coding: utf-8 -*-

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

from numpy import sin, tan, exp, log10, power, radians

def HGmag(H,G,ph):

    # H-G phase function system

    ph = radians(ph)

    w = exp(- 90.56*tan(ph/2e0)**2)
  
    f = 0.119 + 1.341*sin(ph) - 0.754*sin(ph)**2
  
    F1 = w*(1e0 - 0.986*sin(ph)/f) + (1e0- w)*exp(-3.332*power(tan(ph/2e0),0.63))
    
    F2 = w*(1e0 - 0.238*sin(ph)/f) + (1e0 - w)*exp(-1.862*power(tan(ph/2e0),1.218))
    
    return H - 2.5*log10((1 - G)*F1 + G*F2)

