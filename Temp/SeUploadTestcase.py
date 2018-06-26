from selenium import webdriver
import simplifyAutomation


def getData(path=r"C:\Users\chui\Desktop\R1_Search for products_No Search Results.xlsx"):
    test = simplifyAutomation.exceltoscript(path)
    a, b = test.popitem()
    return b[1]

def main():
    driver = webdriver.Firefox()
    driver.implicitly_wait(15)
    driver.get('http://192.168.1.42:8001')
    driver.maximize_window()
    path = r"C:\Users\chui\Desktop\No_Data\R1.1_Configurations and Bundles_Bundle with Options_Price based on configuration.xlsx"
    casename = path.split('\\')[-1][:-5]

    data = getData(path)
    print(data)

    driver.find_element_by_xpath('//input[@id="title"]').send_keys(casename)
    driver.find_element_by_xpath('//input[@value="搜索"]').click()

    driver.find_element_by_xpath('//div[@title="编辑"]').click()
    # {}.items()
    for key, value in data.items():
        num, page, scenario = key.split('_')

        driver.find_element_by_xpath('//li[@id="scenario%s"]' % num).click()
        driver.find_element_by_xpath('//a[text()="编辑"]').click()

        datakey, value = value.popitem()
        if datakey == '' or value == '':
            print(key)
            continue
        assert datakey != ''
        assert value != ''
        try:
            valueinput = driver.find_element_by_xpath('//input[@value="$%s"]' % datakey)
        except:
            print(key, value, ' cannot inputed')
            continue
        valueinput.clear()
        valueinput.send_keys(value)
        driver.find_element_by_xpath('//a[text()="保存"]').click()
    driver.find_element_by_xpath('//input[@value="发布"]').click()
    driver.switch_to.alert.accept()
    driver.find_element_by_xpath('//a[text()="用例"]').click()
    # print(data)

if __name__ == '__main__':
    main()