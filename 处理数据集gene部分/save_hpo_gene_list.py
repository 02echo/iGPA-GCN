
import pandas as pd
import xlrd
import numpy as np

df = pd.read_excel('Uniquegene.xlsx')
gene_list = df['gene_symbol'].values.tolist()
# print(gene_list)
# cur = df.iloc[0].values.tolist()  #第一行数据


# 创建存放gene-phenotype关联的数组
pairs_list = []

workbook = xlrd.open_workbook('gene_to_phenotype.xlsx')
sheet = workbook.sheets()[0]
df1 = pd.read_excel('gene_to_phenotype.xlsx')

for i in range(1,298056):
    cur_gene = sheet.cell_value(i,1)
    if cur_gene in gene_list:
        cur_pair = df1.iloc[i-1].values.tolist()
        # print(cur_pair)
        pairs_list.append(cur_pair)
    if i%1000 == 0:
        print("当前第{}行".format(i))

A = np.array(pairs_list)
data = pd.DataFrame(A)

writer = pd.ExcelWriter('my_gene_to_phenotype.xlsx')
data.to_excel(writer, 'sheet_1', float_format='%.5f')
writer.save()

writer.close()