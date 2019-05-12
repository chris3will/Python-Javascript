#coding:utf-8
import tkinter
import tkinter.filedialog
import tkinter.messagebox
from PIL import ImageTk,Image
import requests
import re
import json
import os
import random
from PIL import Image, ImageDraw, ImageFont
import csv
import face_modfiy as fm
import searchBaidu as sb
#2019/5/12:chris
#查询功能，利用百度图片API得到用户需要的图片
#对比功能，将用户需要的图片与本地已经选取并训练好的模型进行比照
#获取更多，直接让用户调用searchBaidu的功能
#打开图片，就是打开用户自己不知道名字的图片

headers=[
    {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;'},
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'}
]

path="Paul.jpeg"

class FindPeson(object):
    def client_exit(self):
        exit()
    def __init__(self):
        #对比要信息初始化
        # 创建主窗口,用于容纳其它组件
        self.root = tkinter.Tk()
        # 给主窗口设置标题内容
        self.root.title("图鉴xPython3.6")
        self.root.geometry('640x640')
        self.root.resizable(width=False, height=False)

        self.imgPath=None
        self.img=None
        self.downPath=None
        #菜单的设置
        menu=tkinter.Menu(self.root)
        self.root.config(menu=menu)
        do=tkinter.Menu(menu)
        do.add_command(label='showPic',command=self.showPic)
        do.add_command(label='showText',command=self.showText)
        do.add_command(label='openPic',command=self.openPic)
        menu.add_cascade(label='do',menu=do)
        undo=tkinter.Menu(menu)
        undo.add_command(label='desPic',command=self.desPic)
        menu.add_cascade(label='undo',menu=undo)
        self.hello=tkinter.Label(self.root,text="欢迎使用这个小工具,您可以在下方输入框中搜索NBA球星 ---chris")

        # 创建一个输入框,并设置尺寸
        self.ip_input = tkinter.Entry(self.root,width=10)
        self.display_info = tkinter.Message(self.root,width=235)

        self.ask=tkinter.Label(self.root,text="请输入你想批量下载的图片",width=20)
        self.ask_1=tkinter.Entry(self.root,width=10)
        self.nums=tkinter.Label(self.root,text="请输入你想下载的数量",width=20)
        self.nums_1=tkinter.Entry(self.root,width=10)
        self.confirm=tkinter.Button(self.root,command=self.confirmMore,text="确认搜索",width=10)

        # 创建一个查询结果的按钮
        self.result_button = tkinter.Button(self.root, command = self.find_person, text = "查询",width=10)
        self.compare_button = tkinter.Button(self.root, command = self.comparePic, text = "比对",width=10)
        self.more_button = tkinter.Button(self.root, command = self.morePic, text = "获取更多",width=10)
        self.msgbox=tkinter.Message(self.root)
        self.msgbox.config(width=200)

    # 完成布局
    def gui_arrang(self):
        self.hello.pack(side=tkinter.TOP)
        self.ip_input.pack()
        self.result_button.pack()
        self.compare_button.pack()
        self.more_button.pack()
        self.msgbox.pack()
        
    def resize(self,w, h, w_box, h_box, pil_image):  
        ''' 
        https://blog.csdn.net/sinat_27382047/article/details/80138733
        从这里学到的
        resize a pil_image object so it will fit into 
        a box of size w_box times h_box, but retain aspect ratio 
        对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例 
        '''  
        f1 = 1.0*w_box/w # 1.0 forces float division in Python2  
        f2 = 1.0*h_box/h  
        factor = min([f1, f2])  
        #print(f1, f2, factor) # test  
        # use best down-sizing filter  
        width = int(w*factor)  
        height = int(h*factor)  
        return pil_image.resize((width, height), Image.ANTIALIAS)  


    def showPic(self,path='Paul.jpeg'):
        self.forgetMore()
        self.desPic()
        load=Image.open(path)
        w,h=load.size
        w_box=480
        h_box=320
        load=self.resize(w,h,w_box,h_box,load)
        #注意，在后台比对的时候变成小像素以进行加速
        render=ImageTk.PhotoImage(load)
        self.root.img=tkinter.Label(self.root,image=render)
        self.root.img.image=render
        #self.display_info.insert(0,self.root.img)
        self.root.img.pack(side=tkinter.TOP,fill='both')
        self.msgbox.pack(side=tkinter.TOP) 
        #默认直接进行比对 

    def showText(self):
        #计划用这个函数显示每一步的操作;但实际上好些挺鸡肋
        self.forgetMore()
        text=tkinter.Label(self.root,text='This is why we play!')
        text.pack()
        
    def desPic(self):
        #清空图片
        try:
            self.forgetMore()
            self.root.img.destroy()
            self.msgbox.config(text='')
        except:
            pass

    def find_person(self):
        # 获取输入信息
        self.forgetMore()
        self.ip_addr = self.ip_input.get()
        self.ip_addr=self.ip_addr.strip()
        if(self.ip_addr!=''):
            self.downPath='./find/'+str(self.ip_addr)
            got=0
            hasdown=0
            #aim = self.gi.record_by_name(self.ip_addr)
            # 为了避免非法值,导致程序崩溃,有兴趣可以用正则写一下具体的规则,我为了便于新手理解,减少代码量,就直接粗放的过滤了
            app=["","人物","人像","人脸"]
            page=random.randint(0,1)
            url="https://m.baidu.com/sf/vsearch/image/browse/wiseresultjson?&word="+ \
                    str(self.ip_addr)+random.choice(app)+"&rn=30&pn="+str(page*30)+"&browse_style=1"
                #链接中的” 人脸“纯粹是为了让结果更合理
            try:
                rawdata=requests.get(url,headers=random.choice(headers))
                data=json.loads(rawdata.text)
                msg=data['browse_array']
                image_info=[]
                for i in msg:
                    image_info.append(i['image_info']) 
                #print(image_info)

                if not os.path.exists(self.downPath):
                    os.makedirs(self.downPath)

                while(got==0):
                    try:
                        #现在可以解决遇到png或者目标图片源地址拒绝爬虫访问请求时跳过即可
                        #下一步想增加几个选择来匹配原图的格式，使得PNG也可以正常保存，问题在于如果每张图片都要匹配具体的图片类型，会增加程序运行时间
                        #所以实际上爬取过程结束后仍然会有无效图片存在
                        choc=random.randint(0,30)
                        pic=requests.get(image_info[choc]['objurl'],timeout=2*random.randint(1,5))
                        #print("它的地址是{}".format(image_info[choc]['objurl']))
                        patterns=[re.compile('.jpg'),re.compile('.jpeg'),re.compile('.png')]
                        form=['.jpg','.jpeg','.png']
                        #暂定就这三种格式
                        typ=0
                        #匹配格式地标记,默认JPG.下暂不考虑性能问题，增加两个判断来提高图片存储正确性
                        if(patterns[1].search(image_info[choc]['objurl'])):
                            typ=1
                        if(patterns[2].search(image_info[choc]['objurl'])):
                            typ=2
                        with open(self.downPath+'/'+str(choc)+form[typ],'wb') as f:
                            f.write(pic.content)
                        self.imgPath=self.downPath+'/'+str(choc)+form[typ]
                        # 为回显列表赋值
                        '''
                        for item in msg:
                            self.display_info.insert(0,item)
                        '''
                        self.showPic(self.downPath+'/'+str(choc)+form[typ])
                        
                        got+=1
                        hasdown+=1
                        tmp=str(image_info[choc]['title'])
                        dr=re.compile(r'<[^>]+>',re.S)
                        res=dr.sub('',tmp)
                        self.msgbox.config(text=res)
                    except Exception as err:
                        #非常有必要地一步
                        self.imgPath=None
                        print(err,"出现该错误，我们只能跳过这个地址")
                        hasdown+=1
                        continue
            except Exception as err:
                print(err,'出现错误,查询失败')

        else:
            tkinter.messagebox.showerror('警告','请输入你要查询的人物名')
        return self.display_info

    def id2keyword(self,file_path):
        try:
            csv_file_r = open(file_path, 'r', newline='', encoding="utf-8")
            csv_reader = csv.reader(csv_file_r, delimiter=',', quotechar='"')
            next(csv_reader)
            key_dic = {}
            
        except Exception as err:
            print(err,"1")
            pass
        
        try:
            for row in csv_reader:
                #print(row)
                key_dic[row[0]]=row[1]
        except Exception as err:
            print(err,"2")
        #print(key_dic,"id2的展示")
        return key_dic

    def show_name(self,img_path, predictions, key_dic):
        #一个绘图部分即把明星的名字写在已有图片上
        pil_image = Image.open(img_path).convert("RGB")
        draw = ImageDraw.Draw(pil_image)
        ttFont = ImageFont.truetype("simhei.ttf", 15)
        for name, (top, right, bottom, left) in predictions:
            draw.rectangle(((left, top), (right, bottom)), outline="#F08080")
            #print(key_dic,"show_name中")
            try:
                #目前还没时间明白这其中画图的规范和原理，可能会超出空格，目前暂以搁置处理
                name = key_dic[name]
                #print(len(name))
                draw.rectangle(((left, bottom+19), (right, bottom)),
                            fill="#ffffff", outline="#00BFFF")
                draw.text((left + 5, bottom+1), name, fill="#000000", font = ttFont)
            except Exception as err:
                print(err,"show中的问题")

        del draw
        pil_image.show()

    def comparePic(self,path='Paul.jpeg'):
        if(path=='Paul.jpeg' and self.imgPath==None):
            tkinter.messagebox.showinfo('提示',"请找到您需要对比的图片后再执行本操作")
        else:
            tkinter.messagebox.showwarning('友情提醒',"对比结果仍存在误差,仅供参考")
        try:
            if(self.imgPath!=None):
                path=self.imgPath
            try:
                predictions=fm.predict(path,'./models/player_model.mlp')  
                try:
                    self.show_name(path,predictions,self.id2keyword("./info.csv"))

                except Exception as err:
                    print("展示出错",err)
                    pass
            except Exception as err:
                print("预测出错",err)
                tkinter.messagebox.showerror('Hi!','该图片因自身格式问题无法比对，请更换图片再次尝试')
                pass

        except Exception as err:
            print(err)
            tkinter.messagebox.showerror('Hi!','该图片因自身格式问题无法比对，请更换图片再次尝试')
            pass
    
    def morePic(self):
        #调用百度查询对用户喜欢的东西扩展下载 
        self.ask.pack(side=tkinter.LEFT) 
        self.ask_1.pack(side=tkinter.LEFT)       
        self.nums.pack(side=tkinter.LEFT)
        self.nums_1.pack(side=tkinter.LEFT)
        self.confirm.pack(side=tkinter.LEFT)

    def confirmMore(self):
        if(self.ask_1.get() and self.nums_1.get()):
            self.msgbox.configure(text="***下载中***")
            self.msgbox.pack()
            aim=sb.SearchDownload(self.ask_1.get(),int(str(self.nums_1.get())),self.ask_1.get())
            aim.doWork()
            self.msgbox.configure(text="****下载完成****")
            self.msgbox.pack()
            print("下载完成")
            self.forgetMore()
        else:
            tkinter.messagebox.showwarning("警告","请在输入正确的参数后重新执行本操作")
            self.forgetMore()
    
    def forgetMore(self):
        #避免查询操作影响到其他布局
        self.ask_1.delete(0,'end')
        self.nums_1.delete(0,'end')
        self.ask.forget()
        self.ask_1.forget()
        self.nums.forget()
        self.nums_1.forget()
        self.confirm.forget()

    def openPic(self):
        filename=tkinter.filedialog.askopenfile()
        if(filename!=''):
            self.msgbox.config(text="您选择的文件是: "+str(filename.name)+"; 并且我们默认为您执行人脸比对操作!")
            self.imgPath=filename.name
            self.showPic(filename.name)
            self.comparePic(filename.name)
        else:
            self.msgbox.config("您没有选择任何文件")

def main():
    # 初始化对象
    FL = FindPeson()
    # 进行布局
    FL.gui_arrang()
    # 主程序执行
    tkinter.mainloop()
    pass


if __name__ == "__main__":
    main()

