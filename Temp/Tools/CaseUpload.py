import pymysql
import simplifyAutomation
import uuid
import datetime


def Newuuid():
    return uuid.uuid4().__str__()


def getNow():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def getScenarioID(cursor, page, scenario):
    idSQL = """select scenarioinfo.ID, scenarioinfo.r_Title, commoninfo.`Value`
from scenarioinfo, commoninfo
where scenarioinfo.r_GroupName = commoninfo.id
and scenarioinfo.r_Title = '{S}'
and commoninfo.`Value` = '{P}'"""

    cursor.execute(idSQL.format(S=scenario, P=page))
    # result = cursor.fetchone()

    return cursor.fetchone()[0]


def getCaselist(UUID,casename):
    temp = 'insert into caseinfo(Code, Version, Title, Status, Website, ID, CreateTime) values ("{UUID}", 0, "{Case}", "1", "149", 0, "{Time}")'
    # [Newuuid(), 0, casename, '1', '41', 0, getNow()]
    return temp.format(UUID=UUID, Case= casename, Time=getNow())


def getCtoSlist(code, ScenID, Order, Checkpoint):
    temp = 'insert into casetoscen(CaseCode, CaseVersion, ScenarioID, orderby, value) VALUE ("{Code}", 0, {SID}, {Order}, {Checkpoint})'
    # [code, 0, ScenID, Order, Checkpoint]
    return temp.format(Code=code, SID= ScenID, Order=Order, Checkpoint= Checkpoint)


"""update checkpointinfo_copy set Title = (select r_Title from scenarioinfo where checkpointinfo_copy.ScenarioID = scenarioinfo.ID);
update checkpointinfo_copy set Website = (select r_Website from scenarioinfo where checkpointinfo_copy.ScenarioID = scenarioinfo.ID)"""


def main():
    db = pymysql.connect('192.168.1.153', 'root', '111111', 'autodev')
    cursor = db.cursor()
    Casesqllist = []
    # Scenariosqllist = []
    path = r"C:\Users\chui\Desktop\R1.1_Place Order_PR Confirmation_Navigation_Continue Shopping.xlsx"
    excelScenario = simplifyAutomation.exceltoscript(path)
    # print(path.split('\\'))
    caseName = path.split('\\')[-1][:-5]
    UID = Newuuid()
    caseT = getCaselist(UID, caseName)
    Casesqllist.append(caseT)
    # print(caseT)
    for sheetName in excelScenario.keys():
        for scenario in excelScenario[sheetName][0]:
            orderbyid = scenario[0] - 1
            pageName = scenario[1]
            scenName = scenario[2]
            ScenID = getScenarioID(cursor, pageName, scenName)
            if scenario[3]:
                # print(scenario[3])
                sql = 'insert into checkpointinfo_copy(ScenarioID, Value) values (%s, "%s")' % (str(ScenID), scenario[3])
                try:
                    # print(sql)
                    cursor.execute(sql)
                    print(sql, 'is ok')
                    db.commit()
                except Exception as e:
                    print(e)
                    db.rollback()
                checkpoint = int(cursor.lastrowid)
            else:
                checkpoint = 0
            Casesqllist.append(getCtoSlist(UID, ScenID, orderbyid, checkpoint))

    # print(Casesqllist)
    for sql in Casesqllist:
        try:
            cursor.execute(sql)
            print(sql, ' is ok')
            db.commit()
        except Exception as e:
            print(e)
            print(sql)
            db.rollback()

    db.close()

if __name__ == '__main__':
    main()
    # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
