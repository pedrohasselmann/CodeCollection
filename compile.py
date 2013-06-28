#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: compile.py
# Author: Pedro Henrique Aragão Hasselmann
# Compila scripts de python para .pyc e .exe

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division
try:
   xrange = xrange
   # We have Python 2
except:
   xrange = range
   # We have Python 3

import sys
import os
import py_compile
import distutils
from cx_Freeze import setup, Executable, build_exe

script=str(raw_input("Name of script to compile (.pyc): "))
answer1=str(raw_input("Do you also want to create a executable (.exe)? (y/n) "))

py_compile.compile(script,cfile=script+'c')

if answer1=='y':
#  os.system("cxfreeze -OO -s "+script+" --target-dir EXE")
  setup(name="EXE", version="1.0", executables=[Executable(script)])

# END
