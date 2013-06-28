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
import matplotlib.pyplot as plt

# input:
gaussians = [                                \
            [[3, 3] , [0.5, 0.25] ,     0e0],   \
            [[7, 5] , [1, 0.25] , 3e0*pi/4e0],   \
            [[3, 8] , [1, 0.25] ,     pi/4e0]    \
            ]

# Random points from multivariate gaussian distributions:

x_sample = deque()
y_sample = deque()
theta_zero = ones(500)

for m, d, theta in gaussians:
    x = rd.normal(m[0], d[0], 500)
    y = rd.normal(m[1], d[1], 500)

    if theta != 0e0:
       vecl = sqrt((x - m[0])**2 + (y - m[1])**2)
       theta_zero[x < m[0]] = 2e0*pi - arccos((x - m[0])/vecl)
       theta_zero[x >= m[0]] = arccos((x - m[0])/vecl)
       theta = theta + theta_zero

       x_sample.append( vecl * cos(theta) + m[0])
       y_sample.append( vecl * sin(theta) + m[1])
       
    else:
       x_sample.append(x)
       y_sample.append(y)


# random points adding noise.
x_sample.append( 10 * rd.rand(500) )
y_sample.append( 10 * rd.rand(500) )

# Change array format:
x_sample = ravel(x_sample)
y_sample = ravel(y_sample)

plt.plot(x_sample,y_sample,"b.")
plt.show()
