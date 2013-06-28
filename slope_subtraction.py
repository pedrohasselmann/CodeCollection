#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: S3OS2 slope subtraction

# Modules:
import numpy as np
import scipy as scp
import scipy.interpolate as intp
import matplotlib.pyplot as plt
import cookb_signalsmooth as smooth


# Input data:
arq = np.loadtxt(str("S3OS2/designations_s3os2.dat"), dtype=str, unpack=True)

t = 'sm'
o = 'n'
par = 260
step = 0.01

# Output data:
if o == 'y':
  out = open("s3os2_channel.dat", 'w')
  out.write('Data: S3OS2 Smoothing method: Blackman smoothing signal  window_len='+str(par)+'\n')

n = 0
spc_slopeless=[]

for arq_name in arq:
  n = n + 1
  output=''
  wv, refl, error = np.loadtxt(str('S3OS2/'+arq_name), dtype=float, unpack=True)
  
  wv    = np.trim_zeros(wv)
  refl  = np.trim_zeros(refl)
  error = np.array(error[0:len(wv)])

# Number of channels:
  ch_step = int(len(refl)/((0.92 - 0.5)/step))

# Channels position:
  ch_pos = np.arange(0,len(refl),ch_step)

# Spectral smoothing signal:
  if t == 'sm':
    ''' 240 < window_len < 290 '''
    spectra = smooth.smooth(refl, window_len=par, window='blackman')

# Spline fit to the spectra:
  if t == 'sp':
    ''' 40 < s < 200 '''
    spline = intp.UnivariateSpline(wv,refl,w=1/error, k=3, s=par)
    print(spline.get_residual())
    spectra =spline.__call__(wv)/spline.__call__(0.55)

# Polynomial fit to the spectra:
  if t == 'pl':
    ''' deg = 7 or 8 '''
    poly_coefs = np.polyfit(wv, refl, deg=par)
    spectra = np.polyval(poly_coefs, wv)/np.polyval(poly_coefs,0.55)

# Fitting a line equation to the data:
  #line_coefs = np.polyfit(wv, spectra, deg=1)
  #line = np.polyval(slope_coefs, wv)/np.polyval(slope_coefs, 0.55)
  
  line   = lambda a,x : 1.0 + a*(x - 0.55)
  err_line = lambda a, x, y, error: (y - line(a, x))/error

  slope = scp.optimize.leastsq(err_line, x0 = 0.0, args=(wv,refl,error))
  slope = float(slope[0])

# Output channeled spectra:
  if o == 'y':
   for ch in spectra[ch_pos]: output = output + '{0:.3f} '.format(ch)
   out.write('{0:5} {1:15}     {2:+.3f}  '.format(arq_name[0:5],arq_name[6:],slope)+'  '+output+'\n')

# Extracting slope:
  spc_slopeless.append(spectra - line(slope,wv))


# Plot:
  if o == 'n':
   plt.plot(wv, refl, 'k-')
   plt.plot(wv[ch_pos], spectra[ch_pos], 'r-') 
   plt.plot(wv, line(slope,wv), 'b--')
   if n == 4:
    plt.show()
    n = 0

# call PCA

# END

