#采用类的概念将程序封装
#前提是通过简单的观察
#本程序搜索来源为百度图片
#主要输入信息为图片名与所需下载图片数量
#chris 4/21 仅供学习参考
import requests
import re
import json
import os
import random
headers=[
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'},
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
]

class SearchDownload:
    def __init__(self,searchName,maxNum,downPath):
        self.searchName=searchName
        self.maxNum=maxNum
        self.downPath='./download/'+str(searchName)   

    def doWork(self):
        #开始执行下载
        #已经知道API了

        #1确定文件存放位置
        if not os.path.exists('./download/'+str(self.searchName)):
            os.makedirs('./download/'+str(self.searchName))
        
        #这个是发现API每页最多只提供30张图片时采用的加页码策略

        #2组合API准备进行访问工作
        '''
        url="https://m.baidu.com/sf/vsearch/image/browse/wiseresultjson?&word="+ \
            str(self.searchName)+"&rn=30&pn="+str(page)+"&browse_style=1"
        #print(url)
        rawdata=requests.get(url,headers=header)
        data=json.loads(rawdata.text)
        '''
        try:
            hasdown=0
            page=0
            while(hasdown<self.maxNum):
                url="https://m.baidu.com/sf/vsearch/image/browse/wiseresultjson?&word="+ \
                str(self.searchName)+"&rn=30&pn="+str(page*30)+"&browse_style=1"
                #rn最大为30，pn为每页中的具体位置，30，30的更先进就行，因为小循环中是30一轮回，每次继续增加即可
                #print(url)
                rawdata=requests.get(url,headers=random.choice(headers))
                data=json.loads(rawdata.text)
                flag=0
                while(flag<30):
                    msg=data['browse_array'][hasdown%30]
                    image_info=msg['image_info']
                    #只是得到url需要继续request发送请求
                    try:
                        #现在可以解决遇到png或者目标图片源地址拒绝爬虫访问请求时跳过即可
                        #下一步想增加几个选择来匹配原图的格式，使得PNG也可以正常保存，问题在于如果每张图片都要匹配具体的图片类型，会增加程序运行时间
                        #所以实际上爬取过程结束后仍然会有无效图片存在
                        pic=requests.get(image_info['objurl'],timeout=2*random.randint(1,5))
                        #print("正在现在第{}张图片,它的地址是{}".format(hasdown+1,image_info['objurl']))
                        patterns=[re.compile('.jpg'),re.compile('.jpeg'),re.compile('.png')]
                        form=['.jpg','.jpeg','.png']
                        #暂定就这三种格式
                        typ=0
                        #匹配格式地标记,默认JPG.下暂不考虑性能问题，增加两个判断来提高图片存储正确性

                        if(patterns[1].search(image_info['objurl'])):
                            typ=1
                        if(patterns[2].search(image_info['objurl'])):
                            typ=2
                        
                        with open(self.downPath+'/'+str(hasdown+1)+form[typ],'wb') as f:
                            f.write(pic.content)

                        hasdown+=1
                    except Exception as err:
                        #非常有必要地一步
                        print(err,"出现该错误，我们只能跳过这个地址")
                        hasdown+=1
                        continue
                    
                    if(hasdown>=self.maxNum):
                        break

                    flag+=1

                flag=0
                page+=1
            '''
            for msg in data['browse_array']:
                image_info=msg['image_info']
                #只是得到url需要继续request发送请求
                pic=requests.get(image_info['objurl'],timeout=36)
                print("正在现在第{}张图片,它的地址是{}".format(hasdown+1,image_info['objurl']))
                with open(self.downPath+'/'+str(hasdown+1)+'.jpg','wb') as f:
                    f.write(pic.content)
                hasdown+=1
                if(hasdown>=self.maxNum):
                    break
            '''
        except Exception as err:
            print(err)
            print("本次查询因不可抗力终止，请输入其他关键词进行尝试")
            pass


if __name__ == "__main__":
    move=1
    while(move):
        searchName=input("请输入你想搜索的图片(源自百度图片)")
        serachNum=input("请输入你想得到的图片数量")
        aim=SearchDownload(searchName,int(serachNum),searchName)
        aim.doWork()
        info=input("***是否想继续查询(1/0)***")
        if(info != "1"):
            break
    print("欢迎下次使用本程序!")