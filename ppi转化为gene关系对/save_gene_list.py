import pandas as pd
import json

df = pd.read_excel('Uniquegene.xlsx')
gene_list = df['gene_symbol'].values.tolist()

# print(json_string)

with open("my_unique_gene_list.json", "w") as f:
    json.dump(gene_list,f)
    print("载入文件完成。")