__author__ = 'Innovation'
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from time import sleep
import time
import datetime
import sys
import os
from PIL import ImageGrab
ScreenIDList = []
numscreenshot = [0]
logPath = []
imgList = []
caseResult = []


# 声明webdriver.Firefox()
driver = webdriver.Firefox()
driver.implicitly_wait(15)
driver.get('https://live.itg3.hp2b.hp.com')
driver.maximize_window()

# 登录
driver.find_element_by_name('logonId1').send_keys('EMEA.DE.rwe.admin.1@ppsdns.com')
driver.find_element_by_name('logonPassword').send_keys('Wcsadmin1')
driver.find_element_by_xpath("//div[@class='button_align']/a").click()
sleep(5)

# 等待iframe跳出

locator = (By.XPATH, '/html/body/div[20]/div/iframe')
try:
    WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))
    iframe = driver.find_element_by_xpath('/html/body/div[20]/div/iframe')
    driver.switch_to.frame(iframe)
    sleep(2)
    driver.find_element_by_xpath("/html/body/div[2]/div[2]/div[1]/div[1]/button").click()
    driver.switch_to.default_content()
except:
    print ("请求超时")
    driver.close()


# Search,输入Product ID
driver.find_element_by_name("searchTerm").send_keys("E4H3")
driver.find_element_by_xpath("/html/body/div[8]/div[2]/div/div[2]/div/div[2]/form/a").click()

# 点击C9943B的add to cart button
productlistingpage = driver.find_elements_by_class_name('product_listing_container')
for productlist in productlistingpage:
    prolist = productlist.find_elements_by_tag_name('li')
    for product in prolist:
        details = product.find_element_by_xpath('div/div[3]/div[1]/span')
        print(details.text)
        if details.text == 'C9943B':
            product.find_element_by_xpath('//*[@class="product-tile-cta"]/a').click()
#a2c = add2cart[0].find_element_by_tag_name('a')
#a2c.click()
#print(add2cart[0].find_elements_by_tag_name('a'))
# 模糊查询所有的add2cart button
print(driver.find_elements_by_xpath("//a[starts-with(@id, 'add2CartBtn')]").__len__())
driver.find_element_by_class_name('')


# Change Catalog
driver.find_element_by_class_name('company-info').click()
driver.find_element_by_xpath('//table[@id="selectedContractId"]').send_keys(Keys.DOWN)
td = driver.find_elements_by_xpath('//div[@id="selectedContractId_menu"]//td[contains(@id,"text")]')
for contract in td:
    if contract.text == 'Surcharge,  Testing':
        contract.click()
driver.find_element_by_xpath('//button[text()="Apply"]').click()
driver.find_element_by_xpath('//div[@class="widget_quick_info_popup"]//div[text()="OK"]').click()

# PDP optionCode
driver.find_element_by_xpath('//table[contains(@id, "attrValue_Option Code_entitledItem")]').click()
td = driver.find_elements_by_xpath('//td[contains(@id,"text")]')
for tr in td:
    print(tr.text)

# compare
driver.find_elements(By.XPATH,'//label[starts-with(@for, "comparebox")]').__len__()
driver.find_element_by_xpath('//div[starts-with(@id, "compare")]/a').click()
# driver.find_element_by_id('dijit_MenuItem_0').text

#
driver.find_element(By.XPATH, '//input[starts-with(@id, "quantity")]').clear()
driver.find_element_by_xpath('//div[@class="tab_header tab_header_double"]/div[3]')

driver.find_element_by_xpath("//a[starts-with(@id, 'expClose')]")



driver.find_element_by_xpath('//ul[@class="facetSelect"]/li/a[text()="Personal information"]')
driver.find_element_by_xpath('//div[@class="shopper-actions"]//button | //div[@class="shopper-actions"]//a').click()
driver.find_element_by_xpath('//div[@class="definingAttributes"]//div[starts-with(@id,"usedFilterRemove")]')


sleep(8)
driver.find_element_by_id('add2CartBtn_3074457345617692165').click()
sleep(4)
driver.find_element_by_id('GotoCartButton2').click()
sleep(5)
driver.find_element_by_id('checkout_button').click()
sleep(5)

# check out page
driver.find_element_by_xpath("//*[@id='partnerAgent']").send_keys('TestPartnerAgent')
driver.find_element_by_xpath('//*[@id="purchase_order_name"]').send_keys('PO Name1')
driver.find_element_by_xpath('//*[@id="purchase_order_num"]').send_keys('PO Number1')
driver.find_element_by_xpath('/html/body/div[7]/div[5]/div/div/div/div[6]/div[5]/div/div[2]/table/tbody/tr[6]/td/div/label').click()
handles = driver.window_handles
# 点击T&C Check box
if handles[1]:
    driver.switch_to.window(handles[1])
    driver.find_element_by_xpath('/html/body').click()
    driver.close()
    driver.switch_to.window(handles[0])

# Click submit order button
driver.find_element_by_xpath("//*[@id='submitOrder']").click()


#CSR im user
driver.find_element_by_xpath('//div[@id="csrSearchBar"]/a/div').click()
driver.find_element_by_xpath('//form[@id="RegisteredCustomersSearch_searchForm"]//input[contains(@id, "logonId")]').send_keys('123')
driver.find_element_by_id("RegisteredCustomersList_form_botton_1").click()
driver.find_element_by_class_name('dropdown-button')
driver.find_element_by_xpath('//ul[contains(@class, "dropdown-items")]/div[@class="actionItem"]/div').click()

driver.find_element_by_xpath('//div[@class="shopper-actions"]//a[starts-with(@id, "customizeBtn")]')

driver.find_element_by_xpath('//input[contains(@id, "quantity")]').send_keys('2')
driver.find_element_by_xpath('').send_keys('2')
driver.find_element_by_xpath("//ul[@id='departmentsMenu']/li[2]/a")

driver.find_element_by_id('footerWebRequestLink')
driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", driver.find_element_by_id('footerWebRequestLink'),
                                   "border:2px solid red;")
driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_id('submitButton_ACCE_Label'))

driver.find_element_by_xpath('//*[@class="scroll-container"]')
driver.find_element_by_xpath('//ul[@class="facetSelect"]/li/a[text()="Favorites"]')
driver.find_element_by_xpath('//div[@class="scroll-container"]//tr[3]/td')

driver.switch_to.frame(driver.find_element_by_id('configuratorFrame'))

driver.find_element_by_xpath('//*[@class = "custom-dropdown-select"]') # @id="WC_UserDetails_Form_Input_PRIMARYJOBRESPONSIBILITY"
driver.find_element_by_xpath('//div[@class="product-tile-cta"]//button | //div[@class="product-tile-cta"]//a')
driver.find_elements_by_xpath('//a[contains(@id, "SignOut")]')
driver.find_elements_by_id('WC_AdvancedSearchForm_FormInput_searchType')

chains = ActionChains(driver)
chains.move_by_offset(0,0).click().perform()

driver.execute_script('return document.readyState')
#