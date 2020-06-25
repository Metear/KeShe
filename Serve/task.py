import pymysql
from apscheduler.schedulers.background import BackgroundScheduler

def task():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job1, 'cron', hour=10, minute=5)
    scheduler.add_job(job2, 'cron', hour=22, minute=5)
    scheduler.start()

def job1():
    db = pymysql.connect(host="47.95.211.155", user="zf", passwd="zf2279", port=3306, db="TESTDB")
    db.cursor().execute('INSERT INTO  am_not_clock(number, name) SELECT number,name FROM base WHERE \
                         am_clock=Null')    # 上午没有打卡学生信息
    db.cursor().execute('UPDATE  all_not_clock set number=NULL, name = Null')  # 一天都没有打卡的学生的数据表清空
    db.commit()
    db.close()


def job2():
    db = pymysql.connect(host="47.95.211.155", user="zf", passwd="zf2279", port=3306, db="TESTDB")
    db.cursor().execute('INSERT INTO  all_not_clock_old(number, name) SELECT number,name FROM all_not_clock')

    db.cursor().execute('INSERT INTO  all_not_clock(number, name) SELECT number,name FROM base WHERE \
                         am_clock=Null AND pm_clock=Null')

    db.cursor().execute('UPDATE  am_not_clock set number=Null, name = Null')
    db.cursor().execute('UPDATE base set am_clock=Null, pm_clock = Null')
    db.commit()
    db.close()

