import logging
import xml.etree.cElementTree as ET

if __name__ == '__main__':
    root = ET.parse(r'../XMLs/ScenarioStorageV1.xml').getroot() # [@PageName = "LoginPage"]/Scenario[@ScenarioName = "SelectLanguage"]/action
    i = 1
    for page in root:
        for scenario in page:
            action = scenario.find('action')
            if action.items():
                actiontag = ET.Element('action')
                scenario.remove(action)
                action.tag = 'step'
                actiontag.append(action)
                scenario.append(actiontag)
                i += 1
    print(i)
    ET.ElementTree(root).write('text.xml')