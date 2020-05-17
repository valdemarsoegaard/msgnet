# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 11:53:09 2020

@author: valde
"""
#importing dependencies

import os
import ase
import ase.data
from ase.db import connect
from ase import Atoms
from ase.calculators.emt import EMT
from ase.io import read
import csv
import time

start_time=time.time()
os.chdir("C:/Users/valde/OneDrive - Danmarks Tekniske Universitet/GitHub/msgnet") #set the directory


#####
# change all places where it says "set" in commment to appropriate places
####

print("Begin loading XYZ file...")
###########LOAD THE XYZ FILE##################
start_xyz=time.time()
path = "./datasets/play2.xyz"  #set the right path 
with open(path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    output_mol = []  # the molecules in xyz
    output_number_of=[] # number of atoms in a molecule
    mol_index=[0] # index, so you can split output_mol properly
    count = 0
    mol_count = 0   #number of molecules
    a=0
    for row in csv_reader:
        count+=1
        if len(row)==0: #skip blank lines
            continue
        if len(row[0])<3: #make sure the row containing the number of atoms does not get loaded
            mol_count+=1  #when a number of atoms is spotted, count 1 molecule
            output_number_of.append(int(row[0]))# number of atoms in a molecule
            mol_index.append(int(row[0])+a)# the index of the molecules
            a=mol_index[-1] #add the index of the previous, to get right index
            if mol_count%10000==0:
                time_xyz=(time.time()-start_xyz)
                print("loaded {0} Molecules in {1} seconds" .format(mol_count,time_xyz))
        else:
            spl=row[0].split()# split the string
            output_mol.append(spl) #append the string
    if mol_count+1 == len(mol_index):
        time_xyz=(time.time()-start_xyz)
        print("Molecules and index matches...")
        print("{0} Molecules loaded from xyz file in {1} seconds or {2} hours" .format(mol_count,time_xyz,(time_xyz/3600)))
        print("\n{} lines loaded in total" .format(count))
    else:
        print("Molecules and index does not match...")
        
#mapping
print("\nBegin mapping")
start_map=time.time()
molT=list(map(list,zip(*output_mol)))#map to vertical list, for easier float mapping...
end_map=time.time()
print("The list have been transposed vertically, in {0} seconds" .format(end_map-start_map))


A_names=molT[0] #put the atom names in seperate list for ez use

print(set(A_names))
print(len(set(A_names)))
print("Atom names have been extracted to seperate list...")
p1=list(map(float,molT[1]))#map first coordinate for all atoms
p2=list(map(float,molT[2]))#map second coordinate for all atoms
p3=list(map(float,molT[3]))#map third coordinate for all atoms
print("The coordinates have been converted to floats")
P=[p1,p2,p3] #combine them for mapping back

PT=list(map(list,zip(*P))) # map the bitch back
print("The coordinates have been transposed back to horizontal list, now as floats.")
end_map=time.time()
print("Mapping done in {} seconds" .format(end_map-start_map))

##########XYZ HANDLING DONE#########
"""
print("\nBegin Loading HOMO  LUMO GAP from csv file...")
#########LOAD THE homo_lumo_gap TO A LIST#############
mol_path="./datasets/moldata.csv"   #set right datapath
start_h_l_g=time.time()
with open(mol_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    h_l_g=[]  # the molecules in xyz
    count = 0
    next(csv_reader)
    for row in csv_reader:
        count+=1
        h_l_g.append(list(map(float,row[7:10])))
    if mol_count == count:
        end_h_l_g=time.time()
        print("Number of HOMO_LUMO_GAP loaded matches molecules loaded from XYZ file")
        print("loaded {0} lines in {1} seconds" .format(count,(end_h_l_g-start_h_l_g)))
    else:
        end_h_l_g=time.time()
        print("Loaded HOMO_LUMO_GAP does NOT MATCH molecules loaded from XYZ file")
        print("loaded {0} lines in {1} seconds" .format(count,(end_h_l_g-start_h_l_g)))
       
#####WRITE TO desired DB########     
print("\nBegin saving information to ase.db...")        

output_db="./datasets/play3.db"
start_ase=time.time()
ase_count=0
with ase.db.connect(output_db, append=False) as asedb:
    for i in range(10000): #set proper range when converting all -> len(h_l_g) 
        ase_count+=1
        prop_dict={'homo': h_l_g[i][0], 'lumo': h_l_g[i][1] , 'gap': h_l_g[i][2]}  
        atoms = Atoms(A_names[mol_index[i]:mol_index[i+1]],PT[mol_index[i]:mol_index[i+1]])
        asedb.write(atoms, data=prop_dict)
        if ase_count%1000==0:
            time_spent=(time.time()-start_ase)
            print("took {0} seconds to save {1} molecules" .format(time_spent,ase_count))
        
end_time=(time.time()-start_ase)
print("Took {0} seconds to save all {1} molecules" .format(end_time,ase_count))
total_time=time.time()-start_time
print("Script ran for {0} seconds or {1}" .format(total_time,total_time/3600))
"""