from jira import JIRA
import configparser
import shutil

import json
__author__ = 'Lumen'
# -*- coding: utf-8 -*-

#CasePY = r'#-*- coding: utf-8 -*-' + '\n' +  r'from selenium import webdriver'
# /html/body/div[2]/div[2]/div[1]/div[1]/button
#tree = ET.parse("C:\\Users\\chui\\Documents\\myproject\\Common.xml")
    #root = tree.getroot()
    #funName = root.findall("./action/click/xpath/function/name[1]")
    #print(funName[0].text)

#jira = JIRA('https://jxjira.hpcloud.hp.com', basic_auth=('xin.hou','!QAZ2wsx'))
    #print(jira.logging)
    #issue = jira.issue('JR1-29012')
    #print(issue.fields.project.key)
    #print(issue.fields.customfield_10202)
    #print(issue.fields.comment.comments)
    #for comm in issue.fields.comment.comments:
    #    print(comm.body)
    #print(jira.comment('JR1-29012','89990').body)

#iniFileURL = 'XMLs/ElementResult.ini'
#conf = configparser.ConfigParser()
#conf.read(iniFileURL)
#login = conf['LoginPage']

#print(login['UsernameTextboxname'])

# < LoginPage >
# < CELogin >
#
# < / CELogin >
# < / LoginPage >

"""    file = open('case.py','w')
    file.writelines(CasePY)
    file.writelines('\n')
    file.writelines(r'from selenium import webdriver')
    file.close()"""


# path: 一个xmlMapping表的路径
# 返回一个[Pagename: [Scenario: xmlObject]]的字典对象
def pagescrnariomapping(path):
    XMLMapping = {}
    ScenarioMapping = {}
    tree = ET.parse(path)
    root = tree.getroot()

    for child in root:
        #print(child.tag + ':')  # PageName
        for Scenario in child:
            #print(Scenario.tag + "-")  # ScenarioName
            ScriptScenario = ET.Element('Scenario', attrib={'name': child.tag})
            for script in Scenario:
                ScriptScenario.append(script)
            ScenarioMapping[Scenario.tag] = ScriptScenario
            ScriptScenario = {}
        XMLMapping[child.tag] = ScenarioMapping

    return XMLMapping


def addNewMapping(NewScriptPath, MappingPath = r'XMLs/Temp.xml'):
    newXml = ET.parse(NewScriptPath).getroot()
    oldXml = ET.parse(MappingPath).getroot()
    # page = ''
    for newScenario in newXml:
        pagename = newScenario.attrib['name']
        scenarioname = newScenario.attrib['scenarioname']
        #print(oldXml.findall('./' + pagename + '/' + scenarioname))
        if oldXml.findall('./' + pagename + '/' + scenarioname) != []:
            print('有了')
            continue
        if oldXml.findall('./' + pagename) == []:
            page = ET.Element(pagename)
        else:
            page = oldXml.findall('./' + pagename)[0]
        temp = ET.Element(scenarioname)
        for script in newScenario:
            temp.append(script)
        page.append(temp)
        oldXml.append(page)
        print('Updated')
    xmlfile = ET.ElementTree(oldXml)
    xmlfile.write(MappingPath)

if __name__ == '__main__':
    # 一个json字符串, 根据key, 替换指定的value
    # 判断json字符串中是否包含某个子字符串, 递归
    # print(pagescrnariomapping(r'XMLs/newTemp.xml'))
    # print()
    import xml.etree.ElementTree as ET
    import xlrd

    # element = ET.Element('ScriptsDataScore')
    element = ET.parse('XMLs/Scenario_Temp.xml').getroot()

    excelscript = xlrd.open_workbook(r'C:\Users\chui\Desktop\newScenario.xlsx')
    sheets = excelscript.sheets()

    for sheet in sheets:
        rows = sheet.nrows
        for row in range(1,rows):
            page = sheet.cell(row, 0).value
            scenario = sheet.cell(row, 1).value
            description = sheet.cell(row, 2).value
            result = sheet.cell(row, 3).value
            Echeckpoint = ET.Element('CheckPoint', attrib={'description': description, 'result': result})
            Epage = None
            Escenario = None
            if element.find(page) is None:
                Epage = ET.Element(page)
                Escenario = ET.Element(scenario)
                element.append(Epage)
            else:
                # print(element.find(page))
                Epage = element.find(page)
                if Epage.find(scenario) is None:
                    Escenario = ET.Element(scenario)
                    Epage.append(Escenario)
                    # Epage.append(Escenario)
                else:
                    Escenario = Epage.find(scenario)
                # Epage.append(Escenario)
            Escenario.append(Echeckpoint)
            # print(element)
            newxml = ET.ElementTree(element)
            newxml.write('XMLs/Tracy.xml')
