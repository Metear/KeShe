import numpy as np
import cv2
import time
import socket


net = 0

if net:
    sk = socket.socket()
    address = ('47.95.211.155', 40)
    sk.connect(address)
    while sk.read(1024) != 'Welecome Camera!':
        sk.send('camera'.encode('utf8'))
        time.sleep(1)
    
    # device_file ='/sys/bus/w1/devices/28-030597792a39/w1_slave' # 加载ds18b20固件

cap = cv2.VideoCapture(0)        #'0'选择笔记本电脑自带参数，‘1’为USB外置摄像头
print(cap.get(3), cap.get(4))    #查看当前捕获视频的尺寸，默认为640*480
cap.set(propId=3, value=320)     #设置你想捕获的视频的宽度
cap.set(propId=4, value=240)     #设置你想捕获的视频的高度
print(cap.get(3), cap.get(4))    #验证是否设置成功



#加载训练数据集文件
recogizer=cv2.face.LBPHFaceRecognizer_create()
recogizer.read('trainer.yml')
face_detector = cv2.CascadeClassifier(
    'haarcascade_frontalface_default.xml')

id=0  # 现在的学号
id_old=1  #上一次正确的学号
confidence =0  # 人脸识别置信度变量
data ='ok' # 服务器返回数据
temps=0  # ds18b20温度


while (True):
    ret, img = cap.read()      #读取图像并显示
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray)
    for x,y,w,h in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        id, confidence=recogizer.predict(gray[y:y+h,x:x+w])
    print('标签id:',id,'置信评分：',confidence)

    if confidence<50:
        if net:
            temps = 37
            #temps = read_temp()  # 获取ds18b20温度

            file_info = 'data|%s|%s' % (id, temps)  # split获取字符串的信息       以此方式打包，依次为   cmd/name/size
            sk.sendall(bytes(file_info, 'utf8'))  # 第一次发送请求，不是具体内容，而是先发送数据信息
            time.sleep(0.5)
            data = str(sk.recv(1024), 'utf8')
            if data == 'ok':
                id_old = id
        text = "id:" + str(id)+data
    else:
        text = 'Cannot Be Identified!'

    cv2.putText(img, text, (30, 30), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
    cv2.imshow('result',img)
    id = 0
    confidence=0
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()                    #按‘q’键退出后，释放摄像头资源
cv2.destroyAllWindows()




# def read_temp_raw():
#     f = open(device_file,'r')
#     lines = f.readlines()
#     f.close()
#     return lines

# def read_temp():
#     lines = read_temp_raw()
#     while lines[0].strip()[-3:] != 'YES':
#         time.sleep(0.2)
#         lines = read_temp_raw()
#     equals_pos = lines[1].find('t=')
#     if equals_pos != -1:
#         temp_string = lines[1][equals_pos+2:]
#         temp_c = float(temp_string)/1000.0
#     return temp_c
