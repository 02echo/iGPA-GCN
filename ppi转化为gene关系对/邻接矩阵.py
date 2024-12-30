#导入模块
import csv
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from scipy import sparse
import scipy.sparse as sp

from scipy.sparse import *
import torch
import torch.nn as nn
import torch.nn.functional as F


def get_adjmatrix():
    f = open('test_small_dataset.csv')
    # 数据两列（id1，id2），每一行表示这两个节点之间存在边
    data = [tuple(map(int, row)) for row in csv.reader(f)]  # 读取数据
    m=0
    n=0
    for id1,id2 in data:
        m = max(id1,m)
        n = max(id2,n)

    print(m,n)  # 最大节点数对应邻接矩阵的行列数
    matrix = np.zeros((m+1, n+1), dtype='float32')  # 生成m行n列的全0数组
    for id1, id2 in data:
        matrix[id1][id2] = 1  # 遍历数据，将对应关系转化为1
    return matrix

matrix = get_adjmatrix()
print(matrix.shape)
np.save('../处理数据集gene-phenotype/small_adjGP.npy', matrix)
print('保存邻接矩阵成功！')
# xlsx和csv无法保存很大的矩阵
# np.savetxt('gene_adj.txt', matrix, fmt="%d", delimiter=",")
# df = pd.DataFrame(matrix)
# df.to_excel("Adjacency Matrix.xlsx",sheet_name="Sheet1")
#生成邻接矩阵并存储

# 保存为稀疏矩阵的格式
# s_matrix = sparse.csr_matrix(matrix)
# sp.save_npz('adj.npz', s_matrix)
# print('保存稀疏矩阵成功！')


# 生成度矩阵
def get_degree_matrix():
    degree_matrix = np.diag(np.sum(matrix, axis=1))
    print("度矩阵：")
    print(degree_matrix)
    return degree_matrix


# 对邻接矩阵归一化
def preprocess_adj(adj):
    adj_normalized = normalize_adj(adj + sp.eye(adj.shape[0])) # 给A加上一个单位矩阵
    return sparse_to_tuple(adj_normalized)

# 图网络模型搭建
def preprocess_adj(self, normalization, adj, cuda):
    adj_normalizer = fetch_normalization(normalization)
    r_adj = adj_normalization(adj)
    r_adj = sparse_mx_to_torch_sparse_tensor(r_adj).float()
    if cuda:
        r_adj = r_adj.cuda()
    return r_adj



