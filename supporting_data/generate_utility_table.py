import pandas as pd

uni_to_b = {row[48:54]:row[0:5].split(';')[0].strip()
            for row in open("../supporting_data/all_ecoli_genes.txt", 'r')}
b_to_length = {row[0:5]:int(row[75:84]) for row in open("../supporting_data/all_ecoli_genes.txt", 'r')}

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
b_to_uni = {v:k for k,v in uni_to_b.iteritems()}
id_mapper = pd.DataFrame.from_dict(b_to_uni.items()).set_index(0)
id_mapper.index.name = 'Bnumber'
id_mapper.columns = ['UPID']
#id_mapper['gene length [aa]'] = [b_to_length[b] for b in id_mapper.index]


peebo = pd.DataFrame.from_csv('../supporting_data/peebo_info.tsv',sep='\t')

gene_info = id_mapper.join(peebo,how='outer')

schmidt = pd.DataFrame.from_csv('../supporting_data/schmidt_info.tsv',sep='\t')
new_index = [uni_to_b[g] if g in uni_to_b.iterkeys() else g for g in schmidt.index]
schmidt.index = new_index

out = gene_info.merge(schmidt,how='outer')


#id_mapper['MW [kDa]'] = [b_to_length[b] for b in id_mapper.index]