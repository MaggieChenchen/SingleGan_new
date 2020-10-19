import cv2
import numpy as np
import os
import shutil

##获得一张图片的文字框信息，左上角和右下角 并写入文件中
def get_condition(img,path,title):
    #img 图片 path :txt文件的路径+名字 title:这一行的标注名
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    binary = 255-binary
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # x0,y0 左上角 x1,y1右下角 chushihua
    x0,y0,x1,y1 = 255,255,0,0
    for c in contours:
        ##不断比较，得到框的边界
        x, y, w, h = cv2.boundingRect(c)
        x0 = min(x,x0)
        y0 = min(y,y0)
        x1 = max(x1,x+w)
        y1 = max(y1,y+h)
    ##enlarge box
    x0=int(x0-5)
    y0=int(y0-5)
    x1=int(x1+5)
    y1=int(y1+5)

    # draw box
    #h=cv2.rectangle(img, (x0,y0),(x1,y1), (0, 0, 255), 2)
    #cv2.imshow('h',h)
    #cv2.waitKey(10000)
    condition = title+' ' +str(x0)+' '+str(y0)+ ' '+str(x1)+" "+str(y1)+" "+"\n"
    print(condition)
    with open(path, 'a') as f:  # 'a'表示append,即在原来文件内容后继续写数据（不清楚原有数据）
        f.write(condition)
    f.close()


#根据文件和坐标，将图片进行裁剪，保存
def cut_img(img,condition,save_path):
    if condition[0]<0:
        condition[0]=0
    if condition[1]<0:
        condition[1]=0
    crop = img[condition[1]:condition[3],condition[0]:condition[2]]  #y0:y1, x0:x1
    print(condition)
    cv2.imwrite(save_path,crop)


#读取txt文件的每一行，并对每一行用空格进行分开，再根据每一行,对图片进行裁剪,保存到对应字母的文件夹下
def read_image(img_path,img_path_new,txt_path):

    aa = []
    with open(txt_path, "r") as f:
        for line in f.readlines():
            data = line.split('\n\t')
            for str in data:
                sub_str = str.split(' ')
            if sub_str:
                aa.append(sub_str)
    #print(aa)
    for j in range(9500): #txt文件中的数据行数
        condition=[]
        for i in range(4):
            condition.append(int(aa[j][i+1]))
        #save_path='/home/cpy/PycharmProjects/SingleGAN-master/image_new/'+'a'+'/'+'a1'+'.jpg'
        img = cv2.imread(img_path+aa[j][0]+'.jpg')
        cut_img(img,condition,save_path = img_path_new+aa[j][0][0]+'/'+aa[j][0]+'.jpg')




#新建 a-z文件夹
def file():
    for i in range(25):
        os.mkdir(img_path_new+chr(97+i))


 #对文件夹中包含‘0to1’的文件进行改名，把文字位置保存下来，把不包含0to1的文件删除
 #注意 os.listdir()返回的文件名不一定是顺序的，可能是随机的
def process_img(img_path,txt_path):
     for i in os.listdir(img_path):
        if '0to1' in i:
            img = cv2.imread(img_path+i)
            get_condition(img,txt_path,i[0:-13])
            os.rename(img_path+i,img_path+i[0:-13]+'.jpg')
        else:
            os.remove(img_path+i)


############ config path
img_path = '/root/workspace/SingleGan_new/results/test/images/'  #need clear
txt_path = '/root/workspace/SingleGan_new/condition.txt' # need clear
img_path_new = '/root/workspace/SingleGan_new/image_train5/'   #need update to new file folder


file()
process_img(img_path,txt_path)
read_image(img_path,img_path_new,txt_path)

