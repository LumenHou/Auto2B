import pymysql

pymysql.install_as_MySQLdb()

db = pymysql.connect('192.168.1.153', 'root', '111111', 'autodev')
cursor = db.cursor()


def runsql(sql):
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(sql, e)
        db.rollback()


def runlist(list):
    for l in list:
        runsql(l)


def getAllResult():
    return cursor.fetchall()


def getOneResult():
    return cursor.fetchone()


def shutdown():
    return db.close()
