__author__ = 'Lumen'
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import simplifyAutomation
import xlrd


def test():
    action = simplifyAutomation.pagescrnariomapping(r'XMLs/Temp.xml')
    script = simplifyAutomation.pagescrnariomapping(r'XMLs/Tracy.xml')

    NewElement = ET.Element('Scripts')

    # action['LoginPage']['ChangeLanguage'].tag = 'action'
    for page in action:
        Epage = ET.Element(page)
        NewElement.append(Epage)
        # print(page)
        for scenario in action[page]:
            # print(scenario)
            Escenario = ET.Element(scenario)
            action[page][scenario].tag = 'action'
            action[page][scenario].attrib = {}
            Escenario.append(action[page][scenario])
            try:
                script[page][scenario].tag = 'script'
                script[page][scenario].attrib = {}
                Escenario.append(script[page][scenario])
            except:
                print(page + ' ' + scenario + ' is no have script')
            Epage.append(Escenario)
    ET.ElementTree(NewElement).write(r'XMLs/ScenarioStorage.xml')
    # ET.parse(r'XMLs/lumen.xml')


def test2():
    scenarioexcel = xlrd.open_workbook(r'C:\Users\chui\Desktop\Total.xlsx')
    firstsheet = scenarioexcel.sheets()[0]
    rows = firstsheet.nrows
    result = {}
    # {Pagename: {Senario: descript}}
    for row in range(1, rows):
        pagename = firstsheet.cell(row, 1).value  # B2.value pageName
        scenarioname = firstsheet.cell(row, 2).value  # C2.value ScenarioName
        description = firstsheet.cell(row, 3).value  # D2.value description
        temp = {}
        if pagename in result.keys():
            temp = result[pagename]
        else:
            result[pagename] = temp

        if scenarioname in temp.keys():
            continue
        else:
            temp[scenarioname] = description
    # print(result.__len__())
    Eall = ET.Element('Script')
    for page in result.keys():
        Epage = ET.Element(page)
        Eall.append(Epage)
        for scenario in result[page].keys():
            # if '&' in scenario:
            #   Tscenario = scenario.replace('&','_')
            Escenario = ET.Element(scenario.replace('&', '_'))
            Epage.append(Escenario)
            Edes = ET.Element('Desription', attrib={'value': result[page][scenario]})
            Escenario.append(Edes)
    ET.ElementTree(Eall).write('temp.xml')


if __name__ == '__main__':
    import xlsxwriter

    scenarioexcel = xlrd.open_workbook(r'C:\Users\chui\Desktop\NewAddScenario.xlsx')
    firstsheet = scenarioexcel.sheets()[0]
    rows = firstsheet.nrows
    result = {}
    # {Pagename: {Senario: descript}}
    for row in range(1, rows):
        pagename = firstsheet.cell(row, 1).value  # B2.value pageName
        print(pagename)
        scenarioname = firstsheet.cell(row, 2).value  # C2.value ScenarioName
        # description = firstsheet.cell(row, 3).value  # D2.value description
        step = firstsheet.cell(row, 3).value
        sresult = firstsheet.cell(row, 4).value
        temp = {}
        if pagename in result.keys():
            temp = result[pagename]
        else:
            result[pagename] = temp

        if scenarioname in temp.keys():
            continue
        else:
            temp[scenarioname] = ['', step, sresult]

    Eall = ET.Element('Script')
    for page in result.keys():
        Epage = ET.Element('Page', attrib={'PageName': page})
        Eall.append(Epage)
        for scenario in result[page].keys():
            # if '&' in scenario:
            #   Tscenario = scenario.replace('&','_')
            temp = result[page][scenario]
            Escenario = ET.Element('Scenario', attrib={'ScenarioName': scenario.replace(' ', '')})
            Epage.append(Escenario)
            Edes = ET.Element('action')
            ESete = ET.Element('step', attrib={'action': '', 'type':"", 'keys': ''})
            Edes.append(ESete)
            Escenario.append(Edes)
            Estep = ET.Element('script')
            Escenario.append(Estep)
            Edescript = ET.Element('StepResult', attrib={'description': temp[1], 'result': temp[2]})
            Estep.append(Edescript)
            EScenDes = ET.Element('ScenarioDescript', attrib={'Des': temp[0]})
            Escenario.append(EScenDes)
    ET.ElementTree(Eall).write('temp.xml')

    # # print(result['AddUserPage'])
    # workbook = xlsxwriter.Workbook('test.xlsx')
    # titelformat = workbook.add_format(
    #     {'font_name': 'Calibri', 'border': 1, 'font_size': 10, 'bg_color': '#000080', 'font_color': 'white'})
    # cellformat = workbook.add_format({'font_name': 'Calibri', 'border': 1, 'font_size': 10})
    # summarysheet = workbook.add_worksheet('Summary')
    # summarysheet.write("A1", 'Page', titelformat)
    # summarysheet.set_column('A:A', 25)
    # summarysheet.write("B1", "Link", titelformat)
    # summarysheet.set_column('B:B', 25)
    # summarysheet.write("C1", "No.", titelformat)
    # summarysheet.write("D1", "Owner", titelformat)
    # summarysheet.write("E1", "Page Description", titelformat)
    # startrow = 1
    # for pagename in result.keys():
    #     summarysheet.write(startrow, 0, pagename, cellformat)
    #     summarysheet.write_url(startrow, 1, 'internal:' + pagename + '!A1')
    #     summarysheet.write(startrow, 2, len(result[pagename]), cellformat)
    #     startrow += 1
    # del startrow
    # for pagename in result.keys():
    #     startrow = 1
    #     pageSheet = workbook.add_worksheet(pagename)
    #     pageSheet.write("A1", 'Page', titelformat)
    #     pageSheet.set_column('A:A', 12)
    #     pageSheet.write("B1", "Scenario", titelformat)
    #     pageSheet.set_column('B:B', 30)
    #     pageSheet.write("C1", "Scenario Description", titelformat)
    #     pageSheet.set_column('C:C', 55)
    #     pageSheet.write("D1", "Step", titelformat)
    #     pageSheet.set_column('D:D', 30)
    #     pageSheet.write("E1", "Result", titelformat)
    #     pageSheet.set_column('E:E', 55)
    #     pageSheet.write_url("F1", 'internal:Summary!A1')
    #     for scenario in result[pagename].keys():
    #         temp = result[pagename][scenario]
    #         pageSheet.write(startrow, 0, pagename, cellformat)
    #         pageSheet.write(startrow, 1, scenario, cellformat)
    #         pageSheet.write(startrow, 2, temp[0], cellformat)
    #         pageSheet.write(startrow, 3, temp[1], cellformat)
    #         pageSheet.write(startrow, 4, temp[2], cellformat)
    #         pageSheet.write(startrow, 5, 'NoStart', cellformat)
    #         pageSheet.data_validation('F' + str(startrow+1), {'validate': 'list',
    #                                                         'source': ['NoStart', 'OnGoing', 'Block', 'Pass']})
    #         startrow += 1
    #
    # workbook.close()
