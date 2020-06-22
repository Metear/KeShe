import os
import time
import threading


class Sever(threading.Thread):
    def __init__(self, conn, addr, sql_conn):
        # def __init__(self, conn, addr, log, sql_conn):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.sql_conn = sql_conn
        self.Send('Stanby...')
        self.start()

    def Send(self, str):
        self.conn.send(str.encode('utf8'))
        return 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        print('来自%s:%s连接关闭了.' % self.addr)

    def run(self):
        try:
            # 客户端身份选择！！！
            while 1:
                # client = conn
                data = self.conn.recv(1024)  # 缓冲区大小，接收文件的个数               第一次获取请求
                cmd = str(data, 'utf8').split('|')  # 第一次提取请求信息，获取  post name size
                if cmd[0] == 'android':
                    self.Send('Welcome Android!')
                    self.Android()
                    break
                # 上传stm32的测量和身份信息
                elif cmd[0] == 'stm32':
                    self.Send("Welcome stm32!")
                    self.Stm32()
                    break
                # 人脸识别摄像头数据
                elif cmd[0] == 'camera':
                    self.Send('Welecome Camera!')
                    self.Camera()
                    break
                elif cmd[0] == 'exit':
                    break
                else:
                    self.Send("ERROR Please ENTER one of (android、stm32、camera） or exit to disconnect!")
                time.sleep(2)
        finally:
            self.Send("Good by!")
            self.__exit__(0, 0, 0)


        #  登陆数据格式 login|name|password

    def login(self, cmd):
        if len(cmd) == 3:
            try:
                result = self.sql_conn.login(cmd[1], cmd[2])
                if result == 3:
                    self.Send('User ERROR!')
                elif result == 0:
                    self.Send('Password ERROR!')
                elif result == 1:
                    self.Send('login sucessful!')
                    self.Android_update()
            except:
                self.Send('ERROR Please register first!')
        else:
            self.Send("login ERROR,please ENTER like this:'login|user_number|password'")

    def Android(self):
        # 登录操作
        while True:
            data = self.conn.recv(1024)  # 缓冲区大小，接收文件的个数               第一次获取请求
            cmd = str(data, 'utf8').split('|')  # 第一次提取请求信息，获取  post name size
            # Android登陆操作
            if cmd[0] == 'login':
                # name,passwd来自数据库
                self.login(cmd)


            # 注册操作cmd = [    0         1         2         3         4        5           6
            #               'register', 'number', 'name', 'password', 'rfid', 'filename', 'filesize']
            elif cmd[0] == 'register':
                filename = cmd[1] + '.' + cmd[5].split('.')[1]
                self.Send("starting")
                cmd[5] = self.Get_Img(filename, int(cmd[6]))
                l = self.sql_conn.Android(list(cmd[1:6]))
                if l == 1:
                    self.conn.send("Add".encode('utf8'))
                    print('Add')
                elif l == 2:
                    self.conn.send("Haved".encode('utf8'))
                    print('Haved')
                else:
                    print('error')
            elif cmd[0] == 'exit':
                break
            else:
                pass
            time.sleep(2)

    # stm32数据上传格式
    # IP：49.95.211.155
    # 端口：40
    # 先发送:stm32
    # 在发送：rfid|temp
    # 收到：ok 表示数据插入正确
    # 收到：error 表示数据错误
    def Stm32(self):
        while True:
            try:
                data = self.conn.recv(1024)  # 缓冲区大小，接收文件的个数               第一次获取请求
                cmd = str(data, 'utf8').split('|')  # 第一次提取请求信息，获取  post name size
                if cmd[0] == 'exit':
                    break
                elif self.sql_conn.stm32_update(cmd[0], cmd[1]):
                    self.conn.send("ok".encode('utf8'))
                else:
                    self.conn.send('error'.encode('utf8'))
            except:
                self.Send("update: rfid|temp")
                pass
            finally:
                time.sleep(2)

    # 人脸识别摄像头部分
    def Camera(self):
        print('camera request')
        while True:
            data = self.conn.recv(1024)  # 缓冲区大小，接收文件的个数               第一次获取请求
            cmd = str(data, 'utf8').split('|')  # 第一次提取请求信息，获取  post name size
            time.sleep(2)

    # 数据格式 update|number|site|state|temp  update|2017213022|chengdu|good|36.5
    def Android_update(self):
        while 1:
            data = self.conn.recv(1024)  # 缓冲区大小，接收文件的个数               第一次获取请求
            cmd = str(data, 'utf8').split('|')  # 第一次提取请求信息，获取  post name size
            if cmd[0] == 'update':
                cmd[0] = self.Get_time()
                if self.sql_conn.Android_update(cmd):
                    self.conn.send('ok'.encode('utf8'))
                    break
                else:
                    self.conn.send('error'.encode('utf8'))
            elif cmd[0] == 'exit':
                break
            else:
                self.conn.send('error'.encode('utf8'))

    def Get_Img(self, filename, filesize):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 26:11,当前目录
        path = os.path.join(BASE_DIR, 'Picture', filename)
        size = 0
        with open(path, 'ab') as f:
            while size != filesize:
                data = self.conn.recv(1024)
                f.write(data)
                size += len(data)
        self.Send('保存图片成功')
        return path

    def Get_time(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
