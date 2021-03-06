import pymysql
import time


class DB():
    def __init__(self, sql_conn):
        # 建立连接
        self.conn = sql_conn
        # 创建游标，操作设置为字典类型
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        # 返回游标
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 提交数据库并执行
        self.conn.commit()
        # 关闭游标
        self.cur.close()
        # 关闭数据库连接
        self.conn.close()


    def Get_time(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


    def Get_rfid(self, rfid, come_out=0, come_in=0):
            self.cur.execute("SELECT account FROM email WHERE rfid = '%s'" % (rfid))
            number = self.cur.fetchall()[0]['account']
            if come_out ==1:
                if number:
                    self.cur.execute("INSERT INTO Out_Info(time, student_id,out_in) VALUES ('%s', '%s', '%s')" % (self.Get_time(), number, 'come_out'))
                    self.conn.commit()
                    return number
                else:
                    return 0
            elif come_in == 1:
                if number:
                    self.cur.execute("INSERT INTO Out_Info(time, student_id,out_in) VALUES ('%s', '%s', '%s')" % (self.Get_time(), number, 'come_in'))
                    self.conn.commit()
                    return number
                else:
                    return 0

    def camer_update(self, student_number, temp):
        # 执行SQL语句
        try:
            # self.cur.execute("INSERT INTO health(time, student_id, temp, health_status) VALUES ('%s', '%s', '%s', '%s')" % (self.Get_time(), student_number, temp, 'yes'))
            # self.cur.execute("INSERT INTO fc(time, student_id, temp, health_status) VALUES ('%s', '%s', '%s', '%s')" % (self.Get_time(), student_number, temp, 'yes'))
            # self.conn.commit()
            # return 1
            if temp < '37.3':
                self.cur.execute("INSERT INTO fc(time, student_id, temp, health_status) VALUES ('%s', '%s', '%s', '%s')" % (self.Get_time(), student_number, temp, 'yes'))
                self.conn.commit()
                return 1
            else:
                self.cur.execute("INSERT INTO fc(time, student_id, temp, health_status) VALUES ('%s', '%s', '%s', '%s')" % (self.Get_time(), student_number, temp, 'no'))
                self.conn.commit()
                return 2
        except:
            print('插入数据失败')
            return 0
