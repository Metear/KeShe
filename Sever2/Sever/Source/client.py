import socket
import os
import time
sk = socket.socket()
print(sk)

address = ('47.95.211.155', 40)
sk.connect(address)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

'''
while True:
    s = 'register|2017213022|zhangfeng|zf79|jdhs123|hero.png|128'
    sk.send('android'.encode('utf8'))
    inp = input('>>>>>>>>')
    if inp == 'exit':
        break
    fi = "hero.png"
    sk.send('android'.encode('utf8'))
    s1 = 'register|2017213022|zhangfeng|zf79|jdhs123|'+fi+'|'
    with open(fi,'rb') as f:
        l = f.__sizeof__()
        sl = s1+str(l)
        print(s1)
        sk.sendall(bytes(s1, 'utf8'))

        print('发送数据成功，开始传图片')
        size = 0
        while size != l:
            data = f.read(1024)
            sk.sendall(data)
            size += len(data)
        print("Send ok!!")

sk.send('exit'.encode('utf8'))
sk.close()
'''



while True:
    inp = int(input('>>>>>>>>'))  # post|11.png
    #s1 = 'register|2017213022|zhangfeng|zf79|jdhs123|hero.png|'
    # s = 'post|hero.png'
    # cmd, path = s.split('|')  # 拿到post，以及文件11.jpg
    print('get cmd')
    if inp is 1:
        print('zhuche')
        file_info ='android'
        sk.sendall(bytes(file_info, 'utf8'))  # 第一次发送请求，不是具体内容，而是先发送数据信息
    else:
        print('post')
        path = os.path.join(BASE_DIR, 'hero.png')

        filename = os.path.basename(path)

        file_size = os.stat(path).st_size
        print(file_size)
        file_info = 'register|2017213029|hongwen|3022|201721|%s|%s' % (filename, file_size)  # split获取字符串的信息       以此方式打包，依次为   cmd/name/size
        sk.sendall(bytes(file_info, 'utf8'))  # 第一次发送请求，不是具体内容，而是先发送数据信息

        f = open(path, 'rb')
        has_sent = 0
        while has_sent != file_size:
            data = f.read(1024)
            sk.sendall(data)  # 发送真实数据
            has_sent += len(data)

        f.close()
        print('上传成功')

