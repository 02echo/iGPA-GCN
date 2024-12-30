import numpy as np
import csv


# f = open('test_geneid.csv')
# # 数据两列（id1，id2），每一行表示这两个节点之间存在边
# data = [tuple(map(int, row)) for row in csv.reader(f)]  # 读取数据
#
# n = max(max(id1, id2) for id1, id2 in data)
# print(n)  # 最大节点数对应邻接矩阵的行列数
# matrix = np.zeros((n, n), dtype='float32')  # 生成n行n列的全0数组
# for id1, id2 in data:
#     matrix[id2 - 1][id1 - 1] = 1  # 遍历数据，将对应关系转化为1
#
# np.save('GP_adj.npy', matrix)

data = np.load('adjGP.npy')
print(data.shape)