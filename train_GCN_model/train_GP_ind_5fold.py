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
from sklearn.model_selection import KFold
import model_HPOFiller, model_HPODNets, model_iPiDA_GCN

# set random generator seed to allow reproducibility
t.manual_seed(66)
np.random.seed(66)

# assign cuda device ID
device = "cuda:0"
device = t.device('cuda')


def import_data(piRSim, DisSim, adjGP, GP_ben_ind_label):
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
    model.train()
    criterion = nn.MSELoss(reduction='sum')
    scheduler = optim.lr_scheduler.MultiStepLR(optimizer, range(0, 3000, 300), gamma=0.3)

    def train_epoch(i):
        """
        Conduct i-th training iteration
        :param i: which iteration is going on
        :return: loss on training set, AUC & AUPR on test set
        """
        model.zero_grad()
        score = model(train_data["gene_feature"],
                      train_data["phenotype_feature"],
                      train_data["gene_sim"],
                      train_data["pheno_sim"],
                      train_data["relation"])
        trn_loss = criterion(train_data["train_annotation"], score)
        if i % 25 == 0:
            test_auc, test_aupr = test_metric(train_data["test_label"], score, train_data["test_idx"])
        else:
            test_auc, test_aupr = 0, 0

        trn_loss.backward()
        optimizer.step()
        scheduler.step()
        return trn_loss, test_auc, test_aupr

    train_loss = []
    train_acc = []
    for epoch in range(Epoch):
        trn_loss, tst_auc, tst_aupr = train_epoch(epoch)
        train_loss.append(trn_loss.item())
        print("Epoch", epoch, "\t", trn_loss.item(), "\t", tst_auc, "\t", tst_aupr)

    return model(train_data["gene_feature"],
                 train_data["phenotype_feature"],
                 train_data["gene_sim"],
                 train_data["pheno_sim"],
                 train_data["relation"])


def evaluate():
    adjPD = np.load('adjGP.npy')
    Y_pred = np.load('dataset/predicted_score.npy')

    cur_AUC, cur_AUPR, cur_NDCG10, cur_MAP, cur_MRR, cur_MRR10, cur_ROC = \
        evaluation_fun.evaluation_all(Y_pred[test_index], adjPD[test_index])
    print('AUC:', cur_AUC, '........', 'AUPR:', cur_AUPR)
    return cur_AUC, cur_AUPR


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--piRSim", default='dataset/geneSim.npy', type=str,
                        help="the file name of piRNA Similarity npy file")
    parser.add_argument("--DisSim", type=str, default='test_phenoSim.npy',
                        help="the file name of Disease Similarity npy file")
    parser.add_argument("--adjGP", default='adjGP.npy', type=str,
                        help="the file name of piRNA-disease adjacent matrix npy file")
    parser.add_argument("--GP_ben_ind_label", default='GP_ben_ind_label.npy', type=str,
                        help="the file name of piRNA-disease adjacent matrix npy file")
    parser.add_argument("--Epoch", type=int, default=200, help="Epochs")
    parser.add_argument("--lr", type=float, default=0.00000000000000001, help="Learning Rate")
    parser.add_argument("--weight_decay", type=float, default=1.0, help="weight decay factor")

    args = parser.parse_args()

    GS_seq, PS_doid, adjGP, GP_ben_ind_label = import_data(args.piRSim, args.DisSim, args.adjGP, args.GP_ben_ind_label)

    print(sum(sum(adjGP)))
    print(GS_seq.shape)
    print(PS_doid.shape)

    m_gene, n_pheno = adjGP.shape

    pred_score = np.zeros((m_gene, n_pheno))

    gene_feature = rwr(GS_seq, 0.8)
    pheno_feature = rwr(PS_doid, 0.8)

    # 初始化五折交叉验证
    kf_gene = KFold(n_splits=5, shuffle=True, random_state=42)
    kf_hpo = KFold(n_splits=5, shuffle=True, random_state=42)

    auc_scores=[]
    aupr_scores=[]


    # 遍历每一折
    for fold, ((train_gene_idx, test_gene_idx), (train_hpo_idx, test_hpo_idx)) in enumerate(
            zip(kf_gene.split(range(1254)), kf_hpo.split(range(5846)))):
        # 提取训练基因和表型的索引
        train_gene = np.array(train_gene_idx)
        train_hpo = np.array(train_hpo_idx)

        # 从 GP_ben_ind_label 中读取训练矩阵
        train_matrix = GP_ben_ind_label[np.ix_(train_gene, train_hpo)]

        print(f"Fold {fold + 1}")

        train_pos_index = np.where((GP_ben_ind_label == 1))
        test_pos_index = np.where((GP_ben_ind_label == -1))

        train_mask = np.zeros(adjGP.shape)
        train_annotation = np.zeros(adjGP.shape)
        test_annotation = np.zeros(adjGP.shape)

        train_mask[train_pos_index] = 1
        train_annotation[train_pos_index] = 1
        test_annotation[test_pos_index] = 1

        gene = np.zeros((m_gene, m_gene))
        row_id, col_id = np.diag_indices_from(gene)
        gene[row_id, col_id] = 1

        pheno = np.zeros((n_pheno, n_pheno))
        row_id, col_id = np.diag_indices_from(pheno)
        pheno[row_id, col_id] = 1

        rel = np.concatenate((np.concatenate((gene, train_mask), axis=1),
                              np.concatenate((train_mask.T, pheno), axis=1)), axis=0)

        train_annotation[train_mask == 1] = 5

        train_index = np.where((train_matrix > 0) | (-11 > train_matrix))
        test_index = np.where((train_matrix < 0) & (-11 < train_matrix))

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
        #model = GCMC(m_gene, n_pheno, gene_feature, pheno_feature)
        model = model_HPOFiller.GCMC(m_gene, n_pheno)
        model.to(device)

        optimizer = optim.RMSprop(model.parameters(), args.lr, args.weight_decay)

        # fit the model for each fold
        Y_pred = fit(model, train_data, optimizer, args.Epoch)
        Y_pred = Y_pred.detach().cpu().numpy()

        # save the result for each fold
        fold_file_name = os.path.dirname(__file__) + f'/dataset/predicted_score_fold_{fold + 1}.npy'
        np.save(fold_file_name, Y_pred)
        auc, aupr = evaluate()

        # 记录AUC和AUPR
        auc_scores.append(auc)
        aupr_scores.append(aupr)

    # 输出平均结果
    print(f"Average AUC: {np.mean(auc_scores)}")
    print(f"Average AUPR: {np.mean(aupr_scores)}")
