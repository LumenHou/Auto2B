import xml.etree.cElementTree as ET
import pymysql
import sys

scenariosql = """INSERT INTO scenarioinfo (
            r_Title,
            r_Keywords,
            r_StepSummary,
            r_WebSite,
            r_Status,
            r_GroupName,
            Title,
            Keywords,
            WebSite,
            STATUS,
            GroupName,
            StepSummary)
        VALUES(
            '{name}',
            '{keyword}',
            '{Summary}',
            41,
            1,
            {PageNum},
            '{name}',
            '{keyword}',
            41,
            0,
            {PageNum},
            '{Summary}')"""

stepsql = """INSERT INTO stepinfo (
            Type,
            VALUE,
            Action,
            Keywords,
            ScenaID,
            Orderby,
            Description,
            ExpectResult,
            r_Type,
            r_Value,
            r_Action,
            r_Keywords,
            r_Orderby,
            r_Description,
            r_ExpectResult
        )
        VALUES(
            '{type}',
            '{value}',
            '{action}',
            '{keys}',
            {SID},
            {OID},
            '{Des}',
            '{Result}',
            '{type}',
            '{value}',
            '{action}',
            '{keys}',
            {OID},
            '{Des}',
            '{Result}')"""

DuplicateSql = """ClickViewAllHPContacts_GlobalFooter
ClickOrderApproveEditIcon_UserDetailsPage
ClickLookupLink_ShoppingCartPage
ClickChangeBillingAddressButton_CheckoutPage
SelectBillingAddress_CheckoutPage
ClickBillingAddressOKButtopn_CheckoutPage
ClickRequestedDeliveryDateField_CheckoutPage
ClickLookupLink_CheckoutPage
SelectHardwarePurchaseDate_CheckoutPage
SelectHardwarePurchaseDate_CheckoutPage
ClickShowMoreLink_ProductDetailsPage
InputQuantityField_ProductDetailsPage
ClickViewAllPRToApproveLink_HomePage
ClickViewAllPRToApproveLink_HomePage
InputSearchFields_CustomerServicePage
ClickCloseError_OptionCodeOverlay
ClickCloseError_OptionCodeOverlay
CloseBrowser_BrowserAction
ClickOutsideOfOverlay_CartConfirmationOverlay
UpdateFavoriteName_FavoriteDetailPage
ClickGoButton_PFPHomePage
SelectDocument_ManageDocumentPage
ClickRadioButton_SPCLookupOverlay
ClickCancelButton_SPCLookupOverlay
ClickApplyButton_SPCLookupOverlay
ClickSelectApproverDropdown_AssignApproverOverlay
ClickSaveButton_AssignApproverOverlay
ClickCancelButton_AssignApproverOverlay
SelectApprover_AssignApproverOverlay
ClickAdvancedOptionsArrow_BatchEditUsersPage
UpdateSelectableDropdowns_BatchEditUsersPage"""

NewPageScenario = """GlobalHead_MoveCursorToBlank
OrgUsersPage_ClickAddUserButton
OrgUsersPage_ClickUserNameLink
OrgUsersPage_ClickOrganizationsDropdown
OrgUsersPage_SelectOrganizations
OrgUsersPage_ClickSearchExpansion
OrgUsersPage_InputUserName
OrgUsersPage_ClickSearchButton
OrgUsersPage_ClickUserActionsIcon
OrgUsersPage_SelectViewDetailsOption
OrgUsersPage_ClickEnableUserAccount
OrgUsersPage_ClickDisableUserAccount
OrgUsersPage_ClickClearResultsButton
OrgUsersPage_ClickGenerateURLButton
UserDetailsPage_ClickSpendingLimitCancelButton
CheckoutPage_InputOrderUDFA
CheckoutPage_InputOrderUDFB
CheckoutPage_InputOrderUDFC
CheckoutPage_InputOrderUDFD
CheckoutPage_ClickShippingProfileDropdown
CheckoutPage_SelectShippingProfileOption
CheckoutPage_ClickShipAddressOKButton
CheckoutPage_InputCarePackPhone
ProductDetailsPage_ClickRelatedProductCarouselRightArrow
HomePage_ClickOrderStatusTab
HomePage_ClickOrderStatusLink
CategoryPage_FirstProductAddToCart
CategoryPage_SelectItemsPerPage
SearchResultPage_SelectItemsPerPageDropdown
CustomerServicePage_SelectEnableUserOption
CustomerServicePage_SelectDisableUserOption
OrgCatalogAccessOverlay_CheckOrg
OrgCatalogAccessOverlay_UncheckOrg
OrgCatalogAccessOverlay_UncheckMemberGroups
PRToApprovePage_SelectPRViewDetailsOption
CartPreviewOverlay_ClickProductNumber
CartPreviewOverlay_ClickProductQuantity
CartPreviewOverlay_ClickProductPrice
CartPreviewOverlay_ClickOutsideOfOverlay
PFPLoginPage_ClickProfilePeferencesButton
PFPLoginPage_ClickHomeLink
PSPunchoutPage_ClickVisitmystorebutton
BatchEditUsersPage_ClickPageNumber
HPCatalogPage_InputCarouselQuantity
HPCatalogPage_ClickCarouselImage
HPCatalogPage_ClickCarouselAddToCart
UserDetailOverlay_ClickCountryRegionDropdown
UserDetailOverlay_ClickPreferredLanguageDropdown
UserDetailOverlay_ClickPrimaryJobDropdown
UserDetailOverlay_ClickCancelButton
UserDetailOverlay_ClickSaveButton
UserDetailOverlay_InputFirstName
UserDetailOverlay_InputLastName
UserDetailOverlay_InputContactPhoneNumber
"""

scenarioStoragepath = 'XMLs/ScenarioStorageV1.xml'

scenariolist = [['BrowserAction', 'CloseBrowser'], ['PRListingPage', 'SelectStartDate'],
                ['PRListingPage', 'SelectEndDate'], ['PRListingPage', 'ClickClearResultButton'],
                ['PRListingPage', 'SelectViewOptionMenu'], ['PRToApprovePage', 'SelectStartDate'],
                ['PRToApprovePage', 'SelectEndDate'], ['PRToApprovePage', 'ClickSearchButton'],
                ['PRToApprovePage', 'ClickSearchOptionsExpansion'], ['PRToApprovePage', 'ClickClearResultButton'],
                ['PRToApprovePage', 'SelectViewOptionMenu'], ['GlobalHead', 'SelectSearchTypeDropdown'],
                ['FavoriteDetailPage', 'UpdateFavoriteName'],
                ['CustomerServicePage', 'SelectEnableUserOption'], ['CheckoutPage', 'InputEmailNotificationComment']]

# ['PSPunchOutPage', 'ClickVisitmystorebutton'],

class stepSql():

    def setAttr(self, id, type, value, action, keys):
        self.id = id
        self.type = type
        self.action = action
        self.keys = keys
        self.value = value
        return self

    def setNew(self, boolean):
        self.new = boolean
        return self

    def __init__(self):
        self.id = ''
        self.type = ''
        self.action = ''
        self.keys = ''
        self.value = ''
        self.order = ''
        self.description = ''
        self.SID = ''
        self.expect = ''
        self.new = False

    def getSql(self):
        if self.new:
            newsql = stepsql.format(type=self.type, value=self.value, action=self.action, keys=self.keys,
                                    OID=self.order, SID=self.SID, Des=self.description, Result=self.expect)
        else:
            newsql = """UPDATE stepinfo
                        SET type = '{type}',
                        r_type = '{type}',
                        VALUE = '{value}',
                        r_value = '{value}',
                        action = '{action}',
                        r_action = '{action}',
                        keywords = '{keys}',
                        r_keywords = '{keys}'
                        WHERE
                        id = {id}""".format(type=self.type, value=self.value, action=self.action, keys=self.keys,
                                            id=self.id)
        return newsql

    pass


class scenarioSql():

    def __init__(self):
        self.id = 0
        self.steps = []
        self.pageid = ''
        self.scenarioname = ''
        self.summary = ''

    def setUp(self, page, scenario):
        self.pageid = page
        self.scenarioname = scenario

        return self

    def append(self, ob):
        self.steps.append(ob)
        return self.steps

    def setChildOrder(self):
        for i, o in enumerate(self.steps):
            o.order = i

    def setChildeSID(self, id):
        for chlid in self.steps: chlid.SID = id

    def getsql(self):
        return scenariosql.format(name=self.scenarioname, keyword=self.scenarioname, Summary=self.summary,
                                  PageNum=self.pageid)


def getPageid(cursor):
    SQL = 'select id,value from commoninfo where typeof = 3'
    cursor.execute(SQL)
    result = cursor.fetchall()
    return {row[1]: row[0] for row in result}


def getexistScenario(cursor):
    sql = """select scenarioinfo.id, r_Title, value as PageName
from scenarioinfo, commoninfo
where scenarioinfo.r_GroupName = commoninfo.ID"""

    cursor.execute(sql)
    result = cursor.fetchall()

    return {'%s_%s' % (row[2], row[1]): row[0] for row in result}


def main(cursor):
    cursor.execute('select MAX(id) from stepinfo')
    stepID = cursor.fetchone()[0] + 1
    cursor.execute('select MAX(id) from scenarioinfo')
    scenarioID = cursor.fetchone()[0] + 1

    import string
    sqllist = []
    root = ET.parse('XMLs/ScenarioStorageV1.xml').getroot()
    stepTem = string.Template(stepsql)
    ScenarioTem = string.Template(scenariosql)
    for page in root:
        pageName = page.attrib['PageName']
        scenariodic = {'id': '', 'name': '', 'keyword': '', 'StepSummary': '', 'PageNum': ''}

        for scenario in page:
            scenarioName = scenario.attrib['ScenarioName']
            scenariodic['name'] = scenarioName
            Esummary = ET.Element('Scenario')
            tempstr = '%s_%s' % (pageName, scenarioName)
            # if tempstr in existScenario:
            #    continue
            if scenario.find('action/step') == None:
                continue
            steps = scenario.find('action')
            stepdic = {'id': '', 'type': '', 'action': '', 'keys': '', 'ScenarioID': '', 'Orderby': '', 'Des': '',
                       'Result': '', 'value': ''}
            stepOrderid = 0
            for step in steps:
                stepdic['id'] = stepID
                Estep = ET.Element('s')
                Esummary.append(Estep)
                stepdic['Orderby'] = stepOrderid
                stepdic['ScenarioID'] = scenarioID  # ScenarioID
                Ea = ET.Element('a')
                Et = ET.Element('t')
                Ek = ET.Element('k')
                Estep.append(Ea)
                Estep.append(Et)
                Estep.append(Ek)
                if step.get('type'):
                    Et.text = step.attrib['type']
                    stepdic['type'] = step.attrib['type']
                if step.get('action'):
                    Ea.text = step.attrib['action']
                    stepdic['action'] = step.attrib['action']
                if step.get('keys'):
                    Ek.text = step.attrib['keys']
                    stepdic['keys'] = step.attrib['keys']
                if step.get('value'):
                    stepdic['value'] = step.attrib['value']
                sqllist.append(stepTem.safe_substitute(stepdic))
                stepOrderid += 1
                stepID += 1
                stepdic = {}
            str = ET.tostring(Esummary).decode('utf-8')
            scenariodic['StepSummary'] = str
            # scenariodic['PageNum'] = pagedic[pageName]
            scenariodic['id'] = scenarioID
            sqllist.append(ScenarioTem.safe_substitute(scenariodic))
            scenarioID += 1
            scenariodic = {}

    for sql in sqllist:
        try:
            cursor.execute(sql)
            # db.commit()
        except Exception as e:
            print(sql)
            print(e)
            # db.rollback()


def comparseStep(action, result):
    steps = []
    for i, s in enumerate(action):
        if result[i][1] != s.get('type', result[i][1]):
            sp = stepSql().setAttr(result[i][0], s.get('type', result[i][1]), s.get('value', result[i][2]),
                                   s.get('action', result[i][3]), s.get('keys', result[i][4]))
            steps.append(sp)
            continue
        if result[i][2] != s.get('value', result[i][2]):
            sp = stepSql().setAttr(result[i][0], s.get('type', result[i][1]), s.get('value', result[i][2]),
                                   s.get('action', result[i][3]), s.get('keys', result[i][4]))
            steps.append(sp)
            continue
        if result[i][3] != s.get('action', result[i][3]):
            sp = stepSql().setAttr(result[i][0], s.get('type', result[i][1]), s.get('value', result[i][2]),
                                   s.get('action', result[i][3]), s.get('keys', result[i][4]))
            steps.append(sp)
            continue
        if result[i][4] != s.get('keys', result[i][4]):
            sp = stepSql().setAttr(result[i][0], s.get('type', result[i][1]), s.get('value', result[i][2]),
                                   s.get('action', result[i][3]), s.get('keys', result[i][4]))
            steps.append(sp)
            continue
    return steps


def updatePage(cursor, pagelist):
    pageidlist = getPageid(cursor)
    cursor.execute('select MAX(id) from scenarioinfo')
    scenarioID = cursor.fetchone()[0] + 1
    for page in pagelist:
        if page in pageidlist:
            continue
        else:
            cursor.execute('insert into commoninfo (%s, %s, 3)' % (scenarioID, page))
            scenarioID += 1


def Getsummay(actions):
    EScenario = ET.Element('Scenario')
    for step in actions:
        Estep = ET.Element('s')
        EScenario.append(Estep)
        Ea = ET.Element('a')
        Et = ET.Element('t')
        Ek = ET.Element('k')
        Estep.append(Ea)
        Estep.append(Et)
        Estep.append(Ek)
        if step.get('type'):
            Et.text = step.attrib['type']
        if step.get('action'):
            Ea.text = step.attrib['action']
        if step.get('keys'):
            Ek.text = step.attrib['keys']
    return ET.tostring(EScenario).decode('utf-8')


def getstepsObjectlist(actions):
    stepslist = []
    for step in actions:
        if step.get('action', None):
            action = step.get('action')
        else:
            action = step.get('special', None)
        stepO = stepSql().setNew(True).setAttr(0, step.get('type', ''), step.get('value', ''),
                                               action, step.get('keys', ''))
        stepslist.append(stepO)
    return stepslist


def main2():
    db = pymysql.connect('192.168.1.153', 'root', '111111', 'autodev')
    root = ET.parse('XMLs/ScenarioStorageV1.xml').getroot()
    testsql = """SELECT
    	stepinfo.ID,
    	stepinfo.Type,
    	stepinfo.VALUE,
    	stepinfo.Action,
    	stepinfo.Keywords,
    	scenarioinfo.r_Title AS ScenarioName,
    	commoninfo.
    VALUE
    	AS PageName,
    	scenarioinfo.ID as SID
    FROM
    	stepinfo,
    	scenarioinfo,
    	commoninfo
    WHERE
    	stepinfo.ScenaID = scenarioinfo.ID
    AND scenarioinfo.r_GroupName = commoninfo.ID
    AND stepinfo.ScenaID != 0
    AND scenarioinfo.r_Title = '{ScenarioName}'
    AND commoninfo.VALUE = '{PageName}'"""
    cursor = db.cursor()
    pageid = getPageid(cursor)
    scenarioid = getexistScenario(cursor)
    # a, b, c = 0, 0, 0
    steplist = []
    temp = {}
    for page in root:
        for scenario in page:
            action = scenario.findall('action/step')
            steps = scenario.findall('script/StepResult')
            if len(action) == 0:
                continue
            cursor.execute(
                testsql.format(ScenarioName=scenario.attrib['ScenarioName'], PageName=page.attrib['PageName']))
            result = cursor.fetchall()
            pagename = page.attrib['PageName']
            scenarioname = scenario.attrib['ScenarioName']
            if len(result) == 0:
                continue
                # a += 1
                #
                # if pagename in temp.keys():
                #     t = temp[pagename]
                #     t.append(scenarioname)
                #     temp[pagename] = t
                # else:
                #     temp[pagename] = [scenarioname]
                # Sobject = scenarioSql().setUp(pageid[pagename], scenarioname)
                # Sobject.summary = Getsummay(action)
                # Sobject.steps = getstepsObjectlist(action)
                # Sobject.setChildOrder()
                # # try:
                # #     print(Sobject.getsql())
                # #     cursor.execute(Sobject.getsql())
                # #     db.commit()
                # # except Exception as e:
                # #     print('roll back', e)
                # #     db.rollback()
                # #     db.close()
                # #     sys.exit(1)
                # for i, child in enumerate(Sobject.steps):
                #     child.SID = scenarioid['%s_%s' % (pagename, scenarioname)]
                #     try:
                #         child.description = steps[i].attrib['description']
                #         child.expect = steps[i].attrib['result']
                #     except:
                #         pass
                #     # try:
                #     #     cursor.execute(child.getSql())
                #     #     db.commit()
                #     # except Exception as e:
                #     #     print(child.getSql())
                #     #     print('roll back', e)
                #     #     db.rollback()
                #     #     db.close()
                #     #     sys.exit(1)
            if len(action) < len(result):
                print(pagename, scenarioname)
                a = int(len(result) / 2)
                sql = 'DELETE FROM {table} WHERE id = {ID}'
                steplist.append(sql.format(table='scenarioinfo', ID=result[-1][-1]))
                for r in result[a:]:
                    steplist.append(sql.format(table='stepinfo', ID=r[0]))
                # for sql in steplist:
                #     try:
                #         cursor.execute(sql)
                #         db.commit()
                #     except:
                #         print(sql)
                #         print('roll back')
                #         db.rollback()
            if len(action) > len(result):
                # print(pagename, scenarioname)
                SID = scenarioid['%s_%s' % (pagename, scenarioname)]
                for i, item in enumerate(action):
                    try:
                        s = stepSql().setAttr(result[i][0], item.get('type', ''), item.get('value', ''),
                                              item.get('action', ''), item.get('keys', ''))
                        # print(s.getSql())
                    except IndexError as e:
                        s = stepSql().setAttr(0, item.get('type', ''), item.get('value', ''),
                                              item.get('action', ''), item.get('keys', ''))
                        s.SID = SID
                        s.new = True
                        s.order = i
                    # print(s.getSql())
                    # try:
                    #     cursor.execute(s.getSql())
                    #     db.commit()
                    # except:
                    #     print(s.getSql())
                    #     print('roll back')
                    #     db.rollback()
                pass

    db.close()
    # print(scenarioid.popitem())

def main3(page, scenario):
    def run(sql):
        # print(sql)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception as e:
            print(sql)
            print(e)
            db.rollback()

    db = pymysql.connect('192.168.1.153', 'root', '111111', 'autodev')
    cursor = db.cursor()

    cursor.execute('select MAX(id) from scenarioinfo')
    scenarioID = cursor.fetchone()[0] + 1

    root = ET.parse('XMLs/ScenarioStorageV1.xml').getroot()
    pageid = getPageid(cursor)
    scenarioid = getexistScenario(cursor)
    action = root.findall('./Page[@PageName="%s"]/Scenario[@ScenarioName="%s"]/action/step' % (page, scenario))
    steps = root.findall('./Page[@PageName="%s"]/Scenario[@ScenarioName="%s"]/script/StepResult' % (page, scenario))

    Sobject = scenarioSql().setUp(pageid[page], scenario)
    Sobject.summary = Getsummay(action)
    Sobject.steps = getstepsObjectlist(action)
    # print(action)
    Sobject.setChildOrder()
    Sobject.id = scenarioID

    run(Sobject.getsql())

    for i, child in enumerate(Sobject.steps):
        # child.SID = scenarioid['%s_%s' % (page, scenario)]
        child.SID = Sobject.id
        try:
            child.description = steps[i].attrib['description']
            child.expect = steps[i].attrib['result']
        except:
            pass

        run(child.getSql())


if __name__ == '__main__':
    # main3('BrowserAction', 'CloseBrowser')
    for page, scenario in scenariolist:
        main3(page, scenario)