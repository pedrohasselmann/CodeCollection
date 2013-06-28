#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: packdesig.py
# author: Pedro Henrique A. Hasselmann
# date: August 2012

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

def give_number(letter):
    
    try:
     int(letter)
     return letter
    except ValueError:
     if letter.isupper():
      return str(ord(letter) - ord('A') + 10)
     if letter.islower():
      return str(ord(letter) - ord('a') + 36)

def convert_design(packed, conn='_'):
  '''
    Convert the packed designation format to formal designation.
  '''
  try:
    packed = str(packed).strip()
  except ValueError:
    print("ValueError: Input is not convertable to string.")

  if packed.isdigit() == True: desig = packed.lstrip('0') # ex: 00123
  
  if packed[0].isdigit() == False: # ex: A7659 = 107659

    if packed[1:].isdigit() == True: # ex: A7659
      desig = give_number(packed[0]) + packed[1:]
      
    elif packed[1:3].isdigit() == True:  # ex: J98SG2S = 1998 SS162
      if packed[4:5].isdigit() == True and packed[4:5] != '00':
        desig = give_number(packed[0]) + packed[1:3] + conn + packed[3] + packed[-1] + packed[4:5]
      elif packed[4:5] == '00':
        desig = give_number(packed[0]) + packed[1:3] + conn + packed[3] + packed[-1]
      elif packed[4:5].isdigit() == False:
        desig = give_number(packed[0]) + packed[1:3] + conn + packed[3] + packed[-1] + give_number(packed[4]) + packed[5]
      
    elif packed[2] == 'S': # ex: T1S3138 = 3138 T-1     
      desig = packed[3:] + conn + packed[0] + '-' + packed[1]
      pass
  
  return desig

def convert_date(packdt):

  '''
    Convert the packed year format to standard year.
  '''
  
  try:
    packdt = str(packdt).strip()
  except ValueError:
    print("ValueError: Input is not convertable to string.")    
  
  '''  
     Month     Day      Character         Day      Character
                     in Col 4 or 5              in Col 4 or 5
   Jan.       1           1             17           H
   Feb.       2           2             18           I
   Mar.       3           3             19           J
   Apr.       4           4             20           K
   May        5           5             21           L
   June       6           6             22           M
   July       7           7             23           N
   Aug.       8           8             24           O
   Sept.      9           9             25           P
   Oct.      10           A             26           Q
   Nov.      11           B             27           R
   Dec.      12           C             28           S
             13           D             29           T
             14           E             30           U
             15           F             31           V
             16           G

   Examples:

   1996 Jan. 1    = J9611
   1996 Jan. 10   = J961A
   1996 Sept.30   = J969U
   1996 Oct. 1    = J96A1
   2001 Oct. 22   = K01AM
  '''
  
  return '/'.join([give_number(packdt[0]) + packdt[1:3],give_number(packdt[3]),give_number(packdt[4])])