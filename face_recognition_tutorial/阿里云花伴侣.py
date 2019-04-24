import requests
import json
import base64
import sys

#图片是个四纬物体。
base64_data = None

#print(sys.argv)
#经过修改，使得源程序从写死到灵活，可以在命令行中输入参数即可
if(len(sys.argv)>1):
    with open(sys.argv[1],"rb") as f:
    #把读取的图片进行编码,
        base64_data = base64.b64encode(f.read())
        
    host = 'http://plant.market.alicloudapi.com/plant/recognize'
    appcode = '586ed0a7d7e046db8c0e314234b081c5'
    #post的主体就是一个字典
    bodys = {'img_base64': base64_data}
    headers = {'Authorization': 'APPCODE ' + appcode,'Content-Type': 'application/x- www-form-urlencoded; charset=UTF-8'}
    response = requests.post(host, data = bodys, headers = headers)
    content = response.text
    if (content):
        data_reader = json.loads(content)['Result']
        for i in range(len(data_reader)):
            name = data_reader[i]['Name']
            score = data_reader[i]['Score']
            print(name,score)
