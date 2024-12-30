import scipy.sparse as sp
import pandas as pd
import networkx as nx

# 读取关系对
df = pd.read_table('new_network.txt', sep=' ', header=None, encoding='utf-16')
relation_df = pd.DataFrame(df, columns=[0,1])
print('取出交互关系。。。。')

# pandas转numpy
relation_list = []
for index, row in relation_df.iterrows():
    relation_list.append((row[0],row[1]))
print(len(relation_list))
print(relation_list)
print('转化numpy')

# 交互关系转化为图
g = nx.Graph(relation_list) # 交互关系转换为图
print('交互关系转化为图')
# 生成图的邻接矩阵的稀疏矩阵
s_A = nx.to_scipy_sparse_matrix(g, dtype=int, format='csr') # 生成图的邻接矩阵的稀疏矩阵
print('生成稀疏矩阵')
sp.save_npz('adj.npz', s_A)  # 保存稀疏矩阵
# csr_matrix_variable = sp.load_npz('adj.npz') # 读取稀疏矩阵
print('保存矩阵成功')
