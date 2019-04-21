import json
import os
import requests
import re
import random

#作业从专业网站爬图片/从百度网站爬图片
#chris 4/21 仅供学习参考
class TryDownload:
    def __init__(self,download_file,key_word,download_max):
        self.download_num=0#当前下载数量
        self.download_max=download_max#目标下载数量
        self.key_word=key_word
        self.download_path='./download/cfh/' + str(download_file)
    
    def do_download(self):
        url1='http://www.cfh.ac.cn/ajaxserver/speciesserv.ashx?action=spsearchzh&keyword='+ self.key_word
        header={
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) '
                                'Gecko/20100101 Firefox/66.0',
            'Host':'www.cfh.ac.cn',
            'Cookie': 'Hm_lvt_17100a428da6da3b4e5da32712ca72c3=1555421469; '
                            'Hm_lpvt_17100a428da6da3b4e5da32712ca72c3=1555421566; '
                            'CFH_Cookie=sk3fvuvpywqj41uwnncntajr',},
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
        {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'},
        {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
        {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
        }

        raw_data=requests.get(url1,headers=random.choice(header))
        #print(raw_data.text)
        #已经得到获取ID的API网址
        json_data=json.loads(raw_data.text)
        #print(json_data)
        if(len(json_data))>0:
            key_id=json_data[0]['ID']
            url2="http://www.cfh.ac.cn/AjaxServer/Server.ashx?service=photoset&method=get&spid="+str(key_id)+"&pagesize="+str(self.download_max)+"&page=1"
            list2=requests.get(url2,headers=header)
            
            data=json.loads(list2.text)['photolist']
            #已经可以得到所有照片的地址，接下来就是存储工作
            self.download_num=0
            if not  os.path.exists(self.download_path):
                os.makedirs(self.download_path)
            while self.download_num<self.download_max:
                img_url='http://www.cfh.ac.cn'+ \
                        str(data[self.download_num]['thumbnail']).replace('Thumbnail','Normal')
                print('正在下载第 '+str(self.download_num+1)+' 张图片,图片地址为 '+str(img_url))

                try:
                    pic=requests.get(img_url,timeout=10*random.randint(1,10))

                    pic_name=self.download_path+'/'+str(self.download_num+1)+'.jpg'

                    with open(pic_name,'wb') as f:
                        f.write(pic.content)
                    self.download_num+=1

                    if(self.download_num >= self.download_max):
                        break
                except Exception as err:
                    self.download_num+=1 
                    print(err)
                    continue
            print("下载完成")




if __name__== '__main__':
    import csv
    #读取与本文件位于相同目录下的namelist.csv文件并根据需求进行爬取
    name=open('namelist.csv','r')
    rawd=csv.reader(name)
    for row in rawd:
        print(row)
        test=TryDownload(row[0],row[1],float(row[2]))
        test.do_download()


#test=TryDownload("十大功劳","十大功劳",100)
#test.do_download()
