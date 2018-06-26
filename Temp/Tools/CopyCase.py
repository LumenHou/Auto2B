import Tools.DBObject as DB
import Tools.CaseUpload as tc

searchcase = "select code, version from caseinfo where Title = '{casename}'"

searchCasetoScenario = "select * from casetoscen where CaseCode = '{code}' and CaseVersion = '{version}'"


# insertcase = ""
#
# insertCasetoScenario = ""

def main(test=None):
    sqllist = []
    DB.runsql(searchcase.format(casename=test))
    uuid = tc.Newuuid()
    print(uuid)
    sqllist.append(tc.getCaselist(uuid, test.replace('R1', 'MTP', 1)))

    code, version = DB.getAllResult()[-1]

    DB.runsql(searchCasetoScenario.format(code=code, version=version))

    result = DB.getAllResult()

    for r in result:
        ScenarioID = r[3]
        OrderByID = r[4]
        Checkpointid = r[5]
        sqllist.append(tc.getCtoSlist(uuid, ScenarioID, OrderByID, Checkpointid))

    DB.runlist(sqllist)


if __name__ == '__main__':
    # main()
    main()
    pass
