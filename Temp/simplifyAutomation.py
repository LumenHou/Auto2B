__author__ = 'Lumen'
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import xlrd
import string
import copy
import os


# path: 一个xmlMapping表的路径
# 返回一个[Pagename: [Scenario: xmlObject]]的字典对象
# xmlObject: <Scenario name='PageName' Scenario='ScenarioName'>
def pagescrnariomapping(path=r'XMLs/Temp.xml'):
    XMLMapping = {}

    tree = ET.parse(path)
    root = tree.getroot()

    for child in root:
        ScenarioMapping = {}
        # print(child.tag + ':')  # PageName
        for Scenario in child:
            # print(Scenario.tag + "-")  # ScenarioName
            # print(child.tag)
            ScriptScenario = ET.Element('Scenario', attrib={'name': child.tag, 'Scenario': Scenario.tag})
            for script in Scenario:
                ScriptScenario.append(script)
            ScenarioMapping[Scenario.tag] = ScriptScenario
            # ScriptScenario = {}
        XMLMapping[child.tag] = ScenarioMapping

    return XMLMapping


# 把新的NewScriptPath解析并加入到MappingPath文件中
def addNewMapping(NewScriptPath, MappingPath=r'XMLs/newTemp.xml'):
    newXml = ET.parse(NewScriptPath).getroot()
    oldXml = ET.parse(MappingPath).getroot()
    # page = ''
    for newScenario in newXml:
        pagename = newScenario.attrib['name']
        scenarioname = newScenario.attrib['scenarioname']
        # print(oldXml.findall('./' + pagename + '/' + scenarioname))
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


# 输入一个excel, 分析数据
# {ScriptName: [[[PageName, ScenarioName],], {DataName: DataValue}]}
def exceltoscript(excelpath=r"C:\Users\chui\Desktop\PCP Pagination.xlsx"):
    excelscript = xlrd.open_workbook(excelpath)
    sheets = excelscript.sheets()
    scripts = {}
    for sheet in sheets:
        script = []
        datas = {}
        rows = sheet.nrows
        # print (rows)
        key = ''
        for row in range(1, rows):
            data = {}
            pagename = sheet.cell(row, 1).value
            scenario = sheet.cell(row, 2).value
            checkpoint = sheet.cell(row, 3).value
            if pagename == '' or scenario == '':
                if sheet.cell(row, 4).value != '' and sheet.cell(row, 5).value != '':
                    temp = datas[key]
                    temp[sheet.cell(row, 4).value] = sheet.cell(row, 5).value
                    datas[key] = temp
                continue
            num = int(sheet.cell(row, 0).value)

            key = str(num) + '_' + pagename + '_' + scenario
            script.append((num, pagename, scenario, checkpoint))
            data[sheet.cell(row, 4).value] = sheet.cell(row, 5).value
            datas[key] = data
        # del data['']
        scripts[sheet.name] = [script, datas]
        # print(script)
        # print(datas)
    return scripts


def xmltoone(xmllist, casename):
    xmlOne = ET.Element('Script', attrib={'name': casename})
    for xmlO in xmllist: xmlOne.append(xmlO)
    return xmlOne


if __name__ == '__main__':
    scripts = exceltoscript()
    # mapping = pagescrnariomapping()
    scenariostorage = ET.parse(r'XMLs/ScenarioStorageV1.xml')
    newelements = []
    for casename in scripts.keys():
        script = scripts[casename][0]
        datas = scripts[casename][1]
        pagename = ''
        for scr in script:
            key = str(scr[0]) + '_' + scr[1] + '_' + scr[2]
            scenarioxpath = './Page[@PageName="%s"]/Scenario[@ScenarioName="%s"]/action' % (scr[1].strip(), scr[2].strip())
            Eaction = scenariostorage.find(scenarioxpath)
            if Eaction is None:
                # print('./Page[@PageName="' + scr[1] + '"]/Scenario[@ScenarioName="' + scr[2] + '"]/action')
                print(scenarioxpath)
                print('is not correct path')
                exit(1)
            if Eaction.find('step') is None:
                print(scenarioxpath)
                print('Above path not have step child')
                exit(1)
            tempeles = copy.deepcopy(Eaction)
            tempeles.tag = 'Scenario'
            tempeles.attrib = {'name': scr[1], 'Scenario': scr[2]}
            data = datas[key]
            # if pagename != scr[1]: # 'Overlay' BrowserAction
            if pagename not in [scr[1], 'BrowserAction'] and 'Overlay' not in scr[1]:
                pagename = scr[1]
                pageScreen = ET.Element('step', attrib={'action': 'pagescreen', 'keys': '$num', 'value': pagename})
                tempeles.insert(0, pageScreen)
            checkpoint = ET.Element('CheckPoint',
                                    attrib={'value': scr[3], 'keys': key})
            tempeles.insert(1, checkpoint)
            for temp in tempeles:
                if 'value' in temp.keys():
                    if '$' in temp.attrib['value']:
                        temp.attrib['value'] = string.Template(temp.attrib['value']).safe_substitute(data)
                if 'keys' in temp.keys():
                    if '$' in temp.attrib['keys']:
                        temp.attrib['keys'] = key
            newelements.append(tempeles)
        # tempeles = None
        if not os.path.exists('CaseXmls'):
            os.mkdir('CaseXmls')
        ET.ElementTree(xmltoone(newelements, casename)).write('CaseXmls/' + casename + '.xml')
        newelements = []
        print('CaseXmls/%s.xml is complete' % casename)
