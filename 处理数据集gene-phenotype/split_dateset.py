from sklearn.model_selection import train_test_split
import numpy as np

sparse_matrix = np.load('GP_adj.npy')

# 划分数据集
num_rows = sparse_matrix.shape[0]
train_size = int(num_rows * 0.8)  # 训练集占80%
test_size = num_rows - train_size  # 测试集占20%

# 随机打乱数据
np.random.shuffle(sparse_matrix)

# 划分训练集和测试集
train_set = sparse_matrix[:train_size]
test_set = sparse_matrix[train_size:]

print("训练集：\n", train_set)
print("测试集：\n", test_set)





