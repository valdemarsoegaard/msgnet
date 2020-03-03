# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 10:04:56 2020

@author: valde
"""

import os
import csv
import pandas
from openbabel import pybel

#os.getcwd()
os.chdir("C:/Users/valde/OneDrive/Dokumenter/GitHub/msgnet")


df=pandas.read_csv('moldata.csv',header=0)
df.columns.values


df.SMILES_str


input_path = "./datasets/training_data_cleaned.csv"
with open(input_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for row in csv_reader:
            data.append(row)




#%%
ind=[]

for i in range(9):
    
    mymol=pybel.readstring("smi",df.SMILES_str[i])
    print(mymol)
    ind.append(mymol)
    
    
