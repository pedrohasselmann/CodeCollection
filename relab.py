#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: binarytree.py
# Binary Tree
# Author: Pedro H. A. Hasselmann

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

from os import path
import cPickle as pkl

home = path.expanduser("~")
root = path.join(home,"Catalogues")

class Relab:

  import pandas as pd

  def __init__(self):
     import zipfile

     # Create a ZipFile Object for Relab Database:
     with zipfile.ZipFile(
                        path.join(root,"Relab_2012Dec.zip")
                        ) as relab:
      self.db = relab

  def dataframe(self, filename, sheet):
     from numpy import genfromtxt, loadtxt
     
     f = pd.read_excel(filename, sheet, header=1, index_col=1, na_values=" ")
     return f

if __name__ == '__main__':
  relab = Relab()