import numpy as np

# 生成gene的相似网络
gene_sim_matrix = np.eye(10)
print(gene_sim_matrix.shape)
np.save('acute_geneSim.npy',gene_sim_matrix)

# # 生成phenotype的相似网络
# phenotype_sim_martix = np.eye(5846)
# print(phenotype_sim_martix.shape)
# np.save('test_phenoSim.npy', phenotype_sim_martix)