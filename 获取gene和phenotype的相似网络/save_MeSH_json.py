import json
import openpyxl

wb = openpyxl.load_workbook('MeSH主题词.xlsx')
ws = wb['Sheet2']


mesh_list = []
for i in range(2,65034):
    cur_word_list = ws.cell(i,2).value.split('※')
    mesh_list += cur_word_list

    if i % 1000 == 0:
        print('当前处理完第{}行'.format(i))

mesh_list = list(set(mesh_list))

with open('mesh_word.json', 'w') as f:
    json.dump(mesh_list, f)
    print('数据写入成功！共{}条数据'.format(len(mesh_list)))


