#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: plot_methods.py

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

#### MODULES #####

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from numpy import array, zeros, genfromtxt, loadtxt, ones
from itertools import product, combinations
from collections import deque
from os import path, mkdir
import sys
home = path.expanduser("~")
sys.path.append(path.join(home,"Ferramentas","Programas",""))
import myfuncs as mf

path1 = path.join(home,"Projetos","Taxonomia SDSS","PDS Archiving","")
path2 = path.join(home,"Dados","Catalogos","")

#label = ['s','u','b','v','w','x','p','z']
#label = ['u','g','r','i','z']
filters=[0.36,0.47,0.62,0.75,0.89]
#filters= [0.31, 0.32, 0.43, 0.545, 0.705, 0.86, 0.955, 1.055]

#############################################################
########### Orbital distribution of g-mode groups ###########
#############################################################

def load(filename, rng, norm=[3,0e0]):
    classes = map(list,genfromtxt(filename, delimiter=None,dtype=None, skiprows=1))
    
    I = rng[0]
    N = rng[1]
    
    d = deque()
    label = list()
    for each in classes:
        label.append(each[2])
        #phot = map(lambda i: i + norm[1], each[I:N+I])
        phot  = each[I:N+I]
        error = each[N+I:]
        phot.insert(norm[0],norm[1])
        error.insert(norm[0], 0e0)
        d.append([array(phot),array(error)])
        #d.append(mf.refl(array(color),array(error),norm[0]))

    return list(d), label

def dist_orb_groups():


     ### OPEN FILES ####

     ast_classf = open(path.join("Classification","asteroid_classf_q1.3_var0.01_MOC3q_no-err.dat"), "r").readlines()
     num, ap, ep, sinip = loadtxt("MOC3q_parameters.dat", unpack=True, dtype=str, usecols=[5,14,15,16]) 

     ### DATA ###

     ast_classf02 = dict()
     for ast in ast_classf:
         ast = ast.split()
         if len(set(ast[1:])) == 1 :
            ast_classf02[ast[0]] = ast[1]

     ap = dict(zip(num,ap))
     ep = dict(zip(num,ep))
     sinip = dict(zip(num,sinip))
     
     class_units = sorted(set(ast_classf02.values()))
     groups = sorted(set(tax_group.values()))
     #print(class_units,groups)

     ### PLOTS ###

     plt.figure(figsize=(16,18),dpi=80)
     gs = gridspec.GridSpec(4, 3)
     xy = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2],[3,0],[3,1],[3,2]]

     for n, g in enumerate(groups):
         a_l=[]; e_l=[]; sin_l=[]
         for obj in num:
             if obj in ast_classf02 and tax_group[ast_classf02[obj]] == g :
                a_l.append(ap[obj])
                sin_l.append(sinip[obj])
                e_l.append(ep[obj])

         plt.subplot(gs[xy[n][0],xy[n][1]])
         plt.hexbin(a_l,sin_l,gridsize=150,mincnt=1, bins='log')
         plt.xlim(2.0,3.7)
         plt.ylim(0.0,0.30)
         plt.text(3.55, 0.15, g,fontsize=12,fontweight='black')

         if xy[n][0] == 2 and xy[n][1] == 0: plt.ylabel('$sin(i_{p})$',fontsize=22,fontweight='black')


     plt.suptitle('$a_{p}$',fontsize=22,fontweight='black')

     #plt.subplot(gs[4,:])
     #cb=plt.colorbar(orientation='horizontal',fraction=0.10,pad=0.3,drawedges=False)
     #cb.set_label('log10(N)')
     plt.savefig("dist_sini_q1.3_var0.01_MOC3q_no-err.png",format='png')

##############################################################
########### Distribution of flags of g-mode groups ###########
##############################################################

def dist_flags():
    ID, classf = loadtxt("Classification/gmode_C_q1.3_var0.01_MOC3q_logr02.dat", unpack=True, dtype=str, usecols=[2,3])
    pars = open("MOC3q_parameters.dat", "r").readlines() 

    obs_tax = dict(zip(ID,classf))

    classes = sorted(set(classf))
    print(classes)

    '''fig = plt.figure(figsize=(18,20),dpi=90)
       gs = gridspec.GridSpec(5, 5)
       xy = [[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4],[2,0],[2,1],[2,2],[2,3],[2,4],\
            [3,0],[3,1],[3,2],[3,3],[3,4],[4,0],[4,1],[4,2],[4,3]]'''

    for m, T in enumerate(classes):
        cflag = zeros(60)
        for entry in pars:
            entry = entry.split()
            if obs_tax.has_key(entry[0]) and obs_tax[entry[0]] == T:
               flags = entry[17:]
               flags.pop(4)
               flags.pop(18-1)
               flags.pop(23-2)
               flags.pop(35-3)
               #print(len(flags))
               for n, each in enumerate(flags):
                   if each == '1': cflag[n] = cflag[n] + 1

        #print(cflag)
        if T == 'T15' or T=='T16':
           x = range(1,65)
           x.remove(5)
           x.remove(19)
           x.remove(24)
           x.remove(36)
           #print(len(x),len(cflag))
           fig = plt.figure(m,figsize=(17,7),dpi=60)
           #ax = fig.add_subplot(gs[xy[m][0],xy[m][1]])
           ax = fig.add_subplot(1,1,1)
           ax.bar(x, cflag, facecolor='#777777',  align='center')
           ax.set_ylabel('Ocurrences')
           ax.set_title(T)
           ax.set_xticks(x)

           plt.show()


#############################################################
################ Color Map of g-mode groups #################
#############################################################

def color_map(test="q1.2_z5.0_MOC",filename="MOC4_3quartile_refl.dat"):
    import random as rd

    rdnumber = lambda x, y: rd.gauss(x,y)

    ### OPEN FILES ####
    sdssid01, classf = loadtxt(path.join(home,"My Projects","G-mode","TESTS",test,"gmode1_"+lbl+".dat"), unpack=True,dtype=str,usecols=[2,3])
    sdssid02, u, u_err, r, r_err, i, i_err, z, z_err = loadtxt(path.join(home,"Projetos","G-mode","SDSSMOC","lists",filename), unpack=True, dtype=str, usecols=[1,2,3,4,5,6,7,8,9]) 
    tax, group = loadtxt(path.join(home,"My Projects","G-mode","TESTS",test,"clump_"+lbl+".dat"), skiprows=1, unpack=True, dtype=str, usecols=[0,1])

    ### DATA ###
    tax_group = dict(zip(tax,group))
    id_tax = dict(zip(sdssid01,classf))

    groups = sorted(set(tax_group.values()),reverse=True)

    #groups.remove('C')
    #groups.remove('S')

    ### PLOTS ###

    color={'C':'#000000','S':'#66CCCC','V':'#00CC00','D':'#FF0000','G':'#999900','L':'#CC0033',\
           'B':'#0000FF','A':'#9900FF','O':'#FFCC00','N0':'#FF99FF','N1':'#FF0099','N2':'#00FFCC'}

    for n in range(3):
  
        plt.figure(n+1,figsize=(12,13),dpi=70)
 
        for g in groups:
   
            g_u=deque(); r_g=deque(); i_r=deque(); z_i=deque()
  
            for i, obs in enumerate(sdssid02):
                if obs in id_tax and tax_group[id_tax[obs]] == g :
      
                  g_u.append(-2.5*(1e0 - rdnumber(logu[i],logu_err[i])) ) 
                  r_g.append(-2.5*((rdnumber(logr[i],logr_err[i]) - 1e0)) )
                  i_r.append(-2.5*(rdnumber(logi[i],logi_err[i]) - rdnumber(logr[i],logr_err[i])) )
                  z_i.append(-2.5*(rdnumber(logz[i],logz_err[i]) - rdnumber(logi[i],logi_err[i])) )

                if n == 0: 
                  plt.plot(u,r,color=color[g],marker='.',label=g,linestyle='none',alpha=0.8)
                  plt.xlabel("$Ru_{SDSS}$",fontsize=22)
                  plt.ylabel("$Rr_{SDSS}$",fontsize=22)

                if n == 1: 
                  plt.plot(r,i,color=color[g],marker='.',label=g,linestyle='none',alpha=0.8)
                  plt.xlabel("$Rr_{SDSS}$",fontsize=22)
                  plt.ylabel("$Ri_{SDSS}$",fontsize=22)


                if n == 2: 
                  plt.plot(i,z,color=color[g],marker='.',label=g,linestyle='none',alpha=0.8)
                  plt.xlabel("$Ri_{SDSS}$",fontsize=22)
                  plt.ylabel("$Rz_{SDSS}$",fontsize=22)
   
            plt.legend(loc=0,markerscale=4,numpoints=1)

    plt.show()

################################################################
########### groups median reflectances plotted in box ##########
################################################################

def box(data, lbl, grid):

    fig = plt.figure(figsize=(7,10),dpi=80)
    gs = gridspec.GridSpec(grid[0], grid[1])
    xy = list(product(range(grid[0]), range(grid[1])))

    n = 0
    for i, T in enumerate(data):
        a = plt.subplot(gs[xy[n][0],xy[n][1]])
        plt.setp(a.get_yticklabels(), visible=True)      
        plt.errorbar(filters,T[0],yerr=T[1],fmt='ko',linestyle='-',linewidth=2, label= "T"+str(i+1)+"--> "+str(lbl[i]))

        #for i,f in enumerate(filters): plt.text(f,0.3,label[i],fontsize=12)
        
        plt.ylim(0.2,1.8)
        plt.xlim(0.3,filters[-1]+0.15)
        
        if xy[n][0] == int(grid[0]/2) and xy[n][1] == 0: plt.ylabel('Normalized Reflectance',fontsize=13,fontweight='black')
        plt.legend(loc=0,prop={'size':10,'weight':'black'},numpoints=1,frameon=False)

        n += 1

    plt.suptitle('Wavelenght (microns)',fontsize=13,fontweight='black')
    plt.show()

#####################################################################
########### groups median reflectances plotted in vertical ##########
#####################################################################

def vertical(classes, lbl, q, d):

    shift = 0e0

    plt.figure(figsize=(4,18),dpi=40)

    for i in set(lbl):
        for n, T in enumerate(classes):
            if lbl[n] == i:
              plt.errorbar(filters,T[0]+shift,yerr=T[1],fmt='o',color='k',ecolor='k',linestyle='-',linewidth=2)
        
        plt.text(filters[-1]+0.04,T[0][-1]+shift,i,fontsize=11,fontweight='black')
        shift = shift + d

    plt.ylabel('Refletância Normalizada')
    plt.xlabel('comprimento de onda ($\mu m$)')

    import scipy.stats as scp_sts
    plt.text(0.5, 0.40, '$q_{1}$ = '+str(100*round(scp_sts.norm.cdf(q),3))+'%',fontsize=12,fontweight='black')
    plt.ylim(0e0,shift+d)
    plt.xlim(filters[0]-0.05,filters[-1]+0.1)

    plt.show()



def compare_tax_systems(file_class,templ,filename,convert="yes"):

    try:
        mkdir(path.join(filename,""))
    except OSError:
        pass

    gmode = map(list,genfromtxt(path.join("Classes",file_class), dtype=None, skip_header=1))

    sdss_wv = [0.36,0.47,0.62,0.75,0.89]
    

    n=0
    for gclass in gmode:
        z2 = list()
        n += 1
        plt.figure(n,figsize=(8,12),dpi=70)
        plt.xlim(xmax=1e0)

        g_refl, g_err = mf.logr_to_r(gclass[2:6],gclass[6:])
        g_refl.insert(1,1e0); g_err.insert(1, 0e0)

        for model in templ.keys():

            if convert == "yes":
               t_refl, t_err = mf.logr_to_r(templ[model],zeros(len(templ[model])))
               t_refl.insert(1,1e0); t_err.insert(1, 0e0)

            plt.plot(sdss_wv,t_refl,'rD',linestyle='-',linewidth=2)
            plt.text(sdss_wv[-1]+0.04,t_refl[-1],model,fontsize=11,color='r',fontweight='black')

            z2.append(sum(map(lambda x, x0: round((x - x0)**2, 8), g_refl, t_refl)))

        z2_min = min(z2)

        plt.errorbar(sdss_wv,g_refl,yerr=g_err,fmt='o',color='k',ecolor='k',linestyle='-',linewidth=2)

        plt.title("T"+str(n)+"--> "+model+": $Z_{2}$= "+str(z2_min))
        plt.text(sdss_wv[-1]+0.04,g_refl[-1],gclass[0],fontsize=11,fontweight='black')

        plt.savefig(path.join(filename,'T'+str(n)+file_class[6:-4]+'.png'),format='png')

def var_limit_plot():
    q1, vl, N, u, r, i, z = loadtxt(path.join(home,"Projetos","G-mode","tests","var_limit_test.txt"), unpack=True, skiprows=1)
    
    fig = plt.figure(figsize=(10,8),dpi=80)
    ax1 = fig.add_subplot(111)
    #plt.plot(vl,N,'kD',label="Number of Classes")
    ax1.plot(vl,u,'bD',label="u' filter last seed variance")
    ax1.plot(vl,r,'gD',label="r' filter last seed variance")
    ax1.plot(vl,i,'mD',label="i' filter last seed variance")
    ax1.plot(vl,z,'yD',label="z' filter last seed variance")
    ax1.legend(loc=2)
    #plt.plot(vl,N,'k-',label="Number of Classes")
    ax1.plot(vl,u,'b-',label="u' filter last seed variance")
    ax1.plot(vl,r,'g-',label="r' filter last seed variance")
    ax1.plot(vl,i,'m-',label="i' filter last seed variance")
    ax1.plot(vl,z,'y-',label="z' filter last seed variance")
    ax1.set_ylabel("$K*MAD$")
    ax1.set_ylim(0e0,0.03)

    ax2 = ax1.twinx()
    ax2.plot(vl,N,'kD',label="Number of Classes")
    ax2.legend(loc=4)
    ax2.plot(vl,N,'k-',label="Number of Classes")
    ax2.set_ylabel("N")
    ax2.set_ylim(5,25)

    ax1.set_xlabel("$X_{0}^2$")
    plt.show()

if __name__ != "main":
   d, label = load(path.join(home,"Projetos","G-mode","TESTS","q1.3_z4.7_MOC_num2","clump_q1.3_z4.7_MOC_num2.dat"), [3,4], [1,1e0])
   box(d, label, grid=[5,4])
   #vertical(d, label, 2.2, 0.7)
   #color_map()
   
