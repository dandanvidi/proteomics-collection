# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:36:25 2015

@author: dan
"""
import pandas as pd
import csv
import numpy as np

BW = pd.DataFrame.from_csv("ecoli_BW_Schmidt_et_al_2015_copies_cell.csv")
others = pd.DataFrame.from_csv("ecoli_others_Schmidt_et_al_2015_copies_cell.csv")
heinemann = pd.DataFrame.from_csv("ecoli_heinemann_unpublished_copies_cell.csv")
not_mapped = csv.writer(open('../supporting_data/unmapped_proteins.csv','w'))

uni_to_b = {row[48:54]:row[0:5].split(';')[0].strip()
            for row in open("../supporting_data/all_ecoli_genes.txt", 'r')}

manual_replacememnts = {
'D0EX67':'b1107',
'D4HZR9':'b2755',
'P00452-2':'b2234',
'P02919-2':'b0149',
'Q2A0K9':'b2011',
'Q5H772':'b1302',
'Q5H776':'b1298',
'Q5H777':'b1297',
'Q6E0U3':'b3183',
'C9M2Y6':'b2755'}

uni_to_b.update(manual_replacememnts)

id_mapper = pd.DataFrame.from_dict(uni_to_b.items()).set_index(0)
    
schmidt = BW.join(others, how='outer')
schmidt = schmidt.join(heinemann, how='outer')

for g in schmidt.index: 
    if g not in uni_to_b.iterkeys():
        not_mapped.writerow([g])
        print g
        schmidt.drop(g, inplace=True)
        
new_index = [uni_to_b[g] if g in uni_to_b.iterkeys() else g for g in schmidt.index]
schmidt.index = new_index

bnumber_duplicates = schmidt.index[np.where(schmidt.index.duplicated())[0]]
for i in bnumber_duplicates:
    
    tmp = schmidt.loc[bnumber_duplicates].sum()
    schmidt.drop(i,inplace=True)
    schmidt.loc[i] = tmp
    

gc = pd.DataFrame.from_csv('../growth_conditions.csv')
volume = gc['single cell volume [fL]'] # fL per cell
volume = volume.loc[schmidt.columns]

schmidt = schmidt.div(volume,axis=1)
schmidt.to_csv("../copies_fL/ecoli_Schmidt_et_al_2015+heinemann.csv")
