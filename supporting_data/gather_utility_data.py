import pandas as pd
import numpy as np
from Bio.SeqUtils import molecular_weight
from Bio import SeqIO
from collections import Counter
    
    
AA_LETTERS = sorted("ACEDGFIHKMLNQPSRTWVY")
out = pd.DataFrame(columns=[aa for aa in AA_LETTERS])
#

record = SeqIO.read('../supporting_data/U00096.gb', "gb")
## count amino acids per ORF and write to csv file    

i = 0
out = {}
for r in record.features:
    if r.type == 'CDS':
        data = r.qualifiers
        i += 1        
        try:
            data['molecular_weight[Da]'] = molecular_weight(data['translation'][0], seq_type='protein')
        except KeyError:
            continue
        out[i] = data

out = pd.DataFrame.from_dict(out).T
out.to_csv('ecoli_genome_info.tsv', sep='\t')

    #schmidtMW = schmidt['MW [kDa]']
#peeboMW = peebo['MW [kDa]']