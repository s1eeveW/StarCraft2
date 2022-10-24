import copy
import os
import numpy as np
import cv2

dataset = []
count = 0
replay = 0
# 记录所有事件
feature_set = []
# 扫描一遍后，所有事件维度的dictionary
data_dictionary = dict()

# 读入csv文件
for pa in range(1, 372):
    path = 'D:/Final/Banshee/Lose/' + str(pa) + '.csv'
    deter = False
    count += 1
    while(deter == False):
        if os.path.exists(path):
            path = 'D:/Final/Banshee/Lose/' + str(pa) + '.csv'
            break
        else:
            print(1)
            pa += 1
            path = 'D:/Final/Banshee/Lose/' + str(pa) + '.csv'

    # 导入csv
    try:
        # print(count)
        fileIn = open(path)
        for i in fileIn.readlines():
            lines = i.strip()
            if (lines != ''):
                dataset.append(lines)
    except:
        # print(count)
        continue

    for i in range(0, len(dataset)):
        if str(dataset[i]) not in data_dictionary.keys():
            # 将event导入dictionary并将value设为0
            data_dictionary[str(dataset[i])] = 0
    # 记录所有event
    feature_set.append(dataset)
    dataset = []

# 输出一共多少events
print("There are %d events(images)" % len(feature_set))

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

# print(feature[191])
# print(feature)

def image_size(feature):
    length = 0
    size = len(feature)
    image = np.zeros((224, 224, 3))

    for i in range(0, 224):
        for j in range(0, 224):
            for k in range(0, 3):
                if length < size:
                    image[i][j][k] = feature[length]
                    length += 1
                else:
                    return image
for i in range(0, len(feature)):
    image = []
    image = image_size(feature[i])
    # if i == 0:
    #     print(image)
    path = r'D:/programming/Projects/TCAV/images/New/Lose/' + str(i) + '.png'
    cv2.imwrite(path, image)
    # if i == 0:
    #     pathi = r"D:/Images/Target/" + str(i) + "target.png"
    #     image = cv2.imread(pathi)
    #     print(image)

#
# from PIL import Image
# import numpy as np
#
# L_path = 'D:/Images/Target/0target.jpeg'
# L_image = Image.open(L_path)
# out = L_image.convert("RGB")
# img = np.array(out)
#
# # print(out.size)
# # print(img.shape)#高 宽 三原色分为三个二维矩阵
# print(img)
#
# image = cv2.imread("D:/Images/Target/0target.jpeg")
# print(image)
#
