import time
import threading
import face

class Sever(threading.Thread):
    def __init__(self, conn, addr, sql_conn):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.times = 0
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
                    self.Send("ERROR Please ENTER one of (stm32 camera） or exit to disconnect!")
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
                elif cmd[0]=='data1':
                    number = self.sql_conn.Get_rfid(cmd[1], come_in=1)
                    if number != 0:
                        self.conn.send("ok".encode('utf8'))
                    else:
                        self.Send("error")
                elif cmd[0]=='data2':
                    number = self.sql_conn.Get_rfid(cmd[1], come_out=1)
                    if number != 0:
                        self.conn.send("ok".encode('utf8'))
                    else:
                        self.Send("error")
                elif cmd[0] == 'hello':
                    self.Send('hello')
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
                state = self.sql_conn.camer_update(number=cmd[1], temp=cmd[2])
                if state != 0:
                    self.Send('ok')
                    time.sleep(4)
                else:
                    self.Send('error')
                    # # temp = cmd[1]
                    # while 1:
                    #     # path = self.Get_Img('Target/target.jpg', int(cmd[3]))
                    #     # id_number, confidence = face.predict('Target/target.jpg')
                    #     state = self.sql_conn.camer_update(number=cmd[1], temp=cmd[2])
                    #     if state != 0:
                    #         self.Send('ok')
                    #         times = self.Get_time()
                    #         time.sleep(4)
                    #         break
                    #     else:
                    #         self.Send('error')
            time.sleep(2)



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


