import networkx as nx
import numpy as np
import pandas as pd
from scipy.sparse import *
import torch
import torch.nn as nn
import torch.nn.functional as F

# 加载邻接矩阵
# adj_np = np.loadtxt('gene_adj.txt', dtype=int, delimiter=",")
# adj_matrix = pd.DataFrame(adj_np)
# adj_matrix = pd.read_csv('Adjacency Matrix.csv')
matrix_data = np.load('adj.npz')
adj_matrix = csr_matrix((matrix_data.data, matrix_data.indices, matrix_data.indptr), shape=[16606, 16606]).toarray()


# 将邻接矩阵转换为networkx图对象
graph = nx.from_numpy_matrix(adj_matrix)

# 获取图的特征矩阵
feature_matrix = np.eye(graph.number_of_nodes())

# 转换特征矩阵为pytorch tensor
feature_matrix = torch.FloatTensor(feature_matrix)

# 定义图卷积层
class GraphConvolutionLayer(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(GraphConvolutionLayer, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, adjacency, features):
        aggregate = torch.matmul(adjacency, features) #聚合邻居特征
        output = self.linear(aggregate)
        return output

# 创建图卷积网络模型
class GraphConvolutionalNetwork(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(GraphConvolutionalNetwork, self).__init__()
        self.conv1 = GraphConvolutionLayer(input_dim,hidden_dim)
        self.conv2 = GraphConvolutionLayer(hidden_dim,output_dim)

    def forward(self, adjacency, features):
        h1 = F.relu(self.conv1(adjacency, features))
        h2 = self.conv2(adjacency, h1)
        return h2

# 实例化图卷积网络模型
input_dim = feature_matrix.shape[1]
hidden_dim = 64 #隐藏层维度
output_dim = 32 #输出特征维度
gcn_model = GraphConvolutionalNetwork(input_dim,hidden_dim,output_dim)

# 运行模型并获取特征矩阵
graph_adjacency = nx.to_numpy_array(graph)
graph_adjacency = torch.FloatTensor(graph_adjacency)
output_features = gcn_model(graph_adjacency, feature_matrix)

# 输出特征矩阵的形状
print("Output feature matrix shape:", output_features.shape)
