__author__ = 'Lumen'
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import sys, os
import string

PYCase = """__author__ = 'AutoMain'
# -*- coding: utf-8 -*-
from selenium import webdriver
import sys, configparser
$import_other

ScreenIDList = []
numscreenshot = [0]
logPath = []
imgList = []
caseResult = []

def main(common, url, elementsMap):
    common.driver.get(url)

    #logMethod = getattr(Common, 'log')
    #logMethod.__defaults__ = (casename,)

    #Common.caseName = casename
    try:
    $Func_String
    except Exception as e:
        common.log('The Script is not completed')
        common.log(e)
    finally:
        common.report()

if __name__ == '__main__':
    common = Common.Common(sys.argv[0][:-3], webdriver.Firefox())
    elementResource = configparser.ConfigParser()
    iniFileURL = $elementMap
    elementResource.read(iniFileURL)
    main(common, $URL, elementResource)

    common.driver.close()
"""
# StringDric, case替换模板的一个字典
StringDric = {'import_other': 'import Common', 'URL': '', 'Func_String': '',
              'elementMap': '"../XMLs/ElementResult.ini"'}


def get_config(filename=r"XMLs\config.xml"):
    configInfo = {}
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
    except:
        print("Error:cannot parse file:config.xml.")
        sys.exit(1)
    for child in root:
        configInfo[str(child.tag)] = child.text
    return configInfo


def trueprint(str):
    print('\033[1;32;0m', end='')
    print(str)
    print('\033[0m', end='')


def falseprint(str):
    print('\033[1;31;0m', end='')
    print(str)
    print('\033[0m', end='')


# element: step元素， commonroot: Common.xml的root节点
# 把可能的值获取到并传递到dict中, 最后在funName字符串中替换完成并累加到case.py中
def action(element, commonroot, pageName):
    dict = {'pageName': pageName, 'value': ''}  # {'name': type.value}
    for key in element.keys():
        dict[str(key)] = element.attrib[key]
    if element.get('keys') and element.get('type'):
        dict['keys'] = dict['keys'] + dict['type']
    return 'common.' + string.Template(commonroot).safe_substitute(dict) + '\n' + '    '


# 传入case的路径, 解析并最后生成case.py文件
# 暂无返回值
def analyzxml(casePath, outputPath):
    Func_String = ''
    try:
        print('# Script Path:')
        print('# ' + casePath)
        root = ET.parse(casePath).getroot()  # 通过case路径生成一个elementTree的对象
        StringTem = string.Template(PYCase)
    except Exception as e:
        print("Error:cannot parse file:" + casePath)
        print(e)
        return False

    print('# Start scripts steps: ')
    caseName = root.attrib['name']  # 获取caseName值
    if root.find('website'):
        StringDric['URL'] = root.find('website').text
    for child in root.findall('Scenario'):  # child为scenario标签的对象
        print('Current Scenario Name: ' + child.attrib['name'] + ' start')
        try:
            for step in child:  # step为step标签的对象
                if step.tag == 'CheckPoint':
                    Func_String += "    common.checkpoint['" + step.attrib['keys'] + "'] = '''" + step.attrib[
                        'value'] + "'''\n" + '    '
                    continue
                if step.get('special') != None:
                    xmlString = "./special/" + step.attrib['special'] + '/name'
                    Func_String += '    common.' + CommonRoot.find(xmlString).text + '\n' + '    '
                    continue
                xmlString = "./action/" + step.attrib['action'] + '/name'  # 组合成Common.xml的xpath, 为下面传入方法做准备
                Func_String += '    ' + action(step, CommonRoot.find(xmlString).text, child.attrib['name'])
            print('Current Scenario Name: ' + child.attrib['name'] + ' end')
        except:
            return False
    # Func_String += 'common.report()'  # 最终加入report的方法
    StringDric['Func_String'] = Func_String
    CaseFile = open(outputPath + caseName + '.py', 'w')
    CaseFile.writelines('\n')
    CaseFile.writelines(StringTem.safe_substitute(StringDric))
    CaseFile.close()
    print(casePath + '\\' + caseName + ' is end')

    return True


if __name__ == '__main__':
    browser_list = ['firefox', 'ie', 'chrome', 'safari']
    CommonRoot = None
    status = []
    print('#')
    configInfo = get_config()

    print('# initial data from config file..')

    if len(configInfo['Common']) > 0:  # 加载common.xml
        print("Common:" + configInfo['Common'])
        CommonTree = ET.parse(configInfo['Common'])
        CommonRoot = CommonTree.getroot()
    else:
        print('# Common path issue, check config file and type the correct Common.py path.')

    if len(configInfo['URL']) > 0:
        print("http://" + configInfo['URL'])
        StringDric['URL'] = configInfo['URL']
    else:
        print('# URL Address issue, check config file and type the correct url address.')

    if not os.path.exists(configInfo['OutputPath']):
        os.makedirs(configInfo['OutputPath'])

    for caseFile in os.listdir(configInfo['ScriptPath']):  # 从config file中获取scriptPath然后遍历里面所有的文件
        if analyzxml(configInfo['ScriptPath'] + '\\' + caseFile, configInfo['OutputPath']):
            print('*' * 20)
            trueprint(caseFile + ' is passed')
            print('*' * 20)
        else:
            print('*' * 20)
            falseprint(caseFile + ' is failed')
            status.append(caseFile)
            print('*' * 20)
    if status:
        print('Below case has been analy failed')
        print(status)
