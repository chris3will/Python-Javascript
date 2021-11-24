import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def born113(N:int = 100):
    '''
    返回113页所对应题目的内容矩阵
    这里需要用到np.mat的一些操作
    然后再进行mat到array的一些转换
    '''
    a0 = np.mat(np.eye(N,N),np.float64) # 先定义一个N阶单位矩阵
    a1 = np.mat(np.eye(N-1,N-1),np.float64) # 在定义一个N-1阶单位矩阵，之后将会利用到np的一些特性操作

    a11 = np.diag(a1) # 获取单位阵a1的对角线元素，全是1
    a12 = np.diag(a11,1) # 把a11的元素放在一个全零矩阵的对角线的上一位

    A = a12.T + a12 + (-2) * a0     

    b = np.zeros((N,1),np.float64)
    b[0]=b[N-1]=-1

    return np.array(A),b


def conjugate(A:np.ndarray,b:np.ndarray,x0:np.array,epsilon:np.float64):
    
    r0 = b-A.dot(x0)
    d0 = r0
    err = [r0]
    for i in range(b.shape[0]*2):
        # 这个是由理论公式提供的次数限制
        a = r0.T.dot(r0) / d0.T.dot(A).dot(d0)
        x = x0 + a * d0
        r = b - A.dot(x)
        err.append(r)
        if np.linalg.norm(r)<=epsilon:
            x0 = x
            break
        
        beta = np.linalg.norm(r)**2 / np.linalg.norm(r0) ** 2
        d = r + beta*d0

        x0 = x
        r0 = r
        d0 = d

    return x0,err

def steepest(A:np.ndarray, b:np.ndarray, x0:np.array, epsilon:np.float64,iter_max:int):
    
    loss = []
    for i in range(iter_max):
        r = A.dot(x0) - b
        alpha = r.T.dot(r) / r.T.dot(A).dot(r)

        x = x0 - alpha*r
        loss.append(r)
        if np.linalg.norm(r)<=epsilon:
            x0 = x
            break
        
        x0 = x

    return x0,loss

def plot_curve(x,c,points=None):
    '''
    根据提供的参数绘制曲线，散点
    '''
    func = np.poly1d(c)
    y = func(x)
    plt.plot(x,y)
    for item in points:
            plt.scatter(item[0],item[1],c='r')
    plt.xlabel('x')
    plt.ylabel('y(x)')
    plt.savefig('c_cruve'+'.jpg')



def plot_loss(loss,method_name="iteration",points=None):
    '''
    打印误差图像，有必要的时候加入其散点
    '''
    sns.set()
    plt.yscale('log')
    

    idx_x = [i for i in range(1,len(loss)+1)]
    plt.plot(idx_x,[np.linalg.norm(l) for l in loss])
    plt.xlabel('iter round')
    plt.ylabel('loss')
    plt.title(method_name)

    if points:
        # 如果有点的集合需要打印
        for item in points:
            plt.scatter(item[0],item[1],c='r')
    # plt.show()

    plt.savefig(f'{method_name}.jpg')
    plt.clf()


if __name__ == '__main__':
    # 实现梯度下降法

    # A = np.asarray([[2, 0, 1], [0, 1, 0], [1, 0, 2]], dtype=np.float64)
    # b = np.asarray([[3], [1], [3]], dtype=np.float64)
    # x0 = np.asarray([[0], [0], [0]], dtype=np.float64)
    N = 400
    A,b = born113(N)
    # print(A,b)
    x0 = np.zeros((N,1),np.float64)

    print(np.linalg.solve(A,b),"直接利用内置函数求解")


    epsilon = 1e-4
    ans0,err0 = conjugate(A,b,x0,epsilon)
    # print(ans0,err0,type(err0))
    plot_loss(err0,'conjugate_size_{}'.format(N))

    ans1,err1 = steepest(A,b,x0,epsilon,1000)
    print(ans1)
    plot_loss(err1,'steepest_size_{}'.format(N))
