# !/usr/bin/python
# coding=utf-8
#########################################
# kNN: k Nearest Neighbors

#  输入:      newInput:  (1xN)的待分类向量
#             dataSet:   (NxM)的训练数据集
#             labels:     训练数据集的类别标签向量
#             k:         近邻数

# 输出:     可能性最大的分类标签
#########################################
'''
2019/4/10
修改成排序，输出数据集中哪一个和输入样本最接近和最不可能的
老师提供三组数据，即得到三组排序结果
课堂笔记
#1计算距离
#2对距离排序
#3选出k个邻近的
#4计算k个邻近的样本不同类别的数量
#5返回出现次数最多的类别的标签

6,0.5,1.2,0.38
5,0.3,0.7,0.2
1,0.2,2,0.7
结果
1:j
2:j
3:c

最远的都是t

'''
import numpy as np


# 创建一个数据集，包含2个类别共4个样本
def createDataSet():
    # 生成一个矩阵，每行表示一个样本
    import csv
    csv_file_r = open('data1.csv', 'r', newline='')
    csv_reader = csv.reader(csv_file_r, delimiter=',', quotechar='"')
    next(csv_reader)#第一行的跳过，可以把标题跳过去
    x_data = []
    y_data = []
    for row in csv_reader:
        #print(row)
        x_data.append([float(row[0]), float(row[1]), float(row[2]), float(row[3])])
        y_data.append(row[4])

    #print(y_data)
    return np.array(x_data), y_data


# KNN分类算法函数定义
def kNNClassify(newInput, dataSet, labels, k):
    #把建模和预测函数放在了一起
    numSamples = dataSet.shape[0]  # shape[0]表示行数

    # # step 1: 计算距离[
    # 假如：
    # Newinput：[1,0,2]
    # Dataset:
    # [1,0,1]
    # [2,1,3]
    # [1,0,2]
    # 计算过程即为：
    # 1、求差
    # [1,0,1]       [1,0,2]
    # [2,1,3]   --   [1,0,2]
    # [1,0,2]       [1,0,2]
    # =
    # [0,0,-1]
    # [1,1,1]
    # [0,0,-1]
    # 2、对差值平方
    # [0,0,1]
    # [1,1,1]
    # [0,0,1]
    # 3、将平方后的差值累加
    # [1]
    # [3]
    # [1]
    # 4、将上一步骤的值求开方，即得距离
    # [1]
    # [1.73]
    # [1]
    #
    
    # tile(A, reps): 构造一个矩阵，通过A重复reps次得到
    # the following copy numSamples rows for dataSet
    diff = np.tile(newInput, (numSamples, 1)) - dataSet  # 按元素求差值
    print(diff)
    squaredDiff = diff ** 2  # 将差值平方
    squaredDist = np.sum(squaredDiff, axis=1)  # 按行累加
    distance = squaredDist ** 0.5  # 将差值平方和求开方，即得距离

    # # step 2: 对距离排序
    # argsort() 返回排序后的索引值
    print(labels,"old")
    print(distance,"olddistance")
    sortedDistIndices = np.argsort(distance)#按照distance的大小返回一个对应长度的各个地方的索引值
    print(sortedDistIndices,"newdistance")
    classCount = {}  # define a dictionary (can be append element)
    print(labels,"labels")
    for i in range(k):
        # # step 3: 选择k个最近邻
        voteLabel = labels[sortedDistIndices[i]]#改这一行 改成 numSamples-i-1

        # # step 4: 计算k个最近邻中各类别出现的次数
        # when the key voteLabel is not in dictionary classCount, get()
        # will return 0
        classCount[voteLabel] = classCount.get(voteLabel, 0) + 1

    # # step 5: 返回出现次数最多的类别标签
    maxCount = 0
    for key, value in classCount.items():
        if value > maxCount:
            maxCount = value
            maxIndex = key

    return maxIndex


def main():
    dataSet, labels = createDataSet()
    # 定义一个未知类别的数据
    testX = np.array([6,0.5,1.2,0.38])
    k = 3
    # 调用分类函数对未知数据分类
    outputLabel = kNNClassify(testX, dataSet, labels, k)
    print("Your input is:", testX, "and classified to class: ", outputLabel)


if __name__ == '__main__':
    main()

