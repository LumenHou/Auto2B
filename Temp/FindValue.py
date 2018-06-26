import xml.etree.cElementTree as ET
import sys

def findvalue(pagename, scenarioname, defalut=''):
    root = ET.parse(r'XMLs/ScenarioStorageV1.xml').getroot()
    action = root.find('./Page[@PageName="' + pagename + '"]/Scenario[@ScenarioName="' + scenarioname + '"]/action')
    if action is None:
        print('The Page:%s or Scenario:%s is not in ScenarioStorageV1.xml' % (pagename, scenarioname))
        sys.exit(1)
    for step in action:
        if 'value' in step.attrib:
            if '$' in step.attrib['value']:
                # print(step.attrib['value'])
                defalut = step.attrib['value'][1:]
        else:
            print('No Value in this scenario')
    return defalut

if __name__ == '__main__':
    pagename = input('PageName:')
    scenarioname = input("ScenarioName:")

    print(findvalue(pagename, scenarioname))