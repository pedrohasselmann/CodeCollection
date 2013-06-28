#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: spectra-bandpass_conv.py
# Interpolação e convolução.

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division
try:
   xrange = xrange
   # We have Python 2
except:
   xrange = range
   # We have Python 3

# Importar bibliotecas:
import numpy, pylab, sys
from scipy import interpolate as itp
from scipy import integrate as intg

# Abertura dos arquivos:
drct1='//media//A810D30810D2DC7E//Documents and Settings//Administrador//Meus documentos//Projetos//SDSStaxonomies//Analise//ugriz+JHKs//'
drct2='//media//A810D30810D2DC7E//Documents and Settings//Administrador//Meus documentos//Astronomia//Catalogos//Gaffey Meteorite Collection//'

spectra=open(drct2+'mgp120.tab','r')

# Lendo arquivo do espectro meteorítico:
wv_spec=[]
refl=[]
for line in spectra:
   try:
     wv_spec.append(float(line[0:7].rstrip())/1000.0)
     refl.append(float(line[8:17].rstrip()))
   except (RuntimeError, TypeError, NameError, ValueError):
      pass
del line
spectra.close()
# Espectro integrado:
spectra_intg=intg.simps(y=refl,x=wv_spec)

'''Interpolação do espectro meteorítico nos pontos de comp. de onda em que os valores da banda de passagem foram avaliados.
   Interpolar apenas uma das suas funções diminui a propagação do erro na convolução e portanto determinação do fluxo.'''

# Criação da função de interpolação:
refl_itp=itp.interp1d(wv_spec,refl)

refl_norm=[]
[refl_norm.append(item/refl_itp(1.25)) for item in refl]

n=0
#bandpass_name=[]

# Letra das bandas de passagem de entrada:
#bandpass_name.append(str(raw_input('Input the bandpass letter: \n')))
#while bandpass_name[n] != '':
#  bandpass_name.append(str(raw_input(' and ')))
#  n=n+1
bandpass_name=['J','H','Ks']
fluxes=[]
fluxes_norm=[]

wv_center=[1.25,1.65,2.17]
pylab.figure(1,figsize=(11,6),dpi=100)

# Inicio do loop______________________________________________________________
n=0
for bandpass in bandpass_name:
  bp=open(drct1+bandpass+'-band_eff.dat','r')

# Lendo arquivo da eficiencia da banda de passagem por comprimento de onda:
  wv_bp=[]
  eff=[]
  for line in bp:
    try:
      wv_bp.append(float(line[9:14].rstrip()))
      eff.append(float(line[18:24].rstrip()))
    except (RuntimeError, TypeError, NameError, ValueError):
       pass

  eff_intg=intg.simps(y=eff,x=wv_bp)

# interpolacao da eficiencia da banda:
  eff_itp=itp.interp1d(wv_bp,eff)

# Pontos do espectro que estao dentro do limite dos regiao da banda:
  wv_spec_lmt=[]
  print(wv_bp[0],wv_bp[len(wv_bp)-1])
  for item in wv_spec:
    if item >= wv_bp[0] and item <= wv_bp[len(wv_bp)-1]:
      wv_spec_lmt.append(item)

# Funcao de Convolucao:
# Calculando a funcao de convolucao usando f(x)*R(x)=M(x):
  conv_func=[]
  for x in wv_spec_lmt:
    conv_func.append(refl_itp(x)*eff_itp(x))

##########################################

# Integracao da funcao de convolucao:
  flux=0.0
  h=float(( wv_spec_lmt[len(wv_spec_lmt)-1] - wv_spec_lmt[0])/len(wv_spec_lmt))
  flux=intg.simps(y=conv_func,x=wv_spec_lmt)/eff_intg

  fluxes.append(float(flux))
  fluxes_norm.append(float(flux)/fluxes[0])

# gráfico de comparação:
  pylab.plot(wv_spec,refl_norm,'b-',wv_bp,eff,'r-',wv_center[n],fluxes_norm[n],'ro')
  pylab.xlim(0.3,2.6)

  n=n+1
  bp.close()
  del eff,line
# Fim do loop________________________________________________________________

print(fluxes, fluxes_norm)

# Grafico dos fluxos versus espectros:

# Gráfico de comparação:
answer1=raw_input('Do I print a comparative graphic between the interpolation and the data? (y/n, default=no)')
if answer1=='y':
  pylab.figure(2,figsize=(10,8),dpi=100)
  pylab.subplot(211)
  pylab.plot(wv_spec,refl)
  pylab.xlim(1.0,2.5)
  pylab.ylim(0.170,0.178)
  pylab.subplot(212)
  pylab.xlim(1.0,2.5)
# A função de interpolação nos pontos avaliados para a banda de passagem:
  pylab.plot(wv_bp,refl_itp(wv_bp))
  pylab.xlim(1.0,2.5)

pylab.show()

del wv_bp,flux,fluxes,fluxes_norm,refl_norm,item

# END.