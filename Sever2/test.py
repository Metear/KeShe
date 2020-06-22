import pymysql
import time
from DBUtils.PooledDB import PooledDB
# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
#db = pymysql.connect(host="47.95.211.155", user="zf", passwd="zf2279", port=3306, db="TESTDB")
db = PooledDB(pymysql, 20, host="47.95.211.155", port=3306, db="TESTDB", user='zf', passwd='zf2279', charset='utf8').connection()
# 使用 cursor() 方法创建一个游标对象 cursor
number = 2017213025
cursor = db.cursor()
def Get_time():
    return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


data = ['2017213025', 'zhangfeng', 'zf79', 'jdhs123', 'E:\\ClassDesign\\Sever\\Picture\\2017213023.png']

data[4] = data[4].replace('\\', '\\\\')
print(data)
try:
    # 执行SQL语句
    print(Get_time())
    if cursor.execute("select * from base where number = %s"%(data[0])):
        print("Haved the man")
    else:
        cursor.execute("INSERT INTO base(number, name, password, rfid, path) VALUES ('%s', '%s', '%s', '%s', '%s')"%(tuple(data)))
        cursor.execute("SELECT * FROM base")
        results = cursor.fetchall()
        print(results)
        print("Insert ok ")
        db.commit()
        #print("upload ok")
        # 获取所有记录列表


    '''
    for row in results:
        fname = row[0]
        lname = row[1]
        age = row[2]
        sex = row[3]
        income = row[4]
        # 打印结果
        print("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
              (fname, lname, age, sex, income))
              '''
except:
    print("Error: unable to fetch data")


# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()
print("Database version : %s " % data)
print('Sucessful!')
# 关闭数据库连接
db.close()