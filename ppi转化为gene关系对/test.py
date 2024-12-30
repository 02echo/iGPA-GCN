import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 定义一个简单的图,并可视化
# G = nx.Graph()
# G.add_edge(1,2,weight=1)
# G.add_edge(1,3,weight=1)
# for ii, jj, kk in G.edges(data="weight", default=1):
#     print(ii,jj,kk)
# nx.adjacency_matrix(G)
# nx.draw(G, with_labels=True)
# plt.show()

df = pd.read_excel('test_geneidnetwork.xlsx')
numpy_array = df.values



