# -*- coding: utf-8 -*-
"""
全局最优算法的实现尝试
有一个A,C,G,T(U),-的五阶矩阵
有两个长度不超过三的碱基序列
PPT上的写法有点反人类，行列在这个作业里还是正常点好了
使得程序可以满足如
输入AGG AGC
可以得到AGG- / -AGC
    和AAG- / A-GC
两组结果
暂时不考虑输入格式异常的问题
chris will
xiaozhi
2019/4/5
"""
import numpy as np
import copy
dic={"A":1,"C":2,"G":3,"T":4,"U":4}
dicc={0:1,1:4,2:2}

def compute(i,j,s,SS,SF):
    #i为行号，j为列号，s为距离矩阵,本函数返回SS矩阵位于i行j列的值
    #考虑是构建两个矩阵还是改变当前矩阵中每个元素的值
    if(i==0 and j==0):
        SF[i][j]=0
        return 0
    elif(j==0):
        SF[i][j]=1
        return i*int(s[i][-1])
    elif(i==0):
        SF[i][j]=2
        return j*int(s[-1][j])
    else:
        #矩阵生成完毕
        t1=SS[i-1][j]+int(s[dic[A[i-1]]][-1])#来自上方：1
        t2=SS[i-1][j-1]+int(s[dic[A[i-1]]][dic[B[j-1]]])#来自斜方：4
        t3=SS[i][j-1]+int(s[-1][dic[B[j-1]]])#来自左方：2
        #现在需要找到哪个是最大的，是否有一样大的
        #三个一样大/两个一样大/一个最大
        mn=max(t1,t2,t3)
        flag=[i for i,j in enumerate([t1,t2,t3]) if j==mn]
        #print(flag,[t1,t2,t3])
        if(len(flag)==1):
            #只有一条路径
            SF[i][j]=dicc[flag[0]]
        else:
            #有多条路径
            temp=0
            for k in range(0,len(flag)):
                temp+=dicc[flag[k]]
            SF[i][j]=temp
        return mn
        
#生成目标矩阵，定义结构体推到方向分为三个，斜向下，向右，向下，分别附权重(4,2,1)
def job(A,B):
    #该函数结束之后可以得到SS和SF即全局比对的结果和替代方向矩阵
    if(len(A)==len(B)):
        #满足最基本的条件，其实好像不用
        SS=np.eye(len(A)+1)#SS矩阵
        SF=np.eye(len(A)+1)#SF矩阵，用来记录演变方向
        for i in range(0,len(A)+1):
            for j in range(0,len(B)+1):
                SS[i][j]=compute(i,j,s,SS,SF)
        #print(SS," SS")
        #print(SF," SF" )
    return SS,SF

def multipath(SF,ans,stack,pathstack):
    #每个位置的权重，正在处理的是哪一条路线，堆栈的情况
    #print(ans,"ans!!")
    #print(pathstack," pathstack!!")
    #print(stack," stack!")
    while(len(stack)>0 and len(pathstack)>0):
        pathnum=pathstack.pop()
        
        if(pathnum in ans):
            if(len(ans[pathnum])==len(SF)):
            #这条路已经走到尽头，堆栈中的是留给下一条路的
                multipath(SF,ans,stack,pathstack)
                break
        #开始操作
        #每次循环后匹配链长度加一
        temp1=stack.pop()
        #print(temp1,": temp1")
        #获取当前这个元素，判断前进方向
        #temp1是含有三个元素的列表，分别为行号，列号，和属性值
        if(pathnum not in ans):
            #初始化每一条匹配链
            ans[pathnum]=[]
        
        if(temp1[2]==1):
            #向上,且没有第二条分支
            ans[pathnum].append((A[temp1[0]-1],'-'))
            stack.append([temp1[0]-1,temp1[1],SF[temp1[0]-1][temp1[1]]])
            pathstack.append(pathnum)
            multipath(SF,ans,stack,pathstack)
        elif(temp1[2]==2):
            #向左，且没有第二条分支
            ans[pathnum].append(('-',B[temp1[1]-1]))
            stack.append([temp1[0],temp1[1]-1,SF[temp1[0]][temp1[1]-1]])
            pathstack.append(pathnum)
            multipath(SF,ans,stack,pathstack)
        elif(temp1[2]==4):
            #向斜，且没有第二条分支
            ans[pathnum].append((A[temp1[0]-1],B[temp1[1]-1]))
            stack.append([temp1[0]-1,temp1[1]-1,SF[temp1[0]-1][temp1[1]-1]])
            pathstack.append(pathnum)#俗话说的一条路走到黑
            multipath(SF,ans,stack,pathstack)
        else:
            #多路分支,每个分支先走权重小的,且只要分路，路线条数必增加
            if(temp1[2]==3):
                #上/左
                ans[pathnum+1]=copy.deepcopy(ans[pathnum])
                #先拷贝,确保分路前之前的路径内容都一样
                ans[pathnum].append(('-',B[temp1[0]-1]))#大的,应为左
                ans[pathnum+1].append((A[temp1[0]-1],'-'))
                stack2=copy.deepcopy(stack)#分两条路
                
                stack.append([temp1[0]-1,temp1[1],SF[temp1[0]-1][temp1[1]]])
                stack.append([temp1[0],temp1[1]-1,SF[temp1[0]][temp1[1]-1]])
                pathstack.append(pathnum+1)
                pathstack.append(pathnum)
                
                multipath(SF,ans,stack,pathstack)
                #multipath(SF,ans,stack2,pathstack)
                
                 
            elif(temp1[2]==5):
                #上/斜
                ans[pathnum+1]=copy.deepcopy(ans[pathnum])
                #先拷贝
                #print(ans,"haha")
                ans[pathnum].append((A[temp1[0]-1],B[temp1[1]-1]))
                
                #print(ans,"haha1")
                ans[pathnum+1].append((A[temp1[0]-1],'-'))
                
                #print(ans,"haha2")
                #stack2=copy.deepcopy(stack)#分两条路,但实际上发现拷贝出错
                
                pathstack.append(pathnum+1)
                pathstack.append(pathnum)#大的先走，先走就走老路
                
                stack.append([temp1[0]-1,temp1[1],SF[temp1[0]-1][temp1[1]]])
                stack.append([temp1[0]-1,temp1[1]-1,SF[temp1[0]-1][temp1[1]-1]])
                multipath(SF,ans,stack,pathstack)
                #multipath(SF,ans,stack2,pathstack)
                
                
            elif(temp1[2]==6):
                #左/斜
                ans[pathnum+1]=copy.deepcopy(ans[pathnum])
                #先拷贝
                #print(ans,"haha")
                ans[pathnum].append((A[temp1[0]-1],B[temp1[1]-1]))
                
                #print(ans,"haha1")
                ans[pathnum+1].append(('-',B[temp1[1]-1]))
                
                #print(ans,"haha2")
                #stack2=copy.deepcopy(stack)#分两条路,但实际上发现拷贝出错
                
                pathstack.append(pathnum+1)
                pathstack.append(pathnum)#大的先走，先走就走老路
                
                stack.append([temp1[0],temp1[1]-1,SF[temp1[0]][temp1[1]-1]])
                stack.append([temp1[0]-1,temp1[1]-1,SF[temp1[0]-1][temp1[1]-1]])
                multipath(SF,ans,stack,pathstack)
                #multipath(SF,ans,stack2,pathstack)
                
                
            else:
                #三路分支
                if(temp1[2]==0):
                    pathstack.append(pathnum)
                    multipath(SF,ans,stack,pathstack)
                else:
                    #三条路开始
                    ans[pathnum+1]=copy.deepcopy(ans[pathnum])
                    ans[pathnum+2]=copy.deepcopy(ans[pathnum])
                    #先拷贝
                    #print(ans,"haha")
                    ans[pathnum].append((A[temp1[0]-1],B[temp1[1]-1]))#斜着
                    #print(ans,"haha1")
                    ans[pathnum+1].append(('-',B[temp1[1]-1]))#向左
                    ans[pathnum+2].append((A[temp1[0]-1],B[temp1[1]]))#向上
                    #print(ans,"haha2")
                    #stack2=copy.deepcopy(stack)#分两条路,但实际上发现拷贝出错
                
                    pathstack.append(pathnum+2)
                    pathstack.append(pathnum+1)
                    pathstack.append(pathnum)#大的先走，先走就走老路
                    
                    stack.append([temp1[0]-1,temp1[1],SF[temp1[0]-1][temp1[1]]])
                    stack.append([temp1[0],temp1[1]-1,SF[temp1[0]][temp1[1]-1]])
                    stack.append([temp1[0]-1,temp1[1]-1,SF[temp1[0]-1][temp1[1]-1]])
                    multipath(SF,ans,stack,pathstack)
                    #multipath(SF,ans,stack2,pathstack)
                
                    
    #print(ans,"ans")


def findpath(SS,SF):
    #开始处理SF，从SF矩阵最后一个元素开始判断
    #且每个位置如果是1,2,4则说明只有一条匹配路线，该点匹配之后则跳过
    #如果是3,5,6则是两个点共同的结果要分两条路，如果是7则是三条路替代后的结果
    #每个结果输出两个字符串，即匹配结果匹配的长度应为碱基序列长度加一

    row=len(SF)#当前主要判断元素的行号+1
    col=len(SF[0])
    stack=[]#每条路向下走的时候压栈
    #先判断第一个点位，并将数据导入堆栈。然后进行判断
    pathstack=[]
    if(SF[row-1][col-1]==1 or SF[row-1][col-1]==2 or SF[row-1][col-1]==4):
        pathstack.append(1)
        stack.append([row-1,col-1,SF[row-1][col-1]])
    elif(SF[row-1][col-1]==3):
        pathstack.append(2)
        pathstack.append(1)
        stack.append([row-1,col-1,1])
        stack.append([row-1,col-1,2])
    elif(SF[row-1][col-1]==5):
        
        pathstack.append(2)
        
        pathstack.append(1)
        stack.append([row-1,col-1,1])
        stack.append([row-1,col-1,4])
    elif(SF[row-1][col-1]==6):
        
        pathstack.append(2)
        pathstack.append(1)
        stack.append([row-1,col-1,2])
        stack.append([row-1,col-1,4])
    else:
        
        pathstack.append(3)
        pathstack.append(2)
        pathstack.append(1)
        stack.append([row-1,col-1,1])
        stack.append([row-1,col-1,2])
        stack.append([row-1,col-1,4])
    
    #print(stack)
    #最初的哪那一个碱基位置已经被处理
    #假定最初进行替换只有一条路径
    #计划采用字典来存储不同的路径
    #对应节点采用元组来存储
    ans={}  
    multipath(SF,ans,stack,pathstack)
    #print(ans,": ans")
    #对最后的ans进行处理
    final={}
    for p,i in enumerate(ans):
        #print(ans[i])
        temp1=[]
        temp2=[]
        for k,j in enumerate(ans[i]):
            #print(k,j)
            temp1.append(j[0])
            temp2.append(j[1])
        temp1.reverse()
        temp2.reverse()#注意反转的方式，否则返回的东西很奇葩
        final[p]=[temp1,temp2]
    
    print(' {} answers has been found for you!.'.format(len(ans)))
    print(final)#finall 即为所求
    
#先生成矩阵,让矩阵的行列标可以从1开始
s=np.array([
           ['$','A','C','G','T','-'],
           ['A','2','-7','-5','-7','-5'],
           ['C','-7','2','-7','-5','-5'],
           ['G','-5','-7','2','-7','-5'],
           ['T','-7','-5','-7','2','-5'],
           ['-','-5','-5','-5','-5','0']
           ])

A=input("Please input your first serial which divided by ','.\n")
B=input("Now, input your second serial which divided by ','.\n")
A=A.split(',')
B=B.split(',')

AB=job(A,B)
#已经得到SS,SF    
findpath(AB[0],AB[1])
    
    





    
    
    
    