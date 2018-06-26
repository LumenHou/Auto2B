import xlrd
import FindValue

if __name__ == '__main__':
    excelscript = xlrd.open_workbook(r"C:\Users\chui\Desktop\LumenResultData.xlsx")
    sheets = excelscript.sheets()
    # sheet
    for sheet in sheets:
        if sheet.name == 'Summary':
            continue
        rows = sheet.nrows
        for row in range(1, rows):
            pagename = sheet.cell(row, 1).value
            scenario = sheet.cell(row, 2).value
            value = FindValue.findvalue(pagename, scenario)
            if value == '':
                continue
            else:
                print(value)
                sheet.cell(row, 4).value = value