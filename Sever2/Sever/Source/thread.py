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
                if cmd[0] == 'android':
                    self.Android()
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


    # Android操作主函数
    def Android(self):
        self.Send('Welcome Android!')
        while True:
            data = self.conn.recv(1024)  # 缓冲区大小，接收文件的个数               第一次获取请求
            cmd = str(data, 'utf8').split('|')  # 第一次提取请求信息，获取  post name size
            # Android登陆操作
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
                path = os.path.join(BASE_DIR, '../Picture', filename)
                path = self.Get_Img(path, int(cmd[6]))  #获取并保存图片


                cmd[5] = self.Get_Img(filename, int(cmd[6]))
                l = self.sql_conn.Android(list(cmd[1:6]))
                if l == 1:
                    self.conn.send("Add".encode('utf8'))
                    training.getImageAndLabels('../Picture')
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

    # 人脸识别摄像头部分
    def Camera(self):
        print('camera request')
        while True:
            data = self.conn.recv(1024)
            cmd = str(data, 'utf8').split('|')
            if cmd[0] == 'exit':
                break
            elif cmd[0] == 'data':
                if (len(cmd)) > 2:
                    temp = cmd[1]
                    while 1:
                        path = self.Get_Img("../Target/target.png", int(cmd[3]))
                        id_number, confidence = face.predict(path)
                        if confidence > 0.8:
                            self.Send('ok')
                            time.sleep(4)
                            break
                        else:
                            self.Send('error')
                    state = self.sql_conn.stm32_update(number=id_number, temp=temp)
                else:
                    result = self.sql_conn.Get_rfid(cmd[1])
                    if result:
                        self.Send("pass")
                    else:
                        self.Send("error")
                '''
                if state == 1:
                    self.conn.send("ok".encode('utf8'))
                elif state == 2:
                    self.Send('Warning!')
                elif state == 3:
                    self.Send('rfid error')
                    self.conn.send('error'.encode('utf8'))
                '''
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
        # BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 26:11,当前目录
        # path = os.path.join(BASE_DIR, 'Picture', filename)
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


