import pymysql
import time

class DB():
    def __init__(self, sql_conn):
        # 建立连接
        self.conn = sql_conn
        # 创建游标，操作设置为字典类型
        print("Mysql connect Sucessful!")
        self.cur = self.conn.cursor(cursor = pymysql.cursors.DictCursor)
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

    def stm32_update(self, ID, temp):
        # 执行SQL语句
        try:
            self.cur.execute("SELECT number FROM base WHERE rfid = %s " % (ID))
            results = self.cur.fetchall()[0]['number']
            try:
                self.cur.execute("INSERT INTO out_info(time, number, rfid, temp) VALUES ('%s', '%s',  '%s', '%s')" % (self.Get_time(), results, ID, temp))
                self.conn.commit()
                return 1
            except:
                print('插入数据失败')
                return 0
        except:
            return 0
    def Get_time(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def Android(self, data):
        # 执行SQL语句
        try:
            data[4] = data[4].replace('\\', '\\\\')
            if self.cur.execute("select * from base where number = %s"%(data[0])):
                return 2
            self.cur.execute("INSERT INTO base(number, name, password, rfid, path) VALUES ('%s', '%s', '%s', '%s', '%s')"%(tuple(data)))
            self.conn.commit()
            return 1
        except:
            return 0

    def Android_update(self, data):
        try:
            self.cur.execute("INSERT INTO health_info(time, number, site, state, temp) VALUES ('%s', '%s', '%s', '%s', '%s')" % (tuple(data)))
            self.conn.commit()
            return 1
        except:
            return 0









'''
@注册的时候添加学生信息
@name 学生姓名
@student_number 学生学号
@rfid RFID编号
@示例：inser_student('wangxiaokang',2017213023, 'HIDH217G')
'''
def inser_student(name, student_number, rfid):
    with DB(db='TESTDB') as db:
        try:
            #db.execute("CREATE TABLE student_inf(name TINYBLOB, student_number MEDIUMINT, rfid MEDIUMINT,PRIMARY KEY('student_number')) ")
            db.execute("SELECT * FROM student_inf WHERE student_number = %s" % (student_number))
            result = db.fetchall()
            if result:
                print("Database has this man!")
                return 1
            else:
                db.execute("INSERT INTO student_inf(name, student_number, rfid) VALUES ('%s', %s, '%s')" % (name, student_number, rfid))
                print("Insert this student ok!")
                return 0
        except:
            print("INSERT STUDENT ERROR!!!")



def insert_temp(rfid, temp):
    with DB(db='TESTDB') as db:
        times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            db.execute("SELECT * FROM student WHERE id = '%s'" % (rfid))
            result = db.fetchall()
            if result:
                db.execute("INSERT INTO student(time, id, temp) VALUES ('%s', '%s', %s)"%(times, rfid, temp))
                print('Insert ok!')
                return 1
            else:
                print('No this man!!!')
                return 0
        except:
            print('Search ERROR!!!')
        '''
        try:
            db.execute("SELECT * FROM student")
            if db:
                for i in db:
                    print(i)
        except:
            print("ERROR")
        '''



'''
if __name__ == '__main__':
    Insert('HJFK22S54', 36.5)'''

'''
def Insert_menjin(temp, ID):
    with DB(db='TESTDB') as db:
        time  = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        try:
            db.execute("SELECT * FROM EMPLOYEE WHERE INCOME > %s" % (1000))
        try:
            db.execute("SELECT * FROM EMPLOYEE WHERE INCOME > %s" % (1000))
            print('Get data...')
            result = db.fetchall()
            if db:
                for i in db:
                    print(i)
            else:
                print('No this man')
        except:
            print("ERROR")'''





