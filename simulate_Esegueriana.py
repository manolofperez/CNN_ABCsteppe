#!/usr/bin/python

## in order to use this code you have to have ms installed on your computer
## ms can be freely downloaded from:
## http://home.uchicago.edu/rhudson1/source/mksamples.html

## import all required modules.
import random
import os
import math
import shlex, subprocess
import numpy as np

##define a function to read ms' simulations and transform then into a NumPy array.    
def ms2nparray(xfile):
	g = list(xfile)
	k = [idx for idx,i in enumerate(g) if len(i) > 0 and i.startswith(b'//')]
	f = []
	for i in k:
		L = g[i+4:i+nDNANsam+4]
		q = []
		for i in L:
			i = [int(j) for j in list(i)]
			i = np.array(i, dtype=np.int8)
			q.append(i)
		q = np.array(q)
		q = q.astype("int8")
		f.append(np.array(q))
	return f

### variable declarations.

#define the number of simulations.
Priorsize = 10000

## sample size for Extrazonal.
nExZ = 160
## sample size for Zonal.
nZ = 110
## Combines sample size.
nDNANsam = nExZ + nZ

##mutation rate.
mutrate = 7.0E-9

simModel1 = []
simModel2 = []
simModel3 = []


## create a file to store parameters and one to store the models.
parameters1 = open("parameters1.txt","w")
parameters2 = open("parameters2.txt","w")
parameters3 = open("parameters3.txt","w")

### Stable pop sizes model, with migration until LGM.
for i in range(Priorsize):

	### Define parameters.
	## number of years per generation.
	genlen = random.uniform(8,10)
	##Ne from 40k to 200k.
	Ne = random.uniform(40000,200000)
	##Ne proportion for the Zonal lineage.
	NeZ=random.uniform(0.2,5)
	## Calculate theta values.
	Theta = 4*Ne*mutrate*85
	#relative values of Ne fro each period.
	NeExZLGM=1
	NeZLGM=1
	NeExZPl=1
	NeZPl=1
	
	## divergence time prior in years, following uniform distributions.
	T3=random.uniform(0,12000)
	T2=random.uniform(12000,110000)
	T1=random.uniform(110000,2400000)

	## Transform to coalescent units.
	coalT3=T3/(genlen*4.0*Ne)
	coalT2=T2/(genlen*4.0*Ne)
	coalT1=T1/(genlen*4.0*Ne)

	## migration prior set to 0 in this model.
	m12_Pres=0
	m21_Pres=0
	m12_LGM=random.uniform(0,5)
	m21_LGM=random.uniform(0,5)
	m12_Pl=random.uniform(0,5)
	m21_Pl=random.uniform(0,5)
	
	## simulate SNPs.
	com=subprocess.Popen("./ms %d 1000 -s 1 -t %f -I 2 %d %d -n 2 %f -em %f 1 2 %f -em %f 2 1 %f -em %f 1 2 %f -em %f 2 1 %f -ej %f 1 2" % (nDNANsam, Theta, nExZ, nZ, NeZ, coalT3, m12_LGM, coalT3, m21_LGM, coalT2, m12_Pl, coalT2, m21_Pl, coalT1), shell=True, stdout=subprocess.PIPE).stdout
	output = com.read().splitlines()
	simModel1.append(np.array(ms2nparray(output)).swapaxes(0,1).reshape(nDNANsam,-1).T)
	
	## save parameter values.
	parameters1.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (Theta, T1, T2, T3, Ne, NeZ, NeExZLGM, NeZLGM, NeExZPl, NeZPl, m12_Pres, m21_Pres, m12_LGM, m21_LGM, m12_Pl, m21_Pl))

#save NumPy arrays.
simModel1=np.array(simModel1)
np.save('simModel1.npy', simModel1)
del(simModel1)

### Cold stage expansion, with migration until LGM.
for i in range(Priorsize):

	### Define parameters.
	## number of years per generation.
	genlen = random.uniform(8,10)
	##Ne from 40k to 200k.
	Ne = random.uniform(40000,200000)
	##Ne proportion for the Zonal lineage.
	NeZ=random.uniform(0.2,5)
	## Calculate theta values.
	Theta = 4*Ne*mutrate*85
	#relative values of Ne fro each period.
	NeExZLGM=random.uniform(5,100)
	NeZLGM=random.uniform(5,100)
	NeExZPl=random.uniform(0.5,1)
	NeZPl=random.uniform(0.5,1)
	
	## divergence time prior in years, following uniform distributions.
	T3=random.uniform(0,12000)
	T2=random.uniform(12000,110000)
	T1Growth=random.uniform(110000,500000)
	T1=random.uniform(T1Growth,2400000)

	## Transform to coalescent units.
	coalT3=T3/(genlen*4.0*Ne)
	coalT2=T2/(genlen*4.0*Ne)
	coalT1Growth=T1Growth/(genlen*4.0*Ne)
	coalT1=T1/(genlen*4.0*Ne)

	# calculate growth rates from time and magnitude of the expansion.
	GrowthExZ = -(1/(coalT1Growth-coalT2))*math.log(NeExZPl/NeExZLGM)
	GrowthZ = -(1/(coalT1Growth-coalT2))*math.log(NeZPl/NeZLGM)

	## migration prior set to 0 in this model.
	m12_Pres=0
	m21_Pres=0
	m12_LGM=random.uniform(0,5)
	m21_LGM=random.uniform(0,5)
	m12_Pl=random.uniform(0,5)
	m21_Pl=random.uniform(0,5)
	
	## simulate SNPs.
	com=subprocess.Popen("./ms %d 1000 -s 1 -t %f -I 2 %d %d -n 2 %f -en %f 1 %f -en %f 2 %f -em %f 1 2 %f -em %f 2 1 %f -eg %f 1 %f -eg %f 2 %f -em %f 1 2 %f -em %f 2 1 %f -eg %f 1 0 -eg %f 2 0 -ej %f 1 2" % (nDNANsam, Theta, nExZ, nZ, NeZ, coalT3, NeExZLGM, coalT3, NeZLGM, coalT3, m12_LGM, coalT3, m21_LGM, coalT2, GrowthExZ, coalT2, GrowthZ, coalT2, m12_Pl, coalT2, m21_Pl, coalT1Growth, coalT1Growth, coalT1), shell=True, stdout=subprocess.PIPE).stdout
	output = com.read().splitlines()
	simModel2.append(np.array(ms2nparray(output)).swapaxes(0,1).reshape(nDNANsam,-1).T)
	
	## save parameter values.
	parameters2.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (Theta, T1, T2, T3, Ne, NeZ, NeExZLGM, NeZLGM, NeExZPl, NeZPl, m12_Pres, m21_Pres, m12_LGM, m21_LGM, m12_Pl, m21_Pl))

#save NumPy arrays.
simModel2=np.array(simModel2)
np.save('simModel2.npy', simModel2)
del(simModel2)

## Cold stage expansion only in Z, with migration until LGM.
for i in range(Priorsize):

	### Define parameters.
	## number of years per generation.
	genlen = random.uniform(8,10)
	##Ne from 40k to 200k.
	Ne = random.uniform(40000,200000)
	##Ne proportion for the Zonal lineage.
	NeZ=random.uniform(0.2,5)
	## Calculate theta values.
	Theta = 4*Ne*mutrate*85
	#relative values of Ne for each period.
	NeExZLGM=1
	NeZLGM=random.uniform(5,100)
	NeExZPl=1
	NeZPl=random.uniform(0.5,1)
	
	## divergence time prior in years, following uniform distributions.
	T3=random.uniform(0,12000)
	T2=random.uniform(12000,110000)
	T1Growth=random.uniform(110000,500000)
	T1=random.uniform(T1Growth,2400000)

	## Transform to coalescent units.
	coalT3=T3/(genlen*4.0*Ne)
	coalT2=T2/(genlen*4.0*Ne)
	coalT1Growth=T1Growth/(genlen*4.0*Ne)
	coalT1=T1/(genlen*4.0*Ne)
	
	# calculate growth rates from time and magnitude of the expansion.
	GrowthZ = -(1/(coalT1Growth-coalT2))*math.log(NeZPl/NeZLGM)

	## migration prior set to 0 in this model.
	m12_Pres=0
	m21_Pres=0
	m12_LGM=random.uniform(0,5)
	m21_LGM=random.uniform(0,5)
	m12_Pl=random.uniform(0,5)
	m21_Pl=random.uniform(0,5)
	
	## simulate SNPs.
	com=subprocess.Popen("./ms %d 1000 -s 1 -t %f -I 2 %d %d -n 2 %f -en %f 2 %f -em %f 1 2 %f -em %f 2 1 %f -eg %f 2 %f -em %f 1 2 %f -em %f 2 1 %f -eg %f 2 0 -ej %f 1 2" % (nDNANsam, Theta, nExZ, nZ, NeZ, coalT3, NeZLGM, coalT3, m12_LGM, coalT3, m21_LGM, coalT2, GrowthZ, coalT2, m12_Pl, coalT2, m21_Pl, coalT1Growth, coalT1), shell=True, stdout=subprocess.PIPE).stdout
	output = com.read().splitlines()
	simModel3.append(np.array(ms2nparray(output)).swapaxes(0,1).reshape(nDNANsam,-1).T)
	
	## save parameter values.
	parameters3.write("%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (Theta, T1, T2, T3, Ne, NeZ, NeExZLGM, NeZLGM, NeExZPl, NeZPl, m12_Pres, m21_Pres, m12_LGM, m21_LGM, m12_Pl, m21_Pl))

#save NumPy arrays.
simModel3=np.array(simModel3)
np.save('simModel3.npy', simModel3)
del(simModel3)