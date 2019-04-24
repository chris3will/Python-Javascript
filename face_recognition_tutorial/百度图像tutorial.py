'''
生物分类tutorial
这两个码自己可以到官网上免费申请得到500次的使用机会~
16100***
A_K
dUPNwHqGMcXHAXGct6i*****
S_K
F3rVGrhD9eoTHQ4TmxkXNfgZKGv*****
https://cloud.baidu.com/doc/IMAGERECOGNITION/ImageClassify-API.html#.E8.AF.B7.E6.B1.82.E8.AF.B4.E6.98.8E
一个有用的平台
http://ai.baidu.com/easydl/app/1/datasets/new

2019/4/24
'''
import re
import sys
import requests
import json
import base64
api_key='dUPNwHqGMcXHAXGct6i*****'
secret_key='F3rVGrhD9eoTHQ4TmxkXNfgZKGv*****'
base64_data=None

#step0;处理你需要的图片
if(len(sys.argv)>1):
    with open(sys.argv[1],'rb') as f:
        base64_data=base64.b64encode(f.read())
#print(base64_data)
#step1
#先获取百度要求的token;必要步骤
host='https://aip.baidubce.com/oauth/2.0/token?'
fullhost=host+'grant_type=client_credentials'+'&client_id='+api_key+'&client_secret='+secret_key
#print(fullhost)
header={'Content-Type':'application/json; charset=UTF-8'}
response=requests.get(fullhost,headers=header)
#print(response.content)
json_res=json.loads(response.content)
#print(json_res)
access_token=""
for i in json_res:
    if i=="access_token":
        access_token=json_res[i]
print(access_token)#已经得到需要的token

#step2
#已经获取应得权限
host1='https://aip.baidubce.com/rest/2.0/image-classify/v1/animal?access_token='+str(access_token)
headers={'Content-Type':'application/x-www-form-urlencoded'}
bodys={'image':base64_data}
raw=requests.post(host1,data=bodys,headers=headers)
raw=raw.text
if(raw):
    print(raw)

