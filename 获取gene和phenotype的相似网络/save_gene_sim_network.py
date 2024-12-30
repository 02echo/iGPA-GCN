import pandas as pd
import networkx as nx
import numpy as np

df = pd.read_excel('new_network.xlsx')

G = nx.Graph()

for index, row in df.iterrows():
    G.add_edge(row['node1'],row['node2'],weight=row['weight'])


nodes = list(G.nodes())
similarity_matrix = np.zeros((len(nodes),len(nodes)))


for i, node1 in enumerate(nodes):
    for j, node2 in enumerate(nodes):
        if i != j:
            if G.has_edge(node1, node2):
                similarity_matrix[i,j] = G[node1][node2]['weight']
            else:
                similarity_matrix[i,j] = 0

# 打印相似网络矩阵
print("Similarity matrix:")
print(similarity_matrix)
print(similarity_matrix.shape)