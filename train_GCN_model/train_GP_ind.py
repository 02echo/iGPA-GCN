import numpy as np
import os

import torch
import torch as t
import sklearn
from sklearn.metrics import roc_auc_score, average_precision_score

from model import GCMC
from torch import nn, optim
from sklearn.preprocessing import PolynomialFeatures
from sklearn import ensemble
from evaluation import evaluation_fun
from utils import rwr
import argparse
import pandas as pd
import model_HPOFiller, model_HPODNets, model_iPiDA_GCN


# set random generator seed to allow reproducibility
t.manual_seed(66)
np.random.seed(66)

# assign cuda device ID
device = "cuda:0"
device = t.device('cuda')


def import_data(piRSim, DisSim,adjGP, GP_ben_ind_label):
    GS_seq = np.load(piRSim)
    PS_doid = np.load(DisSim)
    adjGP = np.load(adjGP)
    GP_ben_ind_label = np.load(GP_ben_ind_label)

    return GS_seq, PS_doid, adjGP, GP_ben_ind_label


def test_metric(label, input, idx):
    """
   Monitor the performance on test data set.
   :param label: ground-truth completed piRNA-disease label matrix
   :param input: predicted score predicted piRNA-disease score matrix
   :param idx: test samples index
   :return: AUC and AUPR on test set
   """
    score = input.detach().cpu().numpy()[idx]
    return roc_auc_score(label, score), average_precision_score(label, score)

def fit(model, train_data, optimizer, Epoch):
    """
        Predicted gene-phenotype association matrix.
        :param model: instance of model
        :param train_data: assembled training data
        :param optimizer: instance of optimizer
        :return: predicted gene-phenotype association score matrix
        """
    # turn to training mode
    model.train()
    # use MSE as the loss function
    criterion = nn.MSELoss(reduction='sum')
    scheduler = optim.lr_scheduler.MultiStepLR(optimizer, range(0,3000,300), gamma=0.3)

    def train_epoch(i):
        """
        Conduct i-th training iteration
        :param i: which iteration is going on
        :return: loss on training set, AUC & AUPR on test set
        """
        model.zero_grad()

        # 这里就是调用改过之后的模型
        score = model(train_data["gene_feature"],
                      train_data["phenotype_feature"],
                      train_data["gene_sim"],
                      train_data["pheno_sim"],
                      train_data["relation"])
        # score = model(train_data["gene_feature"],
        #               train_data["phenotype_feature"])
        trn_loss = criterion(train_data["train_annotation"], score)

        # print log info every iterations
        if i % 25 == 0:
            test_auc, test_aupr = test_metric(train_data["test_label"], score, train_data["test_idx"])
        else:
            test_auc, test_aupr = 0, 0

        trn_loss.backward()
        # torch.nn.utils.clip_grad_norm(model.parameters(), max_norm=20)
        if trn_loss != trn_loss:
            raise Exception('NaN in Loss, crack!')
        optimizer.step()
        scheduler.step()
        return trn_loss, test_auc, test_aupr

     # conduct training for total of 3000 iterations
    train_loss = []
    train_acc = []
    for epoch in range(Epoch):
        trn_loss, tst_auc, tst_aupr = train_epoch(epoch)
        train_loss.append(trn_loss.item())
        print("Epoch", epoch, "\t", trn_loss.item(), "\t", tst_auc, "\t", tst_aupr)

    with open('train_loss.txt', 'w') as train_los:
        train_los.write(str(train_loss))

    # return the final predicted score
    return model(train_data["gene_feature"],
                      train_data["phenotype_feature"],
                      train_data["gene_sim"],
                      train_data["pheno_sim"],
                      train_data["relation"]
    )
def evaluate():
    # file_path = os.path.dirname(__file__)
    # file_name = os.path.abspath(os.path.join(file_path, 'dataset/'))

    adjPD = np.load('adjGP.npy')
    # adjPD = np.load('../分析/GWAS/adjGP.npy')
    Y_pred = np.load('dataset/predicted_score.npy')

    # 保存为CSV文件
    pd.DataFrame(adjPD).to_csv('adjGP.csv', index=False, header=False)
    pd.DataFrame(Y_pred).to_csv('predicted_score.csv', index=False, header=False)


    # retain only predictions not in train set
    cur_AUC, cur_AUPR, cur_NDCG10, cur_MAP, cur_MRR, cur_MRR10, cur_ROC = \
        evaluation_fun.evaluation_all(Y_pred[test_index], adjPD[test_index])
    print('AUC:', cur_AUC, '........', 'AUPR:', cur_AUPR)

    # print("Y_pred[test_index]:")
    # # 打印出来
    # for i in range(0, len(test_index), 10):  # 每次打印10个元素，避免过多数据
    #     print(Y_pred[test_index[i:i+10]])
    #
    # print("adjPD[test_index]:")
    # for i in range(0, len(test_index), 10):  # 每次打印10个元素
    #     print(adjPD[test_index[i:i+10]])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # dataset/phenoSim.npy
    #Adding necessary input arguments
    parser.add_argument("--file_path", default='/', type=str, help="the folder that store files")
    parser.add_argument("--piRSim",default='dataset/geneSim.npy', type=str, help="the file name of piRNA Similarity npy file")  # dataset/geneSim.npy
    parser.add_argument("--DisSim", type=str, default='test_phenoSim.npy', help="the file name of Disease Similarity npy file")
    # parser.add_argument("--PD_fold_label", type=str, help="the file name of PD_fold_label npy file")
    parser.add_argument("--adjGP", default='adjGP.npy', type=str, help="the file name of piRNA-disease adjacent matrix npy file")
    parser.add_argument("--GP_ben_ind_label", default='GP_ben_ind_label.npy', type=str, help="the file name of piRNA-disease adjacent matrix npy file")
    parser.add_argument("--Epoch", type=int, default=250, help="Epochs")
    parser.add_argument("--lr", type=float, default=0.00000000000000001, help="Learning Rate")
    parser.add_argument("--weight_decay", type=float, default=1.0, help="weight decay factor")

    # parser.add_argument("--piRSim",default='../分析/acute/geneSim_acute.npy', type=str, help="the file name of piRNA Similarity npy file")  # dataset/geneSim.npy
    # parser.add_argument("--DisSim", type=str, default='test_phenoSim.npy', help="the file name of Disease Similarity npy file")
    # # parser.add_argument("--PD_fold_label", type=str, help="the file name of PD_fold_label npy file")
    # parser.add_argument("--adjGP", default='../分析/acute/adjGP_acute.npy', type=str, help="the file name of piRNA-disease adjacent matrix npy file")
    # parser.add_argument("--GP_ben_ind_label", default='../分析/acute/GP_ben_ind_label_acute.npy', type=str, help="the file name of piRNA-disease adjacent matrix npy file")
    # parser.add_argument("--Epoch", type=int, default=250, help="Epochs")
    # parser.add_argument("--lr", type=float, default=0.00000000000000001, help="Learning Rate")
    # parser.add_argument("--weight_decay", type=float, default=1.0, help="weight decay factor")

    args = parser.parse_args()

    # load data
    GS_seq, PS_doid, adjGP, GP_ben_ind_label = import_data(args.piRSim, args.DisSim, args.adjGP, args.GP_ben_ind_label)

    print(adjGP.shape)  #
    print(GS_seq.shape) # 1254, 1254
    print(PS_doid.shape) # 5846, 5846
    print(GP_ben_ind_label.shape)

    # the number of gene and phenotype
    m_gene, n_pheno = adjGP.shape

    pred_score = np.zeros((m_gene, n_pheno))


    # 这里写rwr对相似网络提取的代码
    # 先用单位矩阵代替
    gene_feature = rwr(GS_seq, 0.8)
    pheno_feature = rwr(PS_doid,0.8)
    # poly_pheno = PolynomialFeatures(3, include_bias=False)
    # dis_features = poly_pheno.fit_transform(pheno_feature1)

    # load index
    train_index = np.where((GP_ben_ind_label>0) | (-11>GP_ben_ind_label))
    test_index = np.where((GP_ben_ind_label<0) & (-11<GP_ben_ind_label))
    train_pos_index = np.where((GP_ben_ind_label == 1))
    test_pos_index = np.where((GP_ben_ind_label == -1))

    train_mask = np.zeros(adjGP.shape)
    train_annotation = np.zeros(adjGP.shape)
    test_annotation = np.zeros(adjGP.shape)

    # apply mask to extract know annotations
    train_mask[train_pos_index] = 1
    train_annotation[train_pos_index] = 1
    test_annotation[test_pos_index] = 1

    # construct gene-phenotype block matrix, size: (m+n, m+n), with similarity matrix diag=1
    gene = np.zeros((m_gene,m_gene))
    row_id, col_id = np.diag_indices_from(gene)
    gene[row_id, col_id] = 1

    pheno = np.zeros((n_pheno,n_pheno))
    row_id, col_id = np.diag_indices_from(pheno)
    pheno[row_id,col_id] = 1

    rel = np.concatenate((
        np.concatenate((gene, train_mask), axis=1),
        np.concatenate((train_mask.T, pheno), axis=1)
    ),axis=0)

    # emphasize the positive labels
    train_annotation[train_mask == 1] = 5

    # assemble the training data(这里后期加上gene和hpo的相似网络和节点特征)
    train_data = {
        "gene_feature": t.FloatTensor(gene_feature).to(device),
        "phenotype_feature": t.FloatTensor(pheno_feature).to(device),
        "gene_sim": t.FloatTensor(GS_seq).to(device),
        "pheno_sim": t.FloatTensor(PS_doid).to(device),
        "train_annotation": t.FloatTensor(train_annotation).to(device),
        "train_label": t.FloatTensor(train_annotation[train_index]).to(device),
        "train_index": train_index,
        "relation": t.FloatTensor(rel).to(device),
        "test_annotation": t.FloatTensor(test_annotation).to(device),
        "test_label": adjGP[test_index],
        "test_idx": test_index,
    }

    # create our model
    model = GCMC(m_gene, n_pheno,gene_feature,pheno_feature) #后期传入gene和phenotype的特征矩阵
    #model = model_iPiDA_GCN.GCMC(m_gene, n_pheno,gene_feature,pheno_feature)
    #model = model_HPOFiller.GCMC(m_gene, n_pheno)
    #model = model_HPODNets.Model(m_gene, n_pheno, m_gene)
    model.to(device)

    # data_check = np.isinf(train_annotation[train_index]).all().all()
    # res = np.isnan(train_annotation[train_index]).all().all()
    # print(data_check)
    # print(res)

    # create optimizer
    optimizer = optim.RMSprop(model.parameters(), args.lr, args.weight_decay)  #adjust learning rate

    # make prediction for all gene-phenotype associations
    Y_pred = fit(model, train_data, optimizer, args.Epoch)
    Y_pred = Y_pred.detach().cpu().numpy()

    #save the result
    file_name = os.path.dirname(__file__) + '/dataset/predicted_score.npy'
    np.save(file_name, Y_pred)
    evaluate()



