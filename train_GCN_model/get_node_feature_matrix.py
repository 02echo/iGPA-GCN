import numpy as np

# 定义邻接矩阵
adjacency_matrix = np.array([[0, 1, 0, 1],
                             [1, 0, 1, 0],
                             [0, 1, 0, 1],
                             [1, 0, 1, 0]])

# 定义节点特征矩阵
feature_matrix = np.array([[1, 2, 3],
                           [4, 5, 6],
                           [7, 8, 9],
                           [10, 11, 12]])

# 计算节点特征向量矩阵
def compute_node_feature_matrix(adjacency_matrix, feature_matrix):
    num_nodes = adjacency_matrix.shape[0]
    node_feature_matrix = np.zeros_like(feature_matrix)

    for i in range(num_nodes):
        neighbors = np.where(adjacency_matrix[i] == 1)[0]
        num_neighbors = len(neighbors)
        if num_neighbors > 0:
            node_feature_matrix[i] = np.mean(feature_matrix[neighbors], axis=0)
        else:
            node_feature_matrix[i] = feature_matrix[i]

    return node_feature_matrix

node_feature_matrix = compute_node_feature_matrix(adjacency_matrix, feature_matrix)
print(node_feature_matrix)
