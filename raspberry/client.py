import socket
import os
import time
import cv2
import threading

filename = 'target.png'
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sk = socket.socket()
address = ('47.95.211.155', 40)
sk.connect(address)
while sk.read(1024) != 'Welecome Camera!':
    sk.send('camera'.encode('utf8'))
    time.sleep(1)



device_file ='/sys/bus/w1/devices/28-030597792a39/w1_slave'

def read_temp_raw():
    f = open(device_file,'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string)/1000.0
    return temp_c


def main():
    while 1:
        try:
            a = threading.Thread(target=Camer)
            a.start()

        except:
            print("Reboot")
            filename = 'target.png'
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            cap = cv2.VideoCapture(0)
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            threadlock = threading.Lock()

            sk = socket.socket()
            address = ('47.95.211.155', 40)
            sk.connect(address)
            while sk.read(1024) != 'Welecome Camera!':
                sk.send('camera'.encode('utf8'))
                time.sleep(1)


def Camer():
    while 1:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        while len(faces) != 1:
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            time.sleep(1)
            
        x, y, w, h = faces
        img = img[y:y+h, x:x+w]
        cv2.imwrite("target.png", img)
        #获取温度
        temps = read_temp()

        #上传图片和温度
        path = os.path.join(BASE_DIR, 'target.png')

        filename = os.path.basename(path)

        file_size = os.stat(path).st_size
        file_info = 'data|%s|%s' % (temps, file_size)  # split获取字符串的信息       以此方式打包，依次为   cmd/name/size
        sk.sendall(bytes(file_info, 'utf8'))  # 第一次发送请求，不是具体内容，而是先发送数据信息

        f = open(path, 'rb')
        has_sent = 0
        while has_sent != file_size:
            data = f.read(1024)
            sk.sendall(data)  # 发送真实数据
            has_sent += len(data)
        f.close()
        #接受返回数据
        str1 = sk.recv(1024)
        print(str1)
        print('上传成功')
        
    



    
'''
def Rfid():
    while 1:
        threadlock.acquire()
        count = ser.inWaiting()
        if count:
            recv = ser.read(count)
            file_info = "data1|%s"%(recv)
            sk.sendall(bytes(file_info, 'utf8'))
            s = sk.recv(1024)
            ser.write(s)
        time.sleep(1)
        threadlock.release()
'''


if __name__ == "__main__":
    try:
        main()
    except:
        print("Start ERROR!")
    pass

   


















