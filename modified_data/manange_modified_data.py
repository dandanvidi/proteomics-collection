# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:36:25 2015

@author: dan
"""
import pandas as pd
import csv
import numpy as np

BW = pd.DataFrame.from_csv("ecoli_BW_Schmidt_et_al_2015.csv")
others = pd.DataFrame.from_csv("ecoli_others_Schmidt_et_al_2015.csv")
not_mapped = csv.writer(open('../supporting_information/unmapped_proteins.csv','w'))

uni_to_b = {row[48:54]:row[0:5].split(';')[0].strip()
            for row in open("../source_data/all_ecoli_genes.txt", 'r')}

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
    
schmidt = BW.join(others, how='outer')

for g in schmidt.index: 
    if g not in uni_to_b.iterkeys():
        not_mapped.writerow([g])
        print g
        schmidt.drop(g, inplace=True)
        
schmidt.index.name = 'Bnumber'
new_index = [uni_to_b[g] if g in uni_to_b.iterkeys() else g for g in schmidt.index]
schmidt_bnumbres = schmidt.copy()
schmidt_bnumbres.index = new_index

bnumber_duplicates = schmidt_bnumbres.index[np.where(schmidt_bnumbres.index.duplicated())[0]]
for i in bnumber_duplicates:
    
    tmp = schmidt_bnumbres.loc[bnumber_duplicates].sum()
    schmidt_bnumbres.drop(i,inplace=True)
    schmidt_bnumbres.loc[i] = tmp
    
schmidt_bnumbres.to_csv("../copies_fL/ecoli_Schmidt_et_al_2015.csv")
