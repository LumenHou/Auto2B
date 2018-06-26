import pymysql
import xlrd

__author__ = 'Lumen'
# -*- coding: utf-8 -*-

import os
import PersonalTest.test as TT



def main(dic):
    caseFile = os.listdir(dic)
    # print(dic) [dic + case for case in caseFile]
    # caseFile =[os.path.join(dic, case) for case in caseFile]
    # print([os.path.join(dic, case) for case in caseFile])

    db = pymysql.connect('192.168.1.153', 'root', '111111', 'autodev')
    cursor = db.cursor()

    def excuteSQL(sql):
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print(sql)
            db.rollback()

    codeSql = """select code from caseinfo where caseinfo.Title = '{name}' and caseinfo.Keyword = '{key}' LIMIT 1"""
    versionSQL = 'select max(CaseVersion) from casetoscen where CaseCode = "{code}"'
    tasktocaseSQL = 'INSERT INTO `tasktocase` (`TaskID`, `CaseCode`, `CaseVersion`, `OperateTime`, `Status`) VALUES ("25", "{code}", "{version}", "2018-03-01 14:56:53", "1");'

    for case in caseFile:
        excelscript = xlrd.open_workbook(os.path.join(dic, case))
        sheets = excelscript.sheets()

        caseName = case[:-5]
        keyworlds = sheets[0].name
        # print(caseName, keyworlds)
        excuteSQL(codeSql.format(name=caseName, key=keyworlds))
        code = cursor.fetchone()[0]
        excuteSQL(versionSQL.format(code=code))
        version = cursor.fetchone()[0]
        excuteSQL(tasktocaseSQL.format(code=code, version=version))


def main2(dic):
    caseList = TT.getNotpad(dic)

    pass


def reRunCase(path):
    caseList = TT.getNotpad(path)

    caseList = [case[:-3] for case in caseList]

    db = pymysql.connect('192.168.1.153', 'root', '111111', 'autodev')
    cursor = db.cursor()

    def excuteSQL(sql):
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print(sql)
            db.rollback()

    # codeSql = 'select code from caseinfo where title = "{case}"'
    taskCaseSql = 'update tasktocase set `Status` = 1, ReTryNum = 0 where tasktocase.TaskID = "25" and CaseCode = (select code from caseinfo where title like "{case}%" LIMIT 1)'

    # print(caseList)
    for case in caseList:
        excuteSQL(taskCaseSql.format(case=case))
        print(case)
    # pass



if __name__ == '__main__':
    # main('C:\\Users\\chui\\Desktop\\pass_test')
    # print(xlrd)
    # xlrd.sheet.Sheet
    reRunCase(r'C:\Users\chui\Desktop\casename.txt')