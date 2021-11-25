# 解决第三题的各种方法
# 注意引用tool_method.py中的可行方法
# 核心思路也是，把非线性方程组的求解问题，转变为线性方程组求解，这个时候时关于delta_x的线性方程组

import numpy as np
import matplotlib.pyplot as plt
import math

def divide_range(func,a,b,length = 0.05):
    '''
    规定一个默认的隔离区间长度
    '''
    if  b - a < length:
        return [[a,b]] if func(a) * func(b)<0 else []
    
    mid = (a + b) / 2
    ret = divide_range(func,a,mid,length)
    ret.extend(divide_range(func,mid,b,length))
    return ret

def simple_iteration(func,x0,epsilon1,epsilon2):
    # 自己构造表达式
    # 从最高次开始尝试
    func_fai = lambda x: math.pow(5*x**5 - 3*x**4 -x**3+7*x**2-7*x +20,1/6)
    max_iter = 202 # 设置最大迭代次数
    x = x0
    for i in range(1,max_iter):
        x0 = func_fai(x0)
        print(f'{i}->{x0}')
        if abs(x0-func(x0)) < epsilon1 or abs(x0-x)<epsilon2:
            break
        x = x0

    return x0

def newtwon_method(func,a,b,epsilon1,epsilon2):
    '''
    牛顿法迭代
    利用泰勒展开进行快速迭代
    '''
    Q = np.polyder(func) # 先求出来导数
    x0 = (a+b) / 2  # 初始点先选取为区间中点，做该点的切线
    max_iter = 200 # 设置迭代次数
    x = x0
    for i in range(1,max_iter):
        x0 = x0 - np.polyval(func,x0) / np.polyval(Q,x0)
        print(f'{i}->{x0}')
        if abs(x0 - np.polyval(func,x0))<epsilon1 or abs(x0-x) < epsilon2:
            break
        x = x0
    
    return x0
        
def secant_method(func,a,b,epsilon1,epsilon2):
    '''
    弦割法实现，把x0点就选为初始点，或者一个边界，都可以试试
    func : 因为是牛顿法的改进，所以传入的func也是系数
    '''
    # 取有边界为x0点
    x_ = b
    x0 = (a+b)/2
    x = x0
    max_iter = 200 # 设置最大迭代次数
    for i in range(1,max_iter):
        x0 = x0 - np.polyval(func,(x0))*(x0-x_) / (np.polyval(func,(x0)) - np.polyval(func,(x_)))
        print(f'{i}->{x0}')
        if abs(x0 - np.polyval(func,x0)) < epsilon1 or abs(x0 - x) < epsilon2:
            break
        x = x0
    
    return x0

    


def first_question():
    # 首先要利用二分法进行根的隔离问题
    epsilon1 = 1e-8
    epsilon2 = 1e-8

    func = lambda x: x**6  - 5*x**5 + 3*x**4 + x**3 -7*x**2 + 7*x -20
    P = [1,-5,3,1,-7,7,20] # 定义多项式系数
    ranges = divide_range(func,-1,5) # 给定二分法依据函数，以及总区间范围，返回隔离区间 

    for range in ranges:
        # 对每一个隔离区间进行处理

        print(range,"隔离区间")
        # 从隔离区间的中点开始迭代
        x0 = (range[0]+ range[1])/2

        # 简单迭代法
        print("start simple iteration")
        simple = simple_iteration(func,x0,epsilon1,epsilon2)

        # 牛顿法
        print("start newtwon_method iteration")
        newtwon = newtwon_method(P,range[0],range[1],epsilon1,epsilon2)

        # 弦割法 不用特别点的切线，而是用两点连线来处理 Secant method
        print("start secant_method iteration")
        secant = secant_method(P,range[0],range[1],epsilon1,epsilon2)

def born240_2():
    '''
    针对p240 7.3 （2）进行求解的过程
    利用sympy库对函数进行参数化定义
    '''
    import

def second_question():

    '''
    初始向量x0 = [1,1,1]'
    方程组
    [
        [x1^2+x2^2+x3^2-1]
        [2*x1^2 + x2^2 - 4*x3]
        [3*x1^2 - 4*x2^2 +x3^2]
    ]
    '''
    # 7.3 题
    # 1 先把每个方程表示出来
    # 2 再把每个方程关于不同变量的导数求解出来，放在矩阵的对应位置上
    # 3 得到了这个新的J_f矩阵
    x0 = np.asarray([[1],[1],[1]],np.float64)
    func1 = lambda x : x[0]**2 + x[1]**2 + x[2]**2 - 1
    func2 = lambda x : 2*x[0]**2 + x[1]**2 - 4*x[2]
    func3 = lambda x : 3*x[0]**2 - 4*x[1]**2 + x[2]**2

    # func1对x1求导
    func1_1 = lambda x: 2*x[0]
    # func1对x2求导
    func1_2 = lambda x: 2*x[1]

    func1_3 = lambda x: 2*x[2]

    # func2 对x1求导
    func2_1 = lambda x: 4*x[0]
    func2_2 = lambda x: 2*x[1]
    func2_3 = lambda x: -4

    # func3 对x1求导
    func3_1 = lambda x: 6*x[0]
    func3_2 = lambda x: -8*x[1]
    func3_3 = lambda x: 2*x[2]

    iter_max = 10 # 先设置迭代次数上限

    # 从库中引入共轭梯度法求解方程
    from tool_method import conjugate

    # 以下为牛顿法,针对(1)题进行求解
    epsilon1 = 1e-8
    epsilon2 = 1e-8
    stop = 0
    for epoch in range(iter_max):
        J = np.array([
            [func1_1(x0),func1_2(x0),func1_3(x0)],
            [func2_1(x0),func2_2(x0),func2_3(x0)],
            [func3_1(x0),func3_2(x0),func3_3(x0)]
        ],np.float64)
        b1 = -1 * func1(x0)
        b2 = -1 * func2(x0)
        b3 = -1 * func3(x0)
        b = np.asarray([b1,b2,b3],np.float64)
        # print(J,np.shape(J),"分别观察shape J")
        # print(b, np.shape(b),"分别观察shape b")

        # 我可能必须要把数据处理为矩阵传入，这样才能保证求解
        # delta_x,err = conjugate(J,b,x0,1e-8) # 实践证明，在矩阵不稀疏的情况下，利用共轭梯度法求解反而会没有效果
        
        delta_x = np.linalg.solve(J,b) # 调用库方法得到一组解

        print(delta_x,np.shape(delta_x),"观察一次结果")
        
        # 然后更新原始的x
        x0 = x0 +delta_x
        # print(x0,np.shape(x0),"观察x0的正常更新")
        # break # 为了观察一次迭代后的结果形式

        if (np.linalg.norm(x0-delta_x)!=0 and np.linalg.norm(delta_x) / np.linalg.norm(x0-delta_x)) < epsilon1 or np.linalg.norm([-func1(x0),-func2(x0),-func3(x0)]) < epsilon2:
            print("stop at epoch : {}".format(epoch))
            break

    print(x0,"结果即为所求")

if __name__ == '__main__':

    first_question()
    # second_question()
