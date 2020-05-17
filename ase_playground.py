# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:36:19 2020

@author: valde
"""
import msgnet
import os
from ase.db import connect
from ase import Atoms
from ase.calculators.emt import EMT
from ase.io import read
import csv
import time

os.chdir("C:/Users/valde/OneDrive - Danmarks Tekniske Universitet/GitHub/msgnet")

path = "./datasets/play2.xyz"


##########WE DONE DID IT BOIS###################


##########WE OPENED THE GODDAMN XYZ FILE YAAAAASSS##############


##############With Number of atoms as seperator#############
with open(path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='\t')
    output_mol = []  # the molecules in xyz
    output_number_of=[] # number of atoms in a molecule
    mol_index=[] # index, so you can split output_mol properly
    count = 0
    mol_count = 0   #number of molecules
    a=0
    for row in csv_reader:
        count+=1
        #print(row)
        if len(row)==0:
            continue
        if len(row[0])<3:
            mol_count+=1
            output_number_of.append(int(row[0]))
            mol_index.append(int(row[0])+a)
            a=mol_index[-1]
        else:
            spl=row[0].split()
            output_mol.append(spl) 
    print(mol_count)
    print(count)
    
mol_path="./datasets/play_moldata.csv"

with open(mol_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    h_l_g=[]  # the molecules in xyz
    count = 0
    next(csv_reader)
    for row in csv_reader:
        count+=1
        h_l_g.append(list(map(float,row[7:10]))) 
    print(count)

#homo:8, gap:8, lumo:10
#9,10,11
##############Example, make into loop#################

####################FOR REAL FOR REAL??######################

play_db=os.path.join(msgnet.defaults.datadir, "play2.db")# set db location
# "play.db%s" % @id=??
db=connect(play_db) #connect to database


molT=list(map(list,zip(*output_mol)))#map to vertical list, for easier float mapping...


A_names=molT[0] #set the atom names in seperate list for ez use

p1=list(map(float,molT[1]))#map first coordinate for all atoms
p2=list(map(float,molT[2]))#map second coordinate for all atoms
p3=list(map(float,molT[3]))#map third coordinate for all atoms

P=[p1,p2,p3] #combine them for mapping back

PT=list(map(list,zip(*P))) # map the bitch back

#for i in range(len(mol_index)-1):   <- real stuff

start=time.time()
m_ind=[0]+mol_index #add a zero to make index right

for i in range(len(h_l_g)):
    prop_dict={'homo': h_l_g[i+1][0], 'lumo': h_l_g[i+1][1] , 'gap': h_l_g[i+1][2]} 
    
    M=Atoms(A_names[mol_index[i]:mol_index[i+1]],PT[mol_index[i]:mol_index[i+1]]) #this is where the magic happens
    print(M)
    db.write(M,data=prop_dict)#writing to the database (appends)    
end_time=(time.time()-start)
print(end_time)


#row=db.get(id), extracts tow
#row.key    #use dir(row) to check attributes of the row. 
#row.toatoms() pretty usefull. 



#100 = 1.59 sec, 1000 = 15.9 sec
#gonna run for 1.3 hours with all 291732 molecules


##################RIGHT DIRECTORY###########################
os.chdir("C:/Users/valde/OneDrive - Danmarks Tekniske Universitet/GitHub/msgnet")

play_db=os.path.join(msgnet.defaults.datadir, "play.db")

db=connect(play_db)


h2 = Atoms('H2',[[0,0,0],[0,0,0.7]])
h2.calc=EMT()
h2.get_forces()

db.write(h2, relaxed=False)

read()

import pandas

df=pandas.read_csv("./datasets/play.xyz")


"""
with connect('mols.db') as db:
    for mol in molecules:
        db.write(mol, ...)
"""
"""
db = connect('database.db')
row = db.select(id=1)[0]
dir(row)


from ase.db import connect

db = connect('database.db')
for row in db.select():
    atoms = row.toatoms()
    print(atoms)
"""
"""
 from ase.io import read, write
 write('abc.xyz', read('abc.traj'))
"""
"""

def select_wfilter(con, filterobj):
    if filterobj is None:
        for row in con.select():
            yield row
    elif isinstance(filterobj, str):
        for row in con.select(filterobj):
            yield row
    else:
        for row in con.select():
            if filterobj(row):
                yield row
"""                
                
"""
def load_ase_data(
    db_path="oqmd_all_entries.db",
    dtype=float,
    cutoff_type="voronoi",
    cutoff_radius=2.0,
    filter_query=None,
    self_interaction=False,
    discard_unconnected=False,
):
    load_ase_data
    Load atom structure data from ASE database

    :param db_path: path of the database to load
    :param dtype: dtype of returned numpy arrays
    :param cutoff_type: voronoi, const or coval
    :param cutoff_radius: cutoff radius of the sphere around each atom
    :param filter_query: query string or function to select a subset of database
    :param self_interaction: whether an atom includes itself as a neighbor (not only its images)
    :param discard_unconnected: whether to discard samples that ends up with no edges in the graph
    :return: list of FeatureGraph objects
    
    con = ase.db.connect(db_path)
    sel = filter_query

    for i, row in enumerate(select_wfilter(con, sel)):
        if i % 100 == 0:
            print("%010d    " % i, sep="", end="\r")
        atoms = row.toatoms()
        if row.key_value_pairs:
            prop_dict = row.key_value_pairs
        else:
            prop_dict = row.data
        prop_dict["id"] = row.id
        try:
            graphobj = FeatureGraph(
                atoms,
                cutoff_type,
                cutoff_radius,
                lambda x: x,
                self_interaction=self_interaction,
                **prop_dict
            )
        except RuntimeError:
            logging.error("Error during data conversion of row id %d", row.id)
            continue
        if discard_unconnected and (graphobj.conns.shape[0] == 0):
            logging.error("Discarding %i because no connections made %s", i, atoms)
        else:
            yield graphobj
    print("")
"""