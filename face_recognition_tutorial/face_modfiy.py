# -*- coding:utf-8 -*-
import os
#图片的调用和读取
#需要配合python3.6,dlib附件可以通过附带的文件实现本地下载
#scikit-learn,pillow,face_recognition是必要的
import os.path
import sys
import csv
from sklearn.model_selection import train_test_split
import sklearn.neighbors
import pickle
from PIL import Image, ImageDraw, ImageFont
import face_recognition as fr
from face_recognition.face_detection_cli import image_files_in_folder
from sklearn.neural_network import MLPClassifier

def creat_image_dataset(pic_dir):
    #来进行图像数据集的处理
    #同时把图像中人脸的部分解析出来
    x = []
    y = []
    for class_dir in os.listdir(pic_dir):
        if not os.path.isdir(os.path.join(pic_dir, class_dir)):
            continue
        for img_path in image_files_in_folder(os.path.join(pic_dir, class_dir)):
            try:
                print("正在导入 " + img_path)
                image = fr.load_image_file(img_path)
                boxes = fr.face_locations(image)
                #把人脸的位置解决出来，存到矩形的方框中
                #忽略所有因素，包括背景。只用人脸的轮廓来进行训练
                x.append(fr.face_encodings(
                    image, known_face_locations=boxes)[0])#脸部追加
                y.append(class_dir)#名字追加
            except Exception:
                print("无法导入")
                continue
    return x, y


def train_model(x_train, y_train, model_path, max_iter):
    #数据集已经准备好,开始训练
    mlp = MLPClassifier(hidden_layer_sizes=[
                        100, 100], random_state=62, max_iter=max_iter)
    #将分类器参数设定好
    mlp.fit(x_train, y_train)
    with open(model_path, "wb") as f:
        pickle.dump(mlp, f)
        #把模型打包写入
    return mlp


def predict(img_path, model_path):
    #调用模型,参数分别为图片路径,参照模型路径
    mlp = None
    with open(model_path, "rb") as f:
        mlp = pickle.load(f)
    image = fr.load_image_file(img_path)
    boxes = fr.face_locations(image)
    faces = fr.face_encodings(image, known_face_locations=boxes)
    #调用pickle自己的预测predict函数，将该图的脸部与模型库中的内容进行比对
    return [(pred, loc) for pred, loc in zip(mlp.predict(faces), boxes)]


def show_name(img_path, predictions, key_dic):
    #一个绘图部分即把明星的名字写在已有图片上
    pil_image = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(pil_image)
    ttFont = ImageFont.truetype("simhei.ttf", 20)
    for name, (top, right, bottom, left) in predictions:
        draw.rectangle(((left, top), (right, bottom)), outline="#99cc33")
        name = key_dic[name]
        draw.rectangle(((left, bottom+22), (right, bottom)),
                       fill="#ffffff", outline="#99cc33")
        draw.text((left + 6, bottom+1), name, fill="#000000", font = ttFont)
    del draw
    pil_image.show()


def id2keyword(file_path):
    #人名匹配文件,返回对照字典
    csv_file_r = open(file_path, 'r', newline='', encoding="utf-8")
    csv_reader = csv.reader(csv_file_r, delimiter=',', quotechar='"')
    next(csv_reader)
    key_dic = {}
    for row in csv_reader:
        key_dic[row[0]]=row[1]
    return key_dic


if __name__ == '__main__':
    #这个模型可以输入的参数有
    #原始数据库
    #你需要对比的图片
    #建立数据库训练的模型或其存储名或有必要进行更新的模型名
    #原始资料与完整资料的字典匹配文件

    #第一个参数是数字，代表模式
    #1 最完全模式/ 输入样本集/ 模型地址/ 待检测数据/ 匹配字典/
    #2 训练模式/ 输入新样本/ 新模型地址/ 无输出结果/
    #3 验证模式/ 输入待检测数据/ 模型地址/ 匹配字典/
    print(sys.argv)
    if(len(sys.argv)>1):
        if(str(sys.argv[1])=='1'):
            faces_data,face_name=creat_image_dataset(sys.argv[2])
            x_train,x_test,y_train,y_test=train_test_split(
                faces_data,face_name,test_size=0.33,random_state=42
            )
            mlp=train_model(x_train,y_train,sys.argv[3],1000)
            print("该模型准确率为{:.2f}".format(mlp.score(x_test,y_test)))
            #先不管结果如何勒直接进行模拟
            train_model(faces_data,face_name,sys.argv[3],1000)
            #做出预测
            predctions=predict(sys.argv[4],sys.argv[3])
            #显示名字
            show_name(sys.argv[4],predctions,id2keyword(sys.argv[5]))
        elif(str(sys.argv[1])=='2'):
            faces_data,face_name=creat_image_dataset(sys.argv[2])
            x_train,x_test,y_train,y_test=train_test_split(
                faces_data,face_name,test_size=0.33,random_state=42
            )
            mlp=train_model(x_train,y_train,sys.argv[3],1000)
            print("该模型准确率为{:.2f}".format(mlp.score(x_test,y_test)))
            #先不管结果如何勒直接进行模拟
            train_model(faces_data,face_name,sys.argv[3],1000)
        else:
            predctions=predict(sys.argv[2],sys.argv[3])
            #显示名字
            print(sys.argv[2])
            show_name(str(sys.argv[2]),predctions,id2keyword(sys.argv[4]))
