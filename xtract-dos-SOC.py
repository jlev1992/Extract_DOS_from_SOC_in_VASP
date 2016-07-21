from __future__ import print_function
import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from StringIO import StringIO
import sys, os

# Hello! #
################
# This sript is designed to read the DOSCAR file from a VASP SOC run with LORBIT = 11 activated
# Please gather the DOSCAR file in the directory where you run this script
# Run the scirpt and produce a series of output files organized by ion number
# Eah can be plotted individually to examine the ion and orbital behavior of the DOS
# Cheers!
################

#Written By Joshua Leveillee: 2015


### Read inputs ###
NEDOS = input('What is NEDOS (from INCAR):     ')
FWHH = input('what is the spectral boradening (recommend between 0.1 and 0.4)?:    ')
num_ions = input('how many ions in POSCAR file?:     ')
for k in range(0,num_ions+1):
    print(k)
    m = open("DOSCAR","r")
    g = open("ion_data.txt","w+")
    intro = 6+(k*NEDOS)+k
    for i, line in enumerate(m):
        if (i >= intro) and (i <= NEDOS+intro-1):
            g.write(line) #write data to output file in xmgrace format (-nxy)
        else:
            #print(i,' ',"pass")
            pass
    lines = file('ion_data.txt','r').readlines()
    s = len(lines)
    del lines[s-1]
    file('ion_data.txt','w').writelines(lines)
    
            
            
###################
    input_file = "ion_data.txt" #raw_input("Type the name of the Density of States file:    ")
    data_set = np.loadtxt(input_file)#, skiprows=0)
    energy_values = data_set[:,0] # ~ create an array of the energy values

    import re # Read fermi-energy from OUTCAR
    print('Reading OUTCAR ...')
    hand = open('OUTCAR')
    for line in hand:
        line = line.rstrip()
        if re.search('E-fermi', line) :
            A = line
    E_fermi = float(re.findall(r"[-+]?\d*\.\d+|\d+", A)[0]) # Save fermi-leveil in variable B
    print('Read form OUTCAR: Fermi Energy = ',E_fermi)

    for i in range(0,len(energy_values)):
        energy_values[i] = energy_values[i] - E_fermi

    dE = energy_values[1]-energy_values[0] # ~ Calculate energy grid spacing in DOSCAR
    #FWHH = input('what is the spectral boradening?:    ')

    # Open or create the output pile
    f = open("ion_"+str(k)+".txt","w")
    if k == 0:
        vec = [1]
    elif k > 0:
        vec = [1,5,9,15,17,21,25,29,33]
    for l in vec:#,5,17]:#range(1,len(data_set[0,:])): #Loop through the columns in parsed DOSCAR

        dos_delta = data_set[:,l] # ~ create an array of the DOS
        initial_delta_function = np.zeros(len(energy_values))
        dos_final = initial_delta_function  
        for i in range(0,len(energy_values)):
            initial_delta_function = np.zeros(len(energy_values))
            peak_val = dos_delta[i]
            if peak_val == 0.0:
                initial_delta_function = np.zeros(len(energy_values))
            else:
                A = peak_val*dE
                sigma = FWHH/(2.0*np.sqrt(2.0*np.log(2.0)))
                beta = 1.0/(sigma*np.sqrt(2*np.pi))
                alpha = 1.0/(2.0*sigma**2)
                for j in range(0,len(energy_values)):
                    initial_delta_function[j] = A*beta*np.exp(-alpha*(energy_values[j]-energy_values[i])**2)#*2.0 ##ADDED in 2. for NONCOLLINEAR RUN
            dos_final = dos_final + initial_delta_function
        
        #f = open("out.txt","w")
        f.write("\n"+'# Column '+str(l)+' of resolved DOSCAR'+"\n")
        for i in range(0,len(energy_values)):
            f.write(str(energy_values[i])+' '+str(dos_final[i])+"\n") #write data to output file in xmgrace format (-nxy)
        print("done with column", l)

    f.close()
    print("File written, process complete. Plot in xmgrace by typing 'xmgrace -nxy <filename>' in terminal")
            
            
    
    g.close()
    m.close()