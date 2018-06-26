# -*- coding: utf-8 -*-

import xlrd
import os
import shutil


def getname(excelpath):
    excelscript = xlrd.open_workbook(excelpath)
    sheets = excelscript.sheets()
    passrows = []
    copyrows =[]
    for sheet in sheets:
        rows = sheet.nrows
        for row in range(1, rows):
            scriptName = sheet.cell(row, 2).value
            status = sheet.cell(row, 5).value
            link = sheet.cell(row, 6).value
            if status == 'Pass':
                passrows.append(row)
                if '\\' in link:
                    case = link.split('\\')[-1:]
                    path = r'\\192.168.1.42\06_Automation\06.04_HP2B Automation\ScriptRunning\Final Run Automation Result' + '\\' + case[0] + '\Input'
                    if os.path.exists(path):
                        copyrows.append(row)
                        copyto(path, scriptName)
                    else:
                        path = r'\\192.168.1.42\06_Automation\06.04_HP2B Automation\ScriptRunning\Result' + '\\' + case[0] + '\Input'
                        if os.path.exists(path):
                            copyrows.append(row)
                            copyto(path, scriptName)
                        else:
                            print(path + 'error')
                else:
                    path = r'\\192.168.1.42\06_Automation\06.04_HP2B Automation\ScriptRunning\Final Run Automation Result' + '\\' + link + '\Input'
                    if os.path.exists(path):
                        copyrows.append(row)
                        copyto(path, scriptName)
                    else:
                        path = r'\\192.168.1.42\06_Automation\06.04_HP2B Automation\ScriptRunning\Result' + '\\' + link + '\Input'
                        if os.path.exists(path):
                            copyrows.append(row)
                            copyto(path, scriptName)
                        else:
                            print(path + 'error')
    print([i for i in passrows if i not in copyrows])
    # print(len(copyrows))



def copyto(path, name):
    if os.path.exists(path):
        files = os.listdir(path)
        # a = False
        for file in files:
            if file.endswith('.xlsx'):
                # a = True
                src = path + '\\' + file
                new = r'C:\Users\chui\Desktop\Automation Test Case' + '\\' + file
                # if os.path.exists(new):
                # print(name)
                shutil.copy(src, new)
                name = r'C:\Users\chui\Desktop\Automation Test Case' + '\\' + name + '.xlsx'
                os.rename(new, name)
                #print(file)
        # if not a:
        #     print(path)
    else:
        print('Error:' + path)


if __name__ == '__main__':
    getname(r"C:\Users\chui\Desktop\Automation Script Tracking Task Assign.xlsx")
