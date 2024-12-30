import numpy as np

def modify_matrix(matrix, a, b):
    # 获取所有值为0的元素的坐标
    zero_indices = np.argwhere(matrix == 0)

    # 获取所有值为1的元素的坐标
    one_indices = np.argwhere(matrix == 1)

    # 在所有值为0的元素里随机挑选a个元素改为-20
    zero_to_minus20 = zero_indices[np.random.choice(len(zero_indices), a, replace=False)]
    matrix[zero_to_minus20[:, 0], zero_to_minus20[:, 1]] = -20

    # 在a个值为1的元素里随机挑选b个元素改为-1
    one_to_minus1 = one_indices[np.random.choice(len(one_indices), b, replace=False)]
    matrix[one_to_minus1[:, 0], one_to_minus1[:, 1]] = -1

    # 在a个值为0的元素里随机挑选b个元素改为-10
    zero_to_minus10 = zero_indices[np.random.choice(len(zero_indices), b, replace=False)]
    matrix[zero_to_minus10[:, 0], zero_to_minus10[:, 1]] = -10

    return matrix


# original_matrix = np.load('adjGP.npy')
original_matrix = np.load('small_adjGP.npy')


print("原始矩阵:")
print(original_matrix.shape)

# 修改矩阵
# a, b = 69050, 13810
a,b = 61, 12
modified_matrix = modify_matrix(original_matrix.copy(), a, b)

print("\n修改后的矩阵:")
print(modified_matrix)

np.save('test_GP_ben_ind_label.npy', modified_matrix)
print('保存矩阵成功！')
