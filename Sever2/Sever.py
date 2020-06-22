import db
import socket
import thread
import pymysql
from DBUtils.PooledDB import PooledDB


sk = socket.socket()
address = ('172.25.51.65', 40)
sk.bind(address)  # 将本地地址与一个socket绑定在一起
sk.listen(10)  # 最多允许有3个客户称呼
pool = PooledDB(pymysql, 20, host="47.95.211.155", port=3306, db="TESTDB", user='zf', passwd='zf2279', charset='utf8')

try:
    print('waiting........ ')
    while 1:
        conn, addr = sk.accept()
        sql_conn = db.DB(pool.connection())  # 创建数据库线程池连接
        t = thread.Sever(conn, addr, sql_conn)  # 创建新线程来处理TCP连接
except:
    print("启动线程错误!!!")

finally:
    print("ALL shoutdown!!")


'''
def ALL():
    with open(path, 'wb') as log:
        with DB(db='TESTDB') as db:
            try:
                while 1:
                    conn, addr = sk.accept()
                    t = Sever(conn, addr, db, log) # 创建新线程来处理TCP连接
            except:
                print("启动线程错误!!!")




BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 26:11,当前目录
if len(cmd) > 3:
    print(cmd)

else:
    # filesize = os.stat(data)
    path = os.path.join(BASE_DIR, 'MNIST_80', cmd[1])
    print(path)
    filesize = int(cmd[2])

    f = open(path, 'ab')
    has_receive = 0
    while has_receive != filesize:
        data = conn.recv(1024)  # 第二次获取请求，这次获取的就是传递的具体内容了，1024为文件发送的单位
        f.write(data)
        has_receive += len(data)
    f.close()
'''




