import os
import pymysql
import xlrd

def getkey(path):
    excelscript = xlrd.open_workbook(path)
    key = excelscript.sheet_by_index(0).name
    return key

def getdata(path):
    db = pymysql.connect("192.168.1.153", "root", "111111", "autodev")
    cursor = db.cursor()
    files = os.listdir(path)
    for file in files:
        casename = file.split('\\')[-1][:-5]
        sheetname = getkey(path + '\\' + file)
        sql_code = "SELECT `Code` FROM `caseinfo` WHERE Title='" + str(casename) + "' AND Keyword='" + sheetname +"'"
        #print(sql_code)
        try:
            cursor.execute(sql_code)
            results = cursor.fetchall()
            code = results[0][0]
            sql_ver = "SELECT Version FROM `v_case_maxversion` WHERE `Code`='" + code + "'"
            try:
                cursor.execute(sql_ver)
                results = cursor.fetchall()
                version = results[0][0]
                sql_task = "INSERT INTO tasktocase (TaskID,CaseCode,caseversion,orderby,STATUS) VALUES ('33','" + code + "','" + str(version) + "','0','1')"
                try:
                    # 执行SQL语句
                    cursor.execute(sql_task)
                    db.commit()
                except:
                    print(sql_task)
                    db.rollback()
            except:
                db.rollback()

        except:
            db.rollback()


if __name__ == '__main__':
    getdata(r'C:\Users\webuser3\Desktop\Automation Test Case\pass_test')