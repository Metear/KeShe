整体说明：
连接协议：tcp协议
服务器
ip:47.95.211.155
端口：40
每次最大发送数据量1024字节
所有客户端发送:'exit'退出程序，收到："Good by!"：退出成功并断开连接

连接方式：使用tcp连接到对应Ip和端口号后
stm32: 发送'stm32',收到："Welcome stm32!"表示客户端节点身份绑定成功
       发送'rfid_number|temperature',收到："ok"表示身份识别成功，数据录入成功
                                          'error'表示身份识别失败，未通过
                                          "update: rfid|temp"表示数据格式错误，重新发送数据
       发送：'exit',收到：‘Good by!’表示退出并断开连接成功


连接方式：使用tcp连接到对应Ip和端口号后
android: 1、发送：'android'，                   收到：'Welcome Android!' 表示客户端节点身份绑定成功
         2、再发送 'login|user_number|password'，收到：'User ERROR!'       用户错误
                                                   'Password ERROR!'   密码错误
                                                   'login sucessful!'  登陆成功
                                                   'ERROR Please register first!' 用户未注册
                                                   格式错误："login ERROR,please ENTER like this:'login|user_number|password'"


            2.1、登陆成功后上传健康信息
                 发送： update|number|site|state|temp    update:更新命令; number:学号; site:所在地点; state:健康状态; temp:测量温度
                 收到：'ok'：上传信息成功
                       'error'：上传错误，重新发送
         3、发送： # 注册操作cmd = [    0         1         2         3         4        5           6
                  #               'register', 'number', 'name', 'password', 'rfid', 'filename', 'filesize']
                  register:注册命令
                  number  :学号
                  name    :名字
                  password：密码
                  rfid    ：rfid识别号
                  filename：图片文件名称（.png文件，如：'hero.png'）
                  filesize：图片文件长度
            收到："starting"：开始接收图片
                  'Add'     ：注册成功
                  'Haved'   ：已有该用户

# 打开数据库连接（ip/数据库用户名/登录密码/数据库名）
db = pymysql.connect(host="47.95.211.155", user="zf", passwd="zf2279", port=3306, db="TESTDB")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
# cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

'''
# 使用预处理语句创建表
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,
         SEX CHAR(1),
         INCOME FLOAT )"""

cursor.execute(sql)
'''

CREATE TABLE STUDENT (day DAY,time TIME,id VARCHAR, temp FLOAT);
# 使用预处理语句创建表
sql = "CREATE TABLE EMPLOYEE (\
         FIRST_NAME  CHAR(20) NOT NULL,\
         LAST_NAME  CHAR(20),\
         AGE INT,  \
         SEX CHAR(1),\
         INCOME FLOAT )"
"INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) VALUES ('Mac', 'Mohan', 20, 'M', 2000)"
# SQL 插入语句
sql = "INSERT INTO EMPLOYEE(FIRST_NAME,\
         LAST_NAME, AGE, SEX, INCOME)\
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"

login|2017213022|zf79
CREATE TABLE student (time TINYTEXT, id TINYTEXT NOT NULL, temp  FLOAT NOT NULL);

CREATE TABLE student_inf(name TINYBLOB, student_number BIGINT, rfid TINYBLOB,PRIMARY KEY(student_number));

android|login|221112321

android
login|2017213022|zf79

INSERT INTO student_inf('zf', 2017213022, 'HIDH216G')

# SQL 插入语句
sql = "INSERT INTO student(time, id, temp) VALUES ('%s', '%s',  %s)" %  ('2016-04-07 10:29:46', 'HJFK22S54', 37.1)

# SQL 更新语句
sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')

# SQL 查询语句
sql = "SELECT * FROM EMPLOYEE WHERE INCOME > %s" % (1000)

# SQL 删除语句
sql = "DELETE FROM EMPLOYEE WHERE AGE > %s" % (20)


def inset(sql):
    sql = "INSERT INTO EMPLOYEE(FIRST_NAME, LAST_NAME, AGE, SEX, INCOME) VALUES (%s, %s, %s,%s, %s)" % (
    'Zf', 'Mohan', 21, 'M', 1800)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print("Error: unable to fetch data")


inset(sql)

# SQL 查询语句
sql = "SELECT * FROM EMPLOYEE \
       WHERE INCOME > %s" % (1000)
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        fname = row[0]
        lname = row[1]
        age = row[2]
        sex = row[3]
        income = row[4]
        # 打印结果
        print("fname=%s,lname=%s,age=%s,sex=%s,income=%s" % \
              (fname, lname, age, sex, income))
except:
    print("Error: unable to fetch data")

sql = "SELECT * FROM EMPLOYEE WHERE income = %s" % (2000.0)

try:
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        print('His name is %s' % (result))
    else:
        print('No this man')

if self.conn.execute("select * from base where number = %s" % (data[0])):
    return 0


except:
    print("ERROR")

# 使用 execute()  方法执行 SQL 查询
cursor.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()
print("Database version : %s " % data)
print('Sucessful!')
# 关闭数据库连接
db.close()