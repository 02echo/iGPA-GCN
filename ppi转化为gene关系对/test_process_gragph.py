import networkx as nx
import numpy as np
import matplotlib.pylab as plt
from scipy.linalg import fractional_matrix_power

import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# 初始化图
G = nx.Graph(name="G")

# 创建节点
for i in range(6):
    G.add_node(i, name=i)

# 创建边并添加到图里
edges = [(0,1),(0,2),(0,3),(1,2),(3,4),(3,5),(4,5)]
G.add_edges_from(edges)

print("Graph Info:\n",nx.info(G))

print("\nGraph Nodes:",G.nodes.data())

nx.draw(G, with_labels=True, font_weight='bold')
plt.show()

# 从图G获得邻接矩阵A和节点特征矩阵X
A = np.array(nx.attr_matrix(G, node_attr='name')[0])
X = np.array(nx.attr_matrix(G, node_attr='name')[1])
# 增加维度
X = np.expand_dims(X, axis=1)

print('shape of A:',A.shape)
print('\nshape of X:\n',X.shape)
print('\nAdjacency Matrix(A):\n',A)
print('\nNode Features Matrix(X):\n',X)