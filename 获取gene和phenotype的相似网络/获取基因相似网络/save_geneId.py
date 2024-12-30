import openpyxl
import json

# 保存gene——id信息
wb = openpyxl.load_workbook('gene_information.xlsx')
ws = wb['Sheet1']
gene_map = dict()

for i in range(2,1256):
    cur_gene = ws.cell(i,1).value
    gene_map[cur_gene] = i-2

print(len(gene_map))
with open('gene_id.json', 'w') as f:
    json.dump(gene_map, f)
    print('基因数据保存成功')