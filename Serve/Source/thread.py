import os
import time
import threading
import training
import face

class Sever(threading.Thread):
    def __init__(self, conn, addr, sql_conn):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.sql_conn = sql_conn
        self.start()


    def run(self):
        # 客户端身份选择！！！
        self.Send('Stanby...')
        print("All Ready!")
        while 1:
            try:
                data = self.conn.recv(30)
                cmd = str(data, 'utf8').split('|')
                # if cmd[0] == 'android':
                #     self.Android()
                # 上传stm32的测量和身份信息
                if cmd[0] == 'stm32':
                    self.Send("Welcome stm32!")
                    self.Stm32()
                    break
                # 人脸识别摄像头数据
                # cmd = [start|rfid|temp|filename|filesize]
                elif cmd[0] == 'camera':
                    self.Send('Welecome Camera!')
                    self.Camera()
                    break
                elif cmd[0] == 'exit':
                    break
                else:
                    self.Send("ERROR Please ENTER one of (android camera） or exit to disconnect!")
                time.sleep(2)
            except:
               break
        try:
            self.Send("Good by!")
            self.conn.close()
        except:
            print("异常退出线程")
        else:
            print('正常关闭该线程')
        finally:
            print("退出")


    # Android操作主函数
    def Android(self):
        self.Send('Welcome Android!')
        while True:
            data = self.conn.recv(1024)  # 缓冲区大小，接收文件的个数               第一次获取请求
            cmd = str(data, 'utf8').split('|')  # 第一次提取请求信息，获取  post name size
            # Android登陆操作
            print("android starting")
            if cmd[0] == 'login':
                # name,passwd来自数据库
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
            # 注册操作cmd = [    0         1         2         3         4        5           6
            #               'register', 'number', 'name', 'password', 'rfid', 'filename', 'filesize']
            elif cmd[0] == 'register':
                filename = cmd[1] + '.' + cmd[5].split('.')[1]
                self.Send("starting")
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 26:11,当前目录
                path = os.path.join(BASE_DIR, 'Picture', filename)
                cmd[5] = self.Get_Img(path, int(cmd[6]))
                print("图片传输完成")
                l = self.sql_conn.Android(list(cmd[1:6]))
                if l == 1:
                    self.conn.send("Add".encode('utf8'))
                    training.getImageAndLabels('Picture')
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
    # 在发送：data|temp
    # 收到：ok 表示数据插入正确
    # 收到：error 表示数据错误
    def Stm32(self):
        while True:
            try:
                data = self.conn.recv(1024)  # 缓冲区大小，接收文件的个数               第一次获取请求
                cmd = str(data, 'utf8').split('|')  # 第一次提取请求信息，获取  post name size
                if cmd[0] == 'exit':
                    break
                elif cmd[0]=='data':
                    number = self.sql_conn.Get_rfid(cmd[1])
                    if number != 0:
                        self.conn.send("ok".encode('utf8'))
                    else:
                        self.Send("error")
            except:
                self.Send("error")
            finally:
                time.sleep(2)


    # 人脸识别摄像头部分
    def Camera(self):
        print('camera request')
        while True:
            data = self.conn.recv(1024)
            cmd = str(data, 'utf8').split('|')
            if cmd[0] == 'exit':
                break
            elif cmd[0] == 'data':
                    temp = cmd[1]
                    while 1:
                        path = self.Get_Img("Target/target.png", int(cmd[3]))
                        id_number, confidence = face.predict(path)
                        if confidence > 0.7:
                            self.Send('ok')
                            state = self.sql_conn.stm32_update(number=id_number, temp=temp)
                            time.sleep(4)
                            break
                        else:
                            self.Send('error')
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

    def Get_Img(self, path, filesize):
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

    def Send(self, str):
        self.conn.send(str.encode('utf8'))
        return 1


