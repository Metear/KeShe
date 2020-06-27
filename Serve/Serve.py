import db
import socket
# import task
import thread
import pymysql
from DBUtils.PooledDB import PooledDB

# 172.25.51.65 40
sk = socket.socket()
address = ('172.25.51.65', 40)
sk.bind(address)  # 将本地地址与一个socket绑定在一起
sk.listen(30)  # 最多允许有3个客户称呼
pool = PooledDB(pymysql, 20, host="47.95.211.155", port=3306, db="whoere", user='zf', passwd='zf2279', charset='utf8')


def main():
    try:
        # task.task()
        print('waiting........ ')
        while 1:
                conn, addr = sk.accept()
                sql_conn = db.DB(pool.connection())  # 创建数据库线程池连接
                t = thread.Sever(conn, addr, sql_conn)  # 创建新线程来处理TCP连接
    except:
        print("启动线程错误!!!")

if __name__ == "__main__":
    try:
        main()
    except:
        print("Start ERROR!")





