import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import math
import sympy
from sympy.abc import *
import openpyxl


def get_sim_score(matrix):
    sim_matrix = cosine_similarity(matrix)
    return sim_matrix


def get_idf_arr(df_arr):
    idf_arr = []
    for i in range(911):
        idf = math.log(5846 / (df_arr[i] + 0.01))
        idf_arr.append(idf)
    return idf_arr


def get_down_num(matrix, arr):
    down_num_arr = []
    for i in range(5846):
        cur = 0
        for j in range(911):
            cur += (matrix[i][j] * arr[j])**2
        if cur == 0:
            down_num_arr.append(1)
        else:
            down_num_arr.append(math.sqrt(cur))

    return down_num_arr

def get_weight_matrix(matrix, idf_arr, num_arr):
    for i in range(5846):
        for j in range(911):

            matrix[i][j] = (matrix[i][j] * idf_arr[j]) / num_arr[i]

    return matrix


# with open('occurred_mesh.json', 'r') as f:
#     mesh_arr = json.load(f)
# print(len(mesh_arr))
# weight_matrix = np.load('mesh_weight_matrix.npy')
#
# DF_arr = weight_matrix.sum(axis=0)
# idf_arr = get_idf_arr(DF_arr)
# # print(idf_arr[14],'aaa')
# num_arr = get_down_num(weight_matrix, idf_arr)
# print(num_arr)
# weight_matrix = get_weight_matrix(weight_matrix, idf_arr, num_arr)
# print(weight_matrix)
# print(weight_matrix.shape)
#
# np.save('mesh_weight_matrix111.npy', weight_matrix)
# print('mesh表型权重矩阵保存成功！')









matrix = np.load('mesh_weight_matrix111.npy')
matrix = get_sim_score(matrix)
# print(matrix)
# print(matrix.shape)

arr = []
arr_zero = []
for i in range(5846):
    for j in range(5846):
        if j == i:
            arr.append(matrix[i][j])
            if matrix[i][j] == 0:
                matrix[i][j] = 1
print(matrix)


# 以下是统计有mesh数目但权重矩阵全为零的index值
# wb = openpyxl.load_workbook('phenotype_information.xlsx')
# ws = wb['Sheet2']

# xlsx_zero = []
# for i in range(2, 284):
#     cur = ws.cell(i,3).value
#     xlsx_zero.append(cur)
#
# not_occur_index = []
# for i in range(len(arr_zero)):
#     if arr_zero[i] not in xlsx_zero:
#         not_occur_index.append(arr_zero[i])
# print(not_occur_index)
# print(len(not_occur_index))
# 以上是统计有mesh数目但权重矩阵全为零的index值


np.save('phenotypeSim.npy', matrix)
print('表型相似矩阵保存成功！')








