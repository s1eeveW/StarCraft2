from sklearn.cluster import KMeans
from copy import deepcopy
import numpy as np
# np.set_printoptions(threshold=np.inf)
import os
import csv

dataset = []
count = 0
# 记录所有事件
feature_set = []
# 扫描一遍后，所有事件维度的dictionary
data_dictionary = dict()

# 读入csv文件
for pa in range(56003, 57221):
    path = 'D:/SC2/SCIII/' + str(pa) + '.csv'
    deter = False
    while(deter == False):
        if os.path.exists(path):
            path = 'D:/SC2/SCIII/' + str(pa) + '.csv'
            break
        else:
            pa += 1
            path = 'D:/SC2/SCIII/' + str(pa) + '.csv'

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

# 输出一共多少event
print(len(feature_set))

feature = []
for i in range(0, len(feature_set)):

    # 每次都初始化到value=0的dictionary
    compared_dictionary = deepcopy(data_dictionary)
    for j in range(0, len(feature_set[i])):
        if str(feature_set[i][j]) in compared_dictionary.keys():

            # 匹配成功后，将dictionary里的值加一
            count = compared_dictionary[feature_set[i][j]]
            count += 1
            compared_dictionary[str(feature_set[i][j])] = count

    # 单个replay的全部event匹配完成后，将字典转成list存入feature 2d list
    feature.append(list(compared_dictionary.values()))
    del compared_dictionary

# 测试dimension
print(len(feature))
print(len(feature[0]))
print(len(feature[10]))
print(len(feature[100]))




# 暂时用不到
# compared_dictionary[str(dataset[i])] = 0
# count = compared_dictionary[dataset[i]]
# count += 1
# compared_dictionary[str(dataset[i])] = count

# feature.append(list(compared_dictionary.values()))


# length = len(dataset)
# for i in range(length):
#     dataset[i] += '\n'
# vector = np.array([[0]*7]*length).
# tokens = 0
# count = 0
# col = 0
# row = 0
# for i in dataset:
#     for j in range(len(i)):
#         if dataset[row][j] == ' ':
#             vector[row][col] = count
#             count = 0
#             col += 1
#         elif dataset[row][j] == '\n':
#             vector[row][col] += count
#             count = 0
#             col = 0
#             row += 1
#         else:
#             if dataset[row][j].isdigit() == True:
#                 count += int(dataset[row][j])
#             else:
#                 count += ord(dataset[row][j])
# # print(vector)
#
# # if dataset[1] == dataset[0]:
# #     print(1)
#
# list1 = []
# count = 0
# for i in range(length):
#     for j in range(length):
#         if i != j:
#             if dataset[i] == dataset[j]:
#                 # if dataset[j][0] == '2':
#                 count += 1
#     list1.append(count)
#     count = 0
# print("The number of first ten events: ")
# print(list1[:10])
# # print(len(list1))