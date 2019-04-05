# -*- coding: utf-8 -*-
"""
Created on Fri Apr  5 16:33:45 2019

@author: Chris
"""
AA_CODE={"A":"U","T":"A","G":"C","C":"G"}
START_CODE = ('AUG')#起始子
END_CODE = ('UAA', 'UAG', 'UGA')#终止子
P_TABLE = {'UUU': 'F', 'CUU': 'L', 'AUU': 'I', 'GUU': 'V', \
           'UUC': 'F', 'CUC': 'L', 'AUC': 'I', 'GUC': 'V', \
           'UUA': 'L', 'CUA': 'L', 'AUA': 'I', 'GUA': 'V', \
           'UUG': 'L', 'CUG': 'L', 'AUG': 'M', 'GUG': 'V', \
           'UCU': 'S', 'CCU': 'P', 'ACU': 'T', 'GCU': 'A', \
           'UCC': 'S', 'CCC': 'P', 'ACC': 'T', 'GCC': 'A', \
           'UCA': 'S', 'CCA': 'P', 'ACA': 'T', 'GCA': 'A', \
           'UCG': 'S', 'CCG': 'P', 'ACG': 'T', 'GCG': 'A', \
           'UAU': 'Y', 'CAU': 'H', 'AAU': 'N', 'GAU': 'D', \
           'UAC': 'Y', 'CAC': 'H', 'AAC': 'N', 'GAC': 'D', \
           'UAA': '*', 'CAA': 'Q', 'AAA': 'K', 'GAA': 'E', \
           'UAG': '*', 'CAG': 'Q', 'AAG': 'K', 'GAG': 'E', \
           'UGU': 'C', 'CGU': 'R', 'AGU': 'S', 'GGU': 'G', \
           'UGC': 'C', 'CGC': 'R', 'AGC': 'S', 'GGC': 'G', \
           'UGA': '*', 'CGA': 'R', 'AGA': 'R', 'GGA': 'G', \
           'UGG': 'W', 'CGG': 'R', 'AGG': 'R', 'GGG': 'G'
                 }


def compute(tmp,k,p,P_TABLE):
    #因为每种密码子一次之变一个
    #字典找到当前对应的
    #然后改变那一位碱基
    #再比较是否相同就行
    #返回两个值，即同义突变和非同义突变各自地概率之和
    #k为具体地类型，p为0，1，2其中之一
    #经了解发现，还需要三个三个地输入才行,tmp就是所在的code
    tmp=tmp.replace('T','U')
    comflag=P_TABLE[tmp]#获取匹配对象
    al=3
    same=0
    tocomp=""
    if(k in ['U','C','A','G']):
        #数据输入正常，进行计算
        for i in ['U','C','A','G']:
            #除了自己每个都要替换一遍
            if(i!=k):
                #替换对应的那一位
                if(p==0):
                    #替换第一位
                    tocomp=i+tmp[1:len(tmp)]
                elif(p==1):
                    #替换第二位
                    tocomp=tmp[0]+i+tmp[-1]
                else:
                    #替换第三位
                    tocomp=tmp[0:len(tmp)-1]+i
                print(tocomp,'tocomp')
            else:
                continue
            if(comflag==P_TABLE[tocomp]):
                #氨基酸没有发生变化
                same+=1
            else:
                same+=0
        
        return (al-same)/al,same/al
    else:
        print("数据输入错误! ",k)
        return -1
    
def comD(A):
    #这个函数返回的还是一个元组，分别是dn和ds
    #A是一个形如‘AUGACUAGU’的字符串
    dn=0
    ds=0
    tmp=""
    A=A.replace('T','U')
    #print("我要开动啦")
    for i in range(0,len(A)):
        #print(tmp)
        tmp+=A[i]
        if(len(tmp)==3):
            #凑成了一个密码子可以带入函数了！
            print(tmp)
            for j in range(0,3):    
                score12=compute(tmp,tmp[j],j,P_TABLE)
                print(score12)
                dn+=score12[0]
                ds+=score12[1]
            tmp=""
    print(dn,ds)
    return dn,ds

def comS(A,B,dic):
    sn=0
    ss=0
    #每三位进行比对氨基酸是否相等
    if(len(A)!=len(B)):
        print("数据输入错误")
        return -1
    A=A.replace('T','U')
    B=B.replace('T','U')
    tmpA=""
    tmpB=""
    for i in range(0,len(A)):
        tmpA+=A[i]
        tmpB+=B[i]
        if(len(tmpB)==3):
            if(dic[tmpA]==dic[tmpB]):
                if(tmpA==tmpB):
                    sn+=0
                    ss+=0
                else:
                    for k in range(0,len(tmpA)):
                        if(tmpA[k]!=tmpB[k]):
                            ss+=1                   
            else:
                for k in range(0,len(tmpA)):
                    if(tmpA[k]!=tmpB[k]):
                        sn+=1           
            tmpA=""
            tmpB=""           
    return sn,ss
                   
#print(comD(A),comS(A,B,P_TABLE))
    
#输入三个三个一组
#或者说输入数据长度是3地倍数
A=input("Pleaseinputyourfirst serial like 'AGCAGT'.!\n")
B=input("Pleaseinputyoursecond serial .!\n")
#dn,ds,sn,ss在两条链比较的时候需要得到这四个指标
#compute可以通过逐位计算得到
D=comD(A)
S=comS(A,B,P_TABLE)
ans=(S[0]/D[0])/(S[1]/D[1])
print("K_a / k_s = ",ans)