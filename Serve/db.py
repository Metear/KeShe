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

    # 登陆函数
    def login(self, number, passwd):
        # 执行SQL语句
        try:
            self.cur.execute("SELECT password FROM base WHERE number = %s " % (int(number)))
            results = self.cur.fetchall()[0]['password']
            if results:
                if results == passwd:
                    print('login ok!')
                    return 1
                else:
                    print('Wrong passwd!')
                    return 0
        except:
            print('Search man ERROR!!!')
            return 3

    def Get_time(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def Android(self, data):
        # 执行SQL语句
        try:
            data[4] = data[4].replace('\\', '\\\\')
            if self.cur.execute("select * from base where number = %s" % (data[0])):
                return 2
            self.cur.execute(
                "INSERT INTO base(number, name, password, rfid, path, fitness) VALUES ('%s', '%s', '%s', '%s', '%s', '1')" % (
                    tuple(data)))
            self.conn.commit()
            return 1
        except:
            return 0

    def Android_update(self, data):
        try:
            self.cur.execute(
                "INSERT INTO health_info(time, number, site, state, temp) VALUES ('%s', '%s', '%s', '%s', '%s')" % (
                    tuple(data)))
            self.conn.commit()
            self.Change_clock(data[1])
            if data[4] > '37.5':
                self.Change_fitness(data[1], data[4])
                self.cur.execute("INSERT INTO abnormal(time, number, temp) \
                                VALUES ('%s', '%s', '%s')" % (self.Get_time(), data[1], data[4]))
                self.conn.commit()
            return 1
        except:
            return 0

    def Change_clock(self, number):
        times = int(self.Get_time().split(' ')[1].split(':')[1])

        if 6 < times < 10:
            self.cur.execute("UPDATE base set am_clock = '%s' where number = '%s" % ('yes', number))
            self.conn.commit()
        elif 18 < times < 22:
            self.cur.execute("UPDATE base set pm_clock = '%s' where number = '%s" % ('yes', number))
            self.conn.commit()

    def Change_fitness(self, state, rfid):
        try:
            self.cur.execute("UPDATE base set fitness = '%s' where number = '%s" % (state, rfid))
            self.conn.commit()
            return 1
        except:
            return 0

    def Get_rfid(self,rfid):
            self.cur.execute("SELECT number FROM base WHERE rfid = '%s'" % (rfid))
            number = self.cur.fetchall()[0]['number']
            if number:
                self.cur.execute("INSERT INTO out_info(time, number) \
                                                VALUES ('%s', '%s', '%s')" % (self.Get_time(), number, rfid))
                self.conn.commit()
                return number
            else:
                return 0

    def stm32_update(self, rfid, temp, number=0):
        # 执行SQL语句
        if number:
            results = number
        else:
            results = self.Get_rfid(rfid)
            if results:
                return 3
        self.Change_clock(number)
        try:
            if temp < '37.3':
                self.cur.execute("INSERT INTO out_info(time, number, temp) \
                                 VALUES ('%s', '%s', '%s')" % (self.Get_time(), results, temp))
                self.conn.commit()
                return 1
            else:
                self.cur.execute("INSERT INTO abnormal(time, number, temp) \
                                 VALUES ('%s', '%s', '%s')" % (self.Get_time(), results, temp))
                self.conn.commit()
                self.Change_fitness('0', results)
                return 2
        except:
            print('插入数据失败')
            return 0
