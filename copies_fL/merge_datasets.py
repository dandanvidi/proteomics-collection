import os
import pandas as pd

dirlist = sorted(os.listdir('../copies_fL'))
# if some files are open, ignore them
dirlist = ['../copies_fL/'+x for x in dirlist if not x.startswith('.')]
dirlist = [x for x in dirlist if x.endswith('.csv')]
gc = pd.DataFrame.from_csv('../growth_conditions.csv')

merged = pd.DataFrame()

for f in dirlist:
    try:
        f_data = pd.DataFrame.from_csv(f)
        f_data.dropna(how='all', inplace=True)
        merged = f_data.join(merged, how='outer')
    except:
        print "the following file was ignored: "+f
merged.dropna(how='all', inplace=True)
gr = gc['growth rate [h-1]']
gr.sort
merged = merged[gr.index]
merged.to_csv('../meta_abundance[copies_fL].csv')