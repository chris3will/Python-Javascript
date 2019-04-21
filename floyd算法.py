# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 12:53:45 2019

@author: Chris
"""

import sys
import numpy as np
#输入权矩阵
#计算每个位置权值的变化
#n维矩阵n词迭代后dij即为所求
'''
a=np.array([
        [0,20,100000,100000,15,100000],
        [20,0,20,60,25,100000],
        [100000,20,0,30,18,100000],
        [100000,60,30,0,100000,100000],
        [15,25,18,100000,0,15],
        [100000,100000,100000,100000,15,0]])
'''

a=np.array([
    [0,10,14,1000,1000,1000,1000,1000],
    [10,0,1000,10,10,1000,1000,1000],
    [14,1000,0,5,1000,1000,5,1000],
    [1000,10,5,0,5,4,7,1000],
    [1000,10,1000,5,0,6,1000,13],
    [1000,1000,1000,4,6,0,4,1000],
    [1000,1000,5,7,1000,4,0,9],
    [1000,1000,1000,1000,13,1000,9,0]
])

def shift(matrix,generation):
    #迭代矩阵用的，输入的即上一代矩阵
    tmp=matrix
    for i in range(generation+1):
        for j in range(generation+1):
            tmp[i][j]=min(matrix[i][j],matrix[i][generation-1]+matrix[generation-1][j])
    
    return tmp

generationmax=len(a)
generation=0
while(generation<generationmax):
    generation+=1
    a=shift(a,generation)
    print(generation,a)


print("final\n",a)
    