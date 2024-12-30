import os
import numpy as np
import torch

# print("Default Device : {}".format(torch.Tensor([4, 5, 6]).device))
#
# # cpu设备
# device = torch.Tensor([1, 2, 3], device="cpu:0").device
# print("Device Type: {}".format(device))
#

# # gpu设备
# gpu = torch.device("cuda:0")
# print("GPU Device:【{}：{}】".format(gpu.type, gpu.index))
#
#
# # 查询cpu和gpu设备数量
# print("Total GPU Count :{}".format(torch.cuda.device_count()))
# print("Total CPU Count :{}".format(torch.cuda.os.cpu_count()))
# #
# # 使用to方法将cpu的Tensor转换到GPU设备上
# data = torch.Tensor([[1, 4, 7], [3, 6, 9], [2, 5, 8]])
# print(data.shape)
# data_gpu = data.to(torch.device("cuda:0"))
# print(data_gpu.device)
# data = np.array([[2.3265e+08,1],[2,3]])
#
# print(data.shape)# res = np.isinf(data).all().all()
# print(res)

# import torch
# print(torch.__version__)  #注意是双下划线

# import pandas as pd
#
# # 读取两个Excel文件的第一列
# file1 = '../ppi转化为gene关系对/Uniquegene.xlsx'  # 替换为你的第一个文件路径
# file2 = '../分析/acute-pan.csv'  # 替换为你的第二个文件路径
#
# # 读取Excel文件的第一列（假设数据在第一列）
# df1 = pd.read_excel(file1, usecols=[0])  # 只读取第一列
# df2 = pd.read_csv(file2, usecols=[0])  # 只读取第一列
#
# # 提取第一列的数据并转换为集合（set）以便比较
# set1 = set(df1.iloc[:, 0])  # 将第一列数据转换为集合
# set2 = set(df2.iloc[:, 0])  # 将第二列数据转换为集合
#
# # 找出相同的数据
# common_data = set1.intersection(set2)
#
# # 输出相同的数据
# print("相同的数据有：")
# print(common_data)


# import numpy as np
# import pandas as pd
#
# # 读取CSV文件
# csv_file = 'GP_ben_acute.csv'  # 替换为你的CSV文件路径
# data = pd.read_csv(csv_file)
#
# # 将数据转换为numpy数组
# np_data = data.to_numpy()  # 或者使用 data.values
#
# # 保存为npy文件
# npy_file = 'GP_ben_acute.npy'  # 替换为你想保存的文件名
# np.save(npy_file, np_data)
#
# print(f"数据已保存为 {npy_file}")

# import pandas as pd
# import numpy as np
#
# # 读取CSV文件
# file_path = 'GP_acute.csv'  # 替换为你的文件路径
# data = pd.read_csv(file_path)
#
# # 确定总元素数量
# num_elements = data.size
#
# # 计算需要改写为 -1 的元素数量
# num_to_replace = int(0.2 * num_elements)
#
# # 随机选择需要修改的元素位置
# np.random.seed(42)  # 设置随机种子，保证结果可复现
# rows = np.random.randint(0, data.shape[0], num_to_replace)
# cols = np.random.randint(0, data.shape[1], num_to_replace)
#
# # 将选定位置的元素改为 -1
# for r, c in zip(rows, cols):
#     data.iloc[r, c] = -1
#
# # 保存修改后的文件
# output_path = 'GP_ben_acute.csv'  # 替换为保存路径
# data.to_csv(output_path, index=False)
#
# print(f"已将 {num_to_replace} 个元素改写为 -1，并保存为 {output_path}")


import math

# 定义5个数
numbers = [20.96, 22.74, 22.37, 22.48, 17.28]

# 计算平均值
mean = sum(numbers) / len(numbers)

# 计算标准差
variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
std_deviation = math.sqrt(variance)
print("标准差:", std_deviation)





