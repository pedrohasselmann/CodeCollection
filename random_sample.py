#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: random_sample.pya
# Produce a random syntetic sample of N-gaussians

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

# IMPORT
from math import pi
from numpy import random as rd
from numpy import ones, ravel, sqrt, arccos, cos, sin
from collections import deque

# Random points from multivariate gaussian distributions:
N = 1000
M = 100

def simul_gauss(x_sample, y_sample, GN=20):
   # simulate the gaussians:

   gaussians = deque()
   for i in xrange(GN):
       x = rd.randint(1, M-1)
       y = rd.randint(1, M-1)
    
       dx = sqrt(M) * rd.ranf()
       dy = sqrt(M) * rd.ranf()
       
       align = 0e0 #pi * rd.ranf() 
       
       gaussians.append([[x, y], [dx, dy], align])

   theta_zero = ones(N)
       
   for m, d, theta in gaussians:
       print(m, d, theta)
       x = rd.normal(m[0], d[0], N)
       y = rd.normal(m[1], d[1], N)

       if theta != 0e0:
          print(theta_zero[x < m[0]].shape, theta_zero[x >= m[0]].shape)
          vecl = sqrt((x - m[0])**2 + (y - m[1])**2)
          theta_zero[x < m[0]]  = 2e0*pi - arccos((x - m[0])/vecl)[x < m[0]]
          theta_zero[x >= m[0]] = arccos((x - m[0])/vecl)[x >= m[0]]
          theta = theta + theta_zero

          x_sample.append( vecl * cos(theta) + m[0])
          y_sample.append( vecl * sin(theta) + m[1])
       
       else:
          x_sample.append(x)
          y_sample.append(y)

   return x_sample, y_sample
          
def simul_noise(x_sample, y_sample):

   # random points adding noise.
   x_sample.append( M * rd.rand(N) )
   y_sample.append( M * rd.rand(N) )

   # Change array format:
   x_sample = ravel(x_sample)
   y_sample = ravel(y_sample)
   
   return x_sample, y_sample

##### EDIT HERE #####

if __name__ == "__main__":
  import matplotlib.pyplot as plt
  
  x, y = deque(), deque()
  x, y = simul_gauss(x, y)
  x, y = simul_noise(x, y)

  plt.plot(x, y, "k.")
  plt.show()
