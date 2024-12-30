import pandas as pd
import xlrd
import numpy as np

df = pd.read_excel('my_protein.xlsx')
protein1_list = df['protein1'].values.tolist()
protein2_list = df['protein2'].values.tolist()
my_protein_list = df['Cross'].values.tolist()
protein1_list = list(set(protein1_list))
protein2_list = list(set(protein2_list))

protein_list = []
for cur in my_protein_list:
    if cur in protein1_list:
        protein_list.append(cur)

protein_list = list(set(protein_list))
print(protein_list)