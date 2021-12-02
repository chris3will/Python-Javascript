import numpy as np
import os
from abc import ABCMeta, abstractmethod
import matplotlib.pyplot as plt # 引入图像绘制库


def load(parameters, file):
    params = np.load(file)
    for i in range(len(parameters)):
        parameters[i].data = params[str(i)]


def load_MNIST(file, transform=False):
    file = np.load(file)
    X = file['X']
    Y = file['Y']
    if transform:
        X = X.reshape(len(X), -1)
    return X, Y


# 定义一些比较重要的类结构
class Parameter(object):
    def __init__(self, data, requires_grad, skip_decay=False):
        self.data = data # 数据本身
        self.grad = None # 梯度
        self.skip_decay = skip_decay # 衰减
        self.requires_grad = requires_grad 
    
    @property
    def T(self):
        return self.data.T

class Layer(metaclass=ABCMeta):
    '''
    作为所有层的基类，如果自定义新的层应该从此类继承并重写下面两个方法
    '''
    @abstractmethod
    def forward(self, *args):
        pass

    @abstractmethod
    def backward(self, *args):
        pass


# 批处理归一化层
class BatchNorm(Layer):
    def __init__(self, shape, requires_grad=True, affine=True, is_test=False, **kwargs):
        if affine:
            # 针对输入的归一化不需要仿射变换的参数
            self.gamma = Parameter(np.random.uniform(0.90, 1.10, shape), requires_grad, True)
            self.beta = Parameter(np.random.uniform(-0.1, 0.1, shape), requires_grad, True)
            self.requires_grad = requires_grad
        self.eps = 1e-7
        self.affine = affine
        self.is_test = is_test
        self.coe = 0.02
        self.overall_var = Parameter(np.zeros(shape), False)
        self.overall_ave = Parameter(np.zeros(shape), False)

    def forward(self, x):
        if self.is_test:
            # 进行测试时使用估计的训练集的整体方差和均值进行归一化
            sample_ave = self.overall_ave.data
            sample_std = np.sqrt(self.overall_var.data)
        else:
            # 进行训练时使用样本的均值和方差对训练集整体的均值和方差进行估计（使用加权平均的方法）
            sample_ave = x.mean(axis=0)
            sample_var = x.var(axis=0)
            sample_std = np.sqrt(sample_var + self.eps)
            self.overall_ave.data = (1 - self.coe) * self.overall_ave.data + self.coe * sample_ave
            self.overall_var.data = (1 - self.coe) * self.overall_var.data + self.coe * sample_var
        return (x - sample_ave) / sample_std if not self.affine else self.forward_internal(x - sample_ave, sample_std)

    def backward(self, delta):
        if not self.affine: return              # 如果是针对输入层做归一化就不存在向上传播梯度了
        self.beta.grad = delta.mean(axis=0)
        self.gamma.grad = (delta * self.normalized).mean(axis=0)
        return self.gamma_s * (delta - self.normalized * self.gamma.grad - self.beta.grad)

    def forward_internal(self, sample_diff, sample_std):
        '''
        如果是在网络内部使用Batch Norm需要进一步进行仿射变化，如果是对输入进行归一化就不用了
        '''
        self.normalized = sample_diff / sample_std
        self.gamma_s = self.gamma.data / sample_std
        return self.gamma.data * self.normalized + self.beta.data


# 线性层
class Linear(Layer):
    def __init__(self, shape, requires_grad=True, bias=True, **kwargs):
        '''
        shape: (in_size, out_size)
        requires_grad: 是否在反向传播中计算权重梯度
        bias: 是否设置偏置
        '''
        W = np.random.randn(*shape) * (2 / shape[0]**0.5)
        self.W = Parameter(W, requires_grad)
        self.b = Parameter(np.zeros(shape[-1]), requires_grad) if bias else None
        self.require_grad = requires_grad

    def forward(self, x):
        if self.require_grad: self.x = x
        # 公式：a_{ik}=\sum_{j}^{C} x_{ij} w_{jk}
        a = np.dot(x, self.W.data)
        if self.b is not None: a += self.b.data
        return a

    def backward(self, delta):
        # 在反向计算中矩阵乘法涉及转置，einsum比dot稍好一点点
        if self.require_grad:
            batch_size = delta.shape[0]
            # 公式：dW_{ik}=\frac {1}{N} \sum_{j}^{C} x_{ji} da_{jk}
            self.W.grad = np.einsum('ji,jk->ik', self.x, delta) / batch_size
            # 公式：db_{*}=\frac {1}{N} \sum_{i}^{N} da_{i*}
            if self.b is not None: self.b.grad = np.einsum('i...->...', delta, optimize=True) / batch_size
        # 公式：dz_{ik}=\sum_{j}^{C} da_{ij} w_{kj}
        return np.einsum('ij,kj->ik', delta, self.W.data, optimize=True)
        
class Relu(Layer):
    def forward(self, x):
        self.x = x
        return np.maximum(0, x)

    def backward(self, delta):
        delta[self.x<=0] = 0
        return delta

class Softmax(Layer):
    def forward(self, x):
        '''
        x.shape = (N, C)
        接收批量的输入，每个输入是一维向量
        计算公式为：
        a_{ij}=\frac{e^{x_{ij}}}{\sum_{j}^{C} e^{x_{ij}}}
        '''
        v = np.exp(x - x.max(axis=-1, keepdims=True))    
        return v / v.sum(axis=-1, keepdims=True)
    
    def backward(self, y):
        # 一般Softmax的反向传播和CrossEntropyLoss的放在一起
        pass

class Net(Layer):
    def __init__(self, layer_configures):
        self.layers = []
        self.parameters = []
        for config in layer_configures:
            self.layers.append(self.createLayer(config))

    def createLayer(self, config):
        '''
        继承的子类添加自定义层可重写此方法
        '''
        return self.getDefaultLayer(config)

    def forward(self, x):
        for layer in self.layers:
            x = layer.forward(x)
        return x
    
    def backward(self, delta):
        for layer in self.layers[::-1]:
            delta = layer.backward(delta)
        return delta

    def getDefaultLayer(self, config):
        t = config['type']
        if t == 'linear':
            layer = Linear(**config)
            self.parameters.append(layer.W)
            if layer.b is not None: self.parameters.append(layer.b)
        elif t == 'relu':
            layer = Relu()
        elif t == 'softmax':
            layer = Softmax()
        elif t == 'batchnorm':
            layer = BatchNorm(**config)
        else:
            raise TypeError
        return layer


class Adam(object):
    def __init__(self, parameters, learning_rate, decay=0, beta1=0.9, beta2=0.999, eps=1e-8):
        self.beta1 = beta1
        self.beta2 = beta2
        self.accumulated_beta1 = 1
        self.accumulated_beta2 = 1
        self.learning_rate = learning_rate
        self.decay_rate = 1.0 - decay
        self.eps = eps
        self.parameters = [p for p in parameters if p.requires_grad]
        self.accumulated_grad_mom = [np.zeros(p.data.shape) for p in self.parameters]
        self.accumulated_grad_rms = [np.zeros(p.data.shape) for p in self.parameters]

    def update(self):
        self.accumulated_beta1 *= self.beta1
        self.accumulated_beta2 *= self.beta2
        learning_rate = self.learning_rate * ((1 - self.accumulated_beta2)**0.5) / (1 - self.accumulated_beta1)
        for p, grad_mom, grad_rms in zip(self.parameters, self.accumulated_grad_mom, self.accumulated_grad_rms):
            if self.decay_rate < 1 and not p.skip_decay: p.data *= self.decay_rate
            np.copyto(grad_mom, self.beta1 * grad_mom + (1 - self.beta1) * p.grad)
            np.copyto(grad_rms, self.beta2 * grad_rms + (1 - self.beta2) * np.power(p.grad, 2))
            p.data -= learning_rate * grad_mom / (np.sqrt(grad_rms) + self.eps)

#交叉熵损失函数
class CrossEntropyLoss(object):
    def __init__(self):
        # 内置一个softmax作为分类器
        self.classifier = Softmax()

    def gradient(self):
        return self.grad

    def __call__(self, a, y, requires_acc=True):
        '''
        a: 批量的样本输出
        y: 批量的样本真值
        requires_acc: 是否输出正确率
        return: 该批样本的平均损失[, 正确率]

        输出与真值的shape是一样的，并且都是批量的，单个输出与真值是一维向量
        a.shape = y.shape = (N, C)      N是该批样本的数量，C是单个样本最终输出向量的长度
        '''
        # 网络的输出不应该经过softmax分类，而在交叉熵损失函数中进行
        a = self.classifier.forward(a)
        # 提前计算好梯度
        self.grad = a - y  # 也是之后需要返回的内容，可以理解为方向
        # 样本整体损失
        # L_{i}=-\sum_{j}^{C} y_{ij} \ln a_{ij}
        # 样本的平均损失
        # L_{mean}=\frac{1}{N} \sum_{i}^{N} L_{i}=-\frac{1}{N} \sum_{i}^{N} \sum_{j}^{C} y_{ij} \ln a_{ij}
        # print(y,y.shape)
        # print(np.log(a))
        loss = -1 * np.einsum('ij,ij->', y, np.log(a), optimize=True) / y.shape[0]
 
        if requires_acc:
            acc = np.argmax(a, axis=-1) == np.argmax(y, axis=-1)
            return acc.mean(), loss
        return loss

def train(net, loss_fn, train_file, batch_size, optimizer, load_file,  times=1, retrain=False):
    X, Y = load_MNIST(train_file, transform=True)
    # print("before train, show the data format")
    # print(X,X.shape)
    # print(Y,Y.shape)
    data_size = X.shape[0]
    if not retrain and os.path.isfile(load_file): load(net.parameters, load_file)
    for loop in range(times):
        i = 0
        while i + batch_size <= data_size:
            # 进行批处理，每次向损失函数送入1批数据，并再这批数据处理之前先进行归一化
            x = X[i:i+batch_size]
            y = Y[i:i+batch_size]
            i += batch_size
            # print(i,"i iteration")
            output = net.forward(x) # 先得到输出层结果
            batch_acc, batch_loss = loss_fn(output, y) # 交叉熵函数计算具体的损失
            delta = loss_fn.gradient()
            net.backward(delta)
            optimizer.update()
            if i % 50 == 0:
                print("loop: %d, batch: %5d, batch acc: %2.1f, batch loss: %.2f" % \
                    (loop, i, batch_acc*100, batch_loss))
        pass



if __name__ == "__main__": 
    layers = [
        {'type': 'batchnorm', 'shape': 784, 'requires_grad': False, 'affine': False}, # 因为输入层，不需要仿射变换
        {'type': 'linear', 'shape': (784, 512)},
        {'type': 'batchnorm', 'shape': 512},
        {'type': 'relu'},
        {'type': 'linear', 'shape': (512, 128)},
        {'type': 'batchnorm', 'shape': 128},
        {'type': 'relu'},
        {'type': 'linear', 'shape': (128, 10)}
    ]
    loss_fn = CrossEntropyLoss()
    net = Net(layers)
    learning_rate = 0.002
    batch_size = 256
    optimizer = Adam(net.parameters, learning_rate)
    train_file = './MNIST/trainset.npz'
    
    train(net, loss_fn, train_file, batch_size, optimizer, None,  times=1, retrain=True)
