from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
import matplotlib.pylab as plt
from sklearn.metrics import silhouette_score
import copy
import gc
import math
from umap import UMAP
from sklearn.decomposition import PCA
# import umap
# from sklearn.preprocessing import StandardScaler
import numpy as np
# np.set_printoptions(threshold=np.inf)
import os
import csv
import sys

def min_n(list1, num):
    return sorted(list1, reverse=False)[:num]

dataset = []
count = 0
replay = 0
# 记录所有事件
feature_set = []
# 扫描一遍后，所有事件维度的dictionary
data_dictionary = dict()

# 读入csv文件
for pa in range(1, 726):
    path = 'D:/SC/HeroMarineccc/' + str(pa) + '.csv'
    deter = False
    while(deter == False):
        if os.path.exists(path):
            path = 'D:/SC/HeroMarineccc/' + str(pa) + '.csv'
            break
        else:
            pa += 1
            path = 'D:/SC/HeroMarineccc/' + str(pa) + '.csv'

    # 导入csv
    try:
        fileIn = open(path)
        for i in fileIn.readlines():
            lines = i.strip()
            if (lines != ''):
                dataset.append(lines)
    except:
        continue

    for i in range(0, len(dataset)):
        if str(dataset[i]) not in data_dictionary.keys():
            # 将event导入dictionary并将value设为0
            data_dictionary[str(dataset[i])] = 0
    # 记录所有event
    feature_set.append(dataset)
    dataset = []

# 输出一共多少replays
# 输出一共多少events
print("There are %d events" % len(feature_set))
# feature_set = np.asarray(feature_set, dtype=np.float16)
feature = []
for i in range(0, len(feature_set)):
    compared_dictionary = dict()
    # 每次都初始化到value=0的dictionary
    compared_dictionary = copy.deepcopy(data_dictionary)
    for j in range(0, len(feature_set[i])):
        if str(feature_set[i][j]) in compared_dictionary.keys():
            # tag k=3 player clustering 最相近的几个cluster提出来做evaluation
            # 匹配成功后，将dictionary里的值加一
            count = compared_dictionary[feature_set[i][j]]
            count += 1
            compared_dictionary[str(feature_set[i][j])] = count

    # 单个replay的全部event匹配完成后，将字典转成list存入feature 2d list
    feature.append(list(compared_dictionary.values()))
    # print(sys.getsizeof(compared_dictionary))
    del compared_dictionary
    # print(sys.getsizeof(feature))
    # gc.collect()
# print(feature[0:2])

# 测试dimension
# print(feature)
# print(len(feature))
# print(len(feature[0]))
# print(len(feature[10]))
# print(len(feature[100]))

# PCA + KMeans
lower_dimension = PCA(n_components=50).fit_transform(feature)
embedding = UMAP(random_state=42).fit_transform(feature)
print(len(embedding))
scores = []
for i in range(3, 11):
    kmeans = KMeans(init='k-means++', n_clusters=i, max_iter=300, n_init=10, random_state=0)
    kmeans.fit(embedding)
    score = silhouette_score(embedding, kmeans.labels_, metric='euclidean', sample_size=len(embedding))
    scores.append(score)

best_num = scores.index(np.max(scores))
best_num = best_num + 2
#
km = KMeans(init='k-means++', n_clusters=best_num, max_iter=300, n_init=10, random_state=0)
y_label = km.fit_predict(embedding)
# # centroid = km.cluster_centers_
for i in range(0, best_num):
    plt.scatter(embedding[y_label == i, 0], embedding[y_label == i, 1], s=30, edgecolors='k', label='cluster'+str(i+1))
plt.legend(bbox_to_anchor=(1.35, 1), loc='upper right')
plt.title("Clustering replays of three different race players\nby K-Means")
plt.tight_layout()
plt.show()

# t-sne
# 求聚类的方差和平均数
db = DBSCAN(eps=0.625, min_samples=30)
y_pred = db.fit_predict(embedding)
plt.scatter(embedding[y_pred == -1, 0], embedding[y_pred == -1, 1], s=30, c='black', edgecolors='k', label='outlier(s)')
for i in range(0, max(db.labels_)+1):
    plt.scatter(embedding[y_pred == i, 0], embedding[y_pred == i, 1], s=30, edgecolors='k', label='cluster'+str(i+1))
plt.legend(bbox_to_anchor=(1.35, 1), loc='upper right')
plt.title("Clustering replays of three different race players\nby DBSCAN")
plt.tight_layout()
plt.show()

print("\n")
print("K-Means:")
number = 0
KMx = []
KMy = []
for i in range(0, best_num):
    number = i + 1
    KMx.append(np.mean(embedding[y_label == i, 0]))
    KMy.append(np.mean(embedding[y_label == i, 1]))
    print("Cluster %d mean x-axis:" % number, np.mean(embedding[y_label == i, 0]))
    print("Cluster %d mean y-axis:" % number, np.mean(embedding[y_label == i, 1]))
    # print("Cluster %d variance x-axis:" % number, np.var(embedding[y_label == i, 0]))
    # print("Cluster %d variance y-axis:" % number, np.var(embedding[y_label == i, 1]))

print("\n")
print("DBSCAN:")
number = 0
DBx = []
DBy = []
for i in range(0, max(db.labels_)+1):
    number = i + 1
    DBx.append(np.mean(embedding[y_pred == i, 0]))
    DBy.append(np.mean(embedding[y_pred == i, 1]))
    print("Cluster %d mean x-axis:" % number, DBx[i])
    print("Cluster %d mean y-axis:" % number, DBy[i])
    # print("Cluster %d variance x-axis:" % number, np.var(embedding[y_pred == i, 0]))
    # print("Cluster %d variance y-axis:" % number, np.var(embedding[y_pred == i, 1]))

print("\n")
print(KMx)
print(KMy)
dislist = []
disdict = dict()
for count in range(0, best_num):
    result = []
    for i in range(0, len(embedding)):
        tempx = abs(embedding[i, 0] - KMx[count])
        tempy = abs(embedding[i, 1] - KMy[count])
        distance = math.sqrt(pow(tempy, 2) + pow(tempx, 2))
        disdict[str(distance)] = str(i)
        dislist.append(distance)
    dislist = min_n(dislist, 10)
    for j in range(0, len(dislist)):
        result.append(str(disdict[str(dislist[j])]))
    print(result)
    dislist.clear()
    disdict.clear()

print("\n")
print(DBx)
print(DBy)
for count in range(0, max(db.labels_)+1):
    result = []
    for i in range(0, len(embedding)):
        tempx = abs(embedding[i, 0] - DBx[count])
        tempy = abs(embedding[i, 1] - DBy[count])
        distance = math.sqrt(pow(tempy, 2) + pow(tempx, 2))
        disdict[str(distance)] = str(i)
        dislist.append(distance)
    dislist = min_n(dislist, 10)
    for j in range(0, len(dislist)):
        result.append(str(disdict[str(dislist[j])]))
    print(result)
    dislist.clear()
    disdict.clear()
#
#     # plt.annotate('cluster' + str(i + 1), (centroid[i, 0], centroid[i, 1]))