import socket
import os
import time
sk = socket.socket()


address = ('localhost', 8800)
sk.connect(address)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


file_info = 'android'
sk.sendall(bytes(file_info, 'utf8'))
print(str(sk.recv(1024), 'utf8'))
time.sleep(2)
file_info = 'android'
sk.sendall(bytes(file_info, 'utf8'))
print(str(sk.recv(1024), 'utf8'))

while True:
    cmd = input('>>>>>>>>')
    print('get cmd')
    if cmd == "lo":
        file_info = 'login|2017213023|3023'
        sk.sendall(bytes(file_info, 'utf8'))
        s = str(sk.recv(1024), 'utf8')
        if s == 'login sucessful!':
            file_info = 'update|2017213022|chongqing|good|36'
            sk.sendall(bytes(file_info, 'utf8'))
        print("update ok")


    if cmd == "zc":
        path = os.path.join(BASE_DIR, '2017213023.jpg')

        filename = os.path.basename(path)

        file_size = os.stat(path).st_size
        print(file_size)
        file_info = 'register|2017213023|wangxiaokang|3023|16CAABA0|%s|%s' % (
        filename, file_size)  # split获取字符串的信息       以此方式打包，依次为   cmd/name/size
        sk.sendall(bytes(file_info, 'utf8'))  # 第一次发送请求，不是具体内容，而是先发送数据信息
        time.sleep(2)
        print("开始传图片")
        f = open(path, 'rb')
        has_sent = 0
        while has_sent != file_size:
            data = f.read(1024)
            sk.sendall(data)  # 发送真实数据
            has_sent += len(data)
        f.close()
        print('上传成功')
    print(str(sk.recv(1024), 'utf8'))

