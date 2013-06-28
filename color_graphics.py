#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: color_graphics.py
# Gráficos no espaço cor-cor.

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division
try:
   xrange = xrange
   # We have Python 2
except:
   xrange = range
   # We have Python 3

# Importar Modulos:
import numpy as np
import matplotlib.pyplot as pylab
import sys
sys.path.append('/home/usuario/Analise/TaxonomiaSDSS/')
import myfuncs

# Abertura dos arquivos:
cat=str(raw_input('What catalog do you want to use? ')).rstrip()
data=open('ast2MASS+'+cat+'_best-obs.dat', 'r').readlines()

tax_class=['O','V','A','Q','L','D','X','C','S']
tax_type={'L':'mo','A':'ro','V':'go','S':'bo','Q':'yo','O':'y*','D':'b*','X':'k*','C':'ko'}
tax_type2={'L':'m','A':'r','V':'g','S':'b','Q':'y','O':'y','D':'b','X':'k','C':'k'}

# Contando o numero de objetos daquele tipo taxonomico:
length=len(data)

# lendo os dados necessarios do arquivo ast2MASSMOC4:
fluxs=[]; slops=[]
for obs in data:
  J_mag=float(obs[34:40]); J_error=float(obs[41:47])
  H_mag=float(obs[47:53]); H_error=float(obs[54:59])
  Ks_mag=float(obs[60:66]); Ks_error=float(obs[67:72])
  fluxs.append(myfuncs.fluxes([J_mag, J_error, H_mag, H_error, Ks_mag, Ks_error],[3.32,0.03,3.42,0.03,3.325,0.03],2))
  slops.append(myfuncs.slopes([J_mag, J_error, H_mag, H_error, Ks_mag, Ks_error],[3.32,0.03,3.42,0.03,3.325,0.03],[1.25,1.65,2.17]))

# Plotando gráfico:

n,j=0,0

for obs in data:
  if float(obs[73:80])  < 20.000:
    J_H=float(obs[34:40]) - float(obs[47:53]) - 0.258
    H_Ks=float(obs[47:53]) - float(obs[60:66]) - 0.096
    for tax in tax_class:
      if obs[135:136].strip()==tax:
        j=j+1
# Gráfico de Fluxo Ks vs Fluxo J para observar a dispersão:
        pylab.figure(1,figsize=(11,6),dpi=100)
        pylab.suptitle('Grafico Fluxo-Fluxo')
        pylab.xlabel('Flux Ks/H'); pylab.ylabel('Flux J/H')
#        pylab.plot(fluxs[n][4],fluxs[n][0],tax_type[tax],label=tax)
        pylab.errorbar(fluxs[n][4],fluxs[n][0],yerr=fluxs[n][1],xerr=fluxs[n][5],fmt=tax_type[tax],ecolor=tax_type2[tax],label=tax)

# Gráfico cor-cor:
        pylab.figure(2,figsize=(11,6),dpi=100)
        pylab.suptitle('Grafico cor-cor')
        if float(obs[73:80])  < 17.000:
          pylab.subplot(211)
          pylab.xlabel('$(H - Ks)_{2MASS}$'); pylab.ylabel('$(J - H)_{2MASS}$')
          pylab.plot(H_Ks,J_H,tax_type[tax],label=tax)

        if float(obs[73:80])  < 20.000:
          pylab.subplot(212)
          pylab.xlabel('$(H - Ks)_{2MASS}$'); pylab.ylabel('$(J - H)_{2MASS}$')
          pylab.plot(H_Ks,J_H,tax_type[tax],label=tax)
          pylab.xlim(-0.6,1.1); pylab.ylim(-0.5,1.5)

# Gráfico de Fluxo Ks vs Magnitude V para entender se a dispersão em Ks e J depende do brilho:
        pylab.figure(3,figsize=(11,6),dpi=100)
        pylab.suptitle('Grafico de incerteza por brilho')
        pylab.subplot(211)
        pylab.ylabel('Error Ks'); pylab.xlabel('V Mag')
        pylab.plot(float(obs[73:79]),float(obs[67:72]),tax_type[tax],label=tax)
        pylab.subplot(212)
        pylab.ylabel('Error J'); pylab.xlabel('V Mag')
        pylab.plot(float(obs[73:79]),float(obs[41:46]),tax_type[tax],label=tax)
    n=n+1
print(n,j)

# Mostrar tudo
pylab.show()

#END