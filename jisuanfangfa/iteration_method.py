# 解决第三题的各种方法
# 注意引用tool_method.py中的可行方法
# 核心思路也是，把非线性方程组的求解问题，转变为线性方程组求解，这个时候时关于delta_x的线性方程组

import numpy as np
import matplotlib.pyplot as plt
import math
from numpy.core.fromnumeric import var
import sympy as sym

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
    
    # x0 = np.asarray([[1.04],[0.47]],np.float64)
    print("进行第二题的问题求解")
    x0 = np.asarray([1.04,0.47],np.float64)
    x1 = sym.Symbol('x1')
    x2 = sym.Symbol('x2')
    func1 = sym.cos(x1**2+0.4*x2) + x1**2 + x2**2-1.6
    func2 = 1.5*x1**2 - (1/0.36)*x2**2 - 1

    return [func1,func2,x1,x2,x0]

def delta_A(A0_inv:np.ndarray,s1:np.ndarray,y1:np.ndarray):
    '''
    直接返回增量的add项
    inv_A 矩阵
    s 列向量
    y 列向量
    '''
    return ((s1 - A0_inv.dot(y1)).dot(s1.T).dot(A0_inv)) / (s1.T.dot(A0_inv).dot(y1))


def solve_second_question_broyden():
    '''
    第二大题的第二小问，利用布罗伊登法求解。
    '''

    # 获取必要的参数内容
    func1,func2,x1,x2,x0 = born240_2()
    func1_1 = sym.diff(func1,x1)
    func1_2 = sym.diff(func1,x2)
    func2_1 = sym.diff(func2,x1)
    func2_2 = sym.diff(func2,x2)

    # Broyden法求解
    '''
    确定初始向量x0
    给定两个误差标准epsilon1，epsilon2
    设置最大迭代次数iter_max
    根据初始向量计算迭代需要的矩阵A0
    根据A0计算出x1，接着就开始不断的迭代过程即可

    '''
    print("第二大题第二小问的布罗伊登解法开始")
    x0 = x0.reshape(-1,1)
    epsilon1 = epsilon2 = 1e-8
    iter_max = 200
    A0 = np.asarray([
        [func1_1.subs([(x1,x0[0][0]),(x2,x0[1][0])]), func1_2.subs([(x1,x0[0][0]),(x2,x0[1][0])])],
        [func2_1.subs([(x1,x0[0][0]),(x2,x0[1][0])]), func2_2.subs([(x1,x0[0][0]), (x2,x0[1][0])])]
    ],np.float64)

    fx0 = np.asarray([
        func1.subs({x1:x0[0][0],x2:x0[1][0]}),
        func2.subs({x1:x0[0][0], x2:x0[1][0]})
    ],np.float64).reshape(-1,1)

    inv_A0 = np.linalg.inv(A0)
    x_1 = x0 - inv_A0.dot(fx0)

    # print(inv_A0,x_1,"before iteration, show the vairables")
    for epoch in (1,iter_max):
        s1 = x_1 - x0
        fx1 = np.asarray([
            func1.subs({x1:x_1[0][0], x2:x_1[1][0]}),
            func2.subs({x1:x_1[0][0], x2:x_1[1][0]})
        ],np.float64).reshape(-1,1)
        fx0 = np.asarray([
            func1.subs({x1:x0[0][0],x2:x0[1][0]}),
            func2.subs({x1:x0[0][0], x2:x0[1][0]})
        ],np.float64).reshape(-1,1)
        y1 = fx1 - fx0

        inv_A1 = inv_A0 + delta_A(inv_A0,s1,y1)
        x_2 = x_1 - inv_A1.dot(fx1)

        fx2 = np.asarray([
            func1.subs({x1:x_2[0][0], x2:x_2[1][0]}),
            func2.subs({x1:x_2[0][0], x2:x_2[1][0]})
        ],np.float64).reshape(-1,1)
        # print(fx2,"首次打印fx2")
        # print(x_2-x_1,type(x_2-x_1),"输出x2-x1")
        # print(np.linalg.norm(x_2-x_1),"输出第一项指标")
        # # break
        if np.linalg.norm(x_2-x_1) <= epsilon1 or np.linalg.norm(fx2) <= epsilon2:
            print(f'stop at epoch: {epoch}')
            break
        
        x0 = x_1
        x_1 = x_2
        inv_A0 = inv_A1
    
    print(x_2,"结果即为所求，(2)问的布罗伊登解法")


def solve_second_question_secant():
    '''
    求解第二大题的第三小问，利用弦割法处理
    取一个较小的h来参与计算
    用差商代替偏导，减少了一部分计算
    对于f_ij^k 需要表达出一个e_j*h的概念
    e_j利用numpy生成列向量，然后对一位进行修改即可。
    
    '''
    epsilon1 = 1e-8
    epsilon2 = 1e-8
    h = 0.1 # 取的一个间隔长度
    iter_max = 200 # 最大迭代次数

    func1,func2,x1,x2,x0 = born240_2()
    
    func1_1 = sym.diff(func1,x1)
    func1_2 = sym.diff(func1,x2)
    func2_1 = sym.diff(func2,x1)
    func2_2 = sym.diff(func2,x2)
    print("开始进行弦割法处理**************")
    for epoch in range(1,100):
        new_J = (1/h)*np.asarray([
            [func1.subs([(x1,x0[0]+h),(x2,x0[1])]) - func1.subs([(x1,x0[0]),(x2,x0[1])]), func1.subs({x1:x0[0],x2:x0[1]+h}) - func1.subs({x1:x0[0],x2:x0[1]})],
            [func2.subs([(x1,x0[0]+h),(x2,x0[1])]) - func2.subs([(x1,x0[0]),(x2,x0[1])]), func2.subs({x1:x0[0],x2:x0[1]+h}) - func2.subs({x1:x0[0],x2:x0[1]})]
        ],np.float64)
        print(new_J,"after iteration show the new J")
        b = np.asarray([
            [-1*func1.subs({x1:x0[0],x2:x0[1]})],
            [-1*func2.subs({x1:x0[0],x2:x0[1]})]
        ],np.float64)

        print(b,"after iteration show the b")

        delta_x = np.linalg.solve(new_J,b) # 调用库方法进行求解

        print(delta_x,"观察计算的delta")
        x0 = x0.reshape(-1,1)
        x0 = x0 + delta_x
        fnx = np.asarray([
            [func1.subs({x1:x0[0][0],x2:x0[1][0]})],
            [func2.subs({x1:x0[0][0],x2:x0[1][0]})]
        ],np.float64)

        # if np.linalg.norm(delta_x) < epsilon1 or np.linalg.norm(fnx)  < epsilon2:
        #     print("stop at epoch : {}".format(epoch))
        #     break

        if  np.linalg.norm(delta_x) < epsilon1 or np.linalg.norm(fnx) < epsilon2:
            print("stop at epoch : {}".format(epoch))
            break

        x0 = x0.reshape(-1)
        print(x0,'观察x0')

    print(x0,"迭代结果即为所求")


def solve_second_question_newtwon(method:str = None):
    '''
    第二大题的第二问
    为解决题目，提供更直接的内容思路

    '''
    
    func1,func2,x1,x2,x0 = born240_2()
    print(func1,func2,"打印两个方程")
    # 打印求导的结果
    func1_1 = sym.diff(func1,x1)
    func1_2 = sym.diff(func1,x2)
    func2_1 = sym.diff(func2,x1)
    func2_2 = sym.diff(func2,x2)
    print(func1_1,"1,x1偏导数")
    print(func1_2,"1,x2偏导数")
    func_J = lambda x: np.array([
        [func1_1.subs({x1:x[0],x2:x[1]}),func1_2.subs({x1:x[0],x2:[1]})],
        [func2_1.subs({x1:x[0],x2:x[1]}),func2_2.subs({x1:x[0],x2:x[1]})]
    ],np.float64)

    func_b = lambda x: np.array([
        [func1.subs({x1:x[0],x2:x[1]})],
        [func2.subs({x1:x[0],x2:x[1]})]
    ],np.float64)

    
    # 用牛顿法解决

    epsilon1 = 1e-8
    epsilon2 = 1e-8
    iter_max = 200
    vars = [x1,x2] 
    vals = [x0[0],x0[1]]
    # for item in vals:
    #     print(item,type(item),"传入之前观察类型")
    for epoch in range(1,iter_max):
        print(x0,"迭代前观察一下x")
        J = np.asarray([
            [func1_1.subs([(x1,x0[0]),(x2,x0[1])]),func1_2.subs({x1:x0[0],x2:x0[1]})],
            [func2_1.subs([(x1,x0[0]),(x2,x0[1])]),func2_2.subs({x1:x0[0],x2:x0[1]})]
        ],np.float64)
        print(J,"after iteration show the J")
        b = np.asarray([
            [-1*func1.subs({x1:x0[0],x2:x0[1]})],
            [-1*func2.subs({x1:x0[0],x2:x0[1]})]
        ],np.float64)
        print(b,"after iteration show the b")

        delta_x = np.linalg.solve(J,b) # 调用库方法进行求解

        print(delta_x,np.shape(delta_x),"观察计算的delta形式")

        # 先将x0变为列向量
        x0 = x0.reshape(-1,1)

        x0 = x0 + delta_x
        
        vals = [x0[0][0],x0[1][0]]
        # print(vals,type(vals),"print vals")
        # print(x0,type(x0),"print x0")
        # print(delta_x,type(delta_x),"print delta_x")

        fnx = np.asarray([
            [func1.subs({x1:x0[0][0],x2:x0[1][0]})],
            [func2.subs({x1:x0[0][0],x2:x0[1][0]})]
        ],np.float64)

        if (np.linalg.norm(x0-delta_x)!=0 and np.linalg.norm(delta_x) / np.linalg.norm(x0-delta_x)) < epsilon1 or np.linalg.norm(fnx)  < epsilon2:
            print("stop at epoch : {}".format(epoch))
            break
        # 再将x0恢复数组
        x0 = x0.reshape(-1)
    
    print(x0,"迭代结果即为所求")



def second_question_first():

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
    print("start newtown method")
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

    iter_max = 100 # 先设置迭代次数上限

    # 从库中引入共轭梯度法求解方程
    from tool_method import conjugate

    # 以下为牛顿法,针对(1)题进行求解
    epsilon1 = 1e-8
    epsilon2 = 1e-8
    stop = 0
    for epoch in range(iter_max):
        J = np.asarray([
            [func1_1(x0),func1_2(x0),func1_3(x0)],
            [func2_1(x0),func2_2(x0),func2_3(x0)],
            [func3_1(x0),func3_2(x0),func3_3(x0)]
        ],np.float64)
        print(J,"打印J")
        print(np.linalg.inv(J),"打印J的逆矩阵")
        b1 = -1 * func1(x0)
        b2 = -1 * func2(x0)
        b3 = -1 * func3(x0)
        b = np.asarray([b1,b2,b3],np.float64)
        # print(J,np.shape(J),"分别观察shape J")
        # print(b, np.shape(b),"分别观察shape b")

        # 我可能必须要把数据处理为矩阵传入，这样才能保证求解
        # delta_x,err = conjugate(J,b,x0,1e-8) # 实践证明，在矩阵不稀疏的情况下，利用共轭梯度法求解反而会没有效果
        
        delta_x = np.linalg.solve(J,b) # 调用库方法得到一组解

        # print(J,delta_x,np.shape(delta_x),"观察一次结果 (J,delta_x,shape(delta_x)")
        
        # 然后更新原始的x
        x0 = x0 +delta_x
        # print(x0,np.shape(x0),"观察x0的正常更新")
        # break # 为了观察一次迭代后的结果形式

        if (np.linalg.norm(x0-delta_x)!=0 and np.linalg.norm(delta_x) / np.linalg.norm(x0-delta_x)) < epsilon1 or np.linalg.norm([-func1(x0),-func2(x0),-func3(x0)]) < epsilon2:
            print("stop at epoch : {}".format(epoch))
            break

    print(x0,"结果即为所求,牛顿法解第(1)题的结果")

    # 布罗伊登法求解问题
    # Broyden法求解
    '''
    确定初始向量x0
    给定两个误差标准epsilon1，epsilon2
    设置最大迭代次数iter_max
    根据初始向量计算迭代需要的矩阵A0
    根据A0计算出x1，接着就开始不断的迭代过程即可

    '''
    
    print("start broyden method")
    # 重置x0的情况
    x0 = np.asarray([[1],[1],[1]],np.float64) # 采用一个数组的形式进行的定义，这样数据的类型会根据其出现的位置动态调整p
    A0 = np.asarray([
            [func1_1(x0),func1_2(x0),func1_3(x0)],
            [func2_1(x0),func2_2(x0),func2_3(x0)],
            [func3_1(x0),func3_2(x0),func3_3(x0)]
        ],np.float64)
    print(A0,"init A0")
    fx0 = np.asarray([
        func1(x0),
        func2(x0),
        func3(x0)
    ],np.float64).reshape(-1,1)    
    x1 = x0 - np.linalg.inv(A0).dot(fx0)
    # print(x1,"打印计算一次后的x1")

    for i in range(1,iter_max):
        # 开始进行迭代
        # print(f'{i} epoch')
        s1 = x1 - x0
        # print("s1",s1,type(s1))
        fx1 = np.asarray([
            func1(x1),
            func2(x1),
            func3(x1)
        ],np.float64).reshape(-1,1)
        # print("fx1",fx1,type(fx1))
        fx0 = np.asarray([
            func1(x0),
            func2(x0),
            func3(x0)
        ],np.float64).reshape(-1,1)    
        y1 = fx1 - fx0
        # print(y1,"打印y1，观察fx前后的差值")
        A0_inv = np.linalg.inv(A0)
        # print("invA0",A0_inv,type(A0_inv))
        A1_inv = A0_inv + delta_A(A0_inv,s1,y1)
        # print("invA1",A1_inv,type(A1_inv))

        x2 = x1 - A1_inv.dot(fx1)
        # print("x2",x2)
        # 判断终止条件
        fx2 = np.asarray([
            func1(x2),
            func2(x2),
            func3(x2)
        ],np.float64).reshape(-1,1)
        # print(fx2,"观察fx2的迭代情况")
        # print((x2-x1),np.linalg.norm(x2-x1),"观察x向量做差")
        # break

        if np.linalg.norm(x2-x1) < epsilon1 or np.linalg.norm(fx2) < epsilon2:
            print(f'stop at epoch {epoch}')
            x1 = x2
            break   
        
        # 每次循环结束，更新变量

        x0 = x1
        x1 = x2
        A0_inv = A1_inv # 这个之前忘了更新了
    
    print(x1,"结果即为所求，布罗伊登法求解第(1)题结果")


    # 开始用弦割法
    print("开始用弦割法解决第二大题第一小问的方程****************")
    # 重置必要参数
    h = 0.1
    x0 = np.asarray([[1],[1],[1]],np.float64) # 采用一个数组的形式进行的定义，这样数据的类型会根据其出现的位置动态调整p

    for epoch in range(1,iter_max):
        new_J = np.asarray([
            [func1(x0+np.asarray([[h],[0],[0]])) - func1(x0), func1(x0 + np.asarray([[0],[h],[0]])) - func1(x0), func1(x0 + np.asarray([[0],[0],[h]])) - func1(x0)],
            [func2(x0+np.asarray([[h],[0],[0]])) - func2(x0), func2(x0 + np.asarray([[0],[h],[0]])) - func2(x0), func2(x0 + np.asarray([[0],[0],[h]])) - func2(x0)],
            [func3(x0+np.asarray([[h],[0],[0]])) - func3(x0), func3(x0 + np.asarray([[0],[h],[0]])) - func3(x0), func3(x0 + np.asarray([[0],[0],[h]])) - func3(x0)],
        ],np.float64)

        b1 = -1 * func1(x0)
        b2 = -1 * func2(x0)
        b3 = -1 * func3(x0)
        b = np.asarray([b1,b2,b3],np.float64)


        delta_x = np.linalg.solve(J,b) # 调用库方法得到一组解

        x0 = x0 +delta_x
        
        if np.linalg.norm(delta_x) < epsilon1 or np.linalg.norm([-func1(x0),-func2(x0),-func3(x0)]) < epsilon2:
            print("stop at epoch : {}".format(epoch))
            break

    print(x0,"结果即为所求,弦割法解第(1)题的结果")
    
if __name__ == '__main__':

    # first_question()
    second_question_first()
    # solve_second_question_secant()
    # solve_second_question_newtwon()
    # solve_second_question_broyden()
