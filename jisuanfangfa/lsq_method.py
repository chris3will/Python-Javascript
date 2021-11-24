import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import math

# 实现最小二乘拟合问题
# 参考p176 5.1

# 如何构造方程P154页下的形式比较关键

def sum_idx(lst,p_num):
    '''
    返回序列lst的 p_num指数次和
    '''
    ret = 0
    for item in lst:
        ret += math.pow(item,p_num)
    return ret

def sum_idx_with_y(lstx,lsty,p_num):
    '''
    返回序列lstx的指数次与lsty对应元素乘积的和
    '''
    ret = 0
    for idx,item in enumerate(lstx):
        ret += math.pow(item,p_num)*lsty[idx]
    return ret

def born154(n:int,x,y):
    '''
    n 记录了待求多项式的次数
    而矩阵维度是 n + 1
    根据给定的x和y序列，返回相应的矩阵
    A.dot(x) = b
    '''
    A = []
    for i in range(0,n+1):
        # 矩阵的维度是n+1
        row = [] # 单独生成每一行的对应元素
        for j in range(i,i+n+1):
            row.append(sum_idx(x,j))
    
        A.append(row)
    A = np.asarray(A,np.float64)

    print(A,"观察生成的A")

    b = []
    for i in range(0,n+1):
        b.append([sum_idx_with_y(x,y,i)])
    b = np.asarray(b,np.float64)
    print(b,"观察生成的b")

    return A,b

if __name__ == '__main__':
    x = np.array([i for i in range(1,10,1)]) / 10
    y = np.array([5.1234,5.3057,5.5687,5.9375,6.4370,7.0978,7.9493,9.0253,10.3627])
    N = 4 # 我需要拟合的多项式的最高次
    A,b = born154(N,x,y)
    c0 = np.zeros((N+1,1),np.float64)
    from tool_method import conjugate,plot_loss,plot_curve
    
    c,err = conjugate(A,b,c0,1e-8) 
    print(c,np.shape(c))

    plot_loss(err,'conjugate')
    c = np.transpose(c)
    c = c[0]
    points = zip(x,y)
    plot_curve(x,c[::-1],points)



