import json
import openpyxl


wb = openpyxl.load_workbook('gene1.xlsx')
ws = wb['Sheet1']
gene_map = {}
for i in range(16606):
    cur_geneId = ws.cell(i+1,1).value
    gene_map[str(cur_geneId)] = i+1


with open("geneId_number_map.json", "w") as f:
    json.dump(gene_map,f)
    print("载入文件完成!")
wb.save('gene1.xlsx')
wb.close()





