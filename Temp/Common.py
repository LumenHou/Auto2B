__author__ = 'Innovation'
# -*- coding: utf-8 -*-

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
from selenium.webdriver.common.action_chains import *
from selenium import webdriver
from time import sleep
import time
import xlsxwriter
import os, sys
import logging
from selenium.webdriver.support.ui import Select
from PIL import Image, ImageGrab
import io
import numpy as np
import shutil
import string
import Temp.simplifyAutomation as simplifyAutomation
import threading
import datetime
import xml.etree.cElementTree as ET


class Common:
    scenario = 0
    checkpoint = {}
    thred = []
    scenariostorage = ET.parse(r'../XMLs/ScenarioStorageV1.xml')

    def __init__(self, casename, driver):
        self.casename = casename
        self.driver = driver
        self.driver.implicitly_wait(15)
        self.driver.maximize_window()
        self.outputpath = self.casename + "_" + time.strftime("%Y%m%d")
        if not os.path.exists(self.outputpath):
            os.mkdir(self.outputpath)
        self.begin = datetime.datetime.now()
        self.pagescreen = {}
        self.reportresult = {}

    def screenshot_window(self, arg1, arg2):
        thed = threading.Thread(target=self.screenshot_window2, args=(arg1, arg2,))
        thed.setDaemon(True)
        thed.start()
        sleep(2)
        # thed.join()
        self.thred.append(thed)


    # Screen Shot
    def screenshot_window2(self, group, screenname):
        num, pagename, scenario = group.split('_')
        # sleep(5)
        self.log('In Screenshot method')
        # nowTime1 = time.strftime("%Y%m%d")
        filepath = self.outputpath
        screenname = screenname + '_' + num

        # self.driver.get_screenshot_as_file(filepath + "/" + screenname + ".png")
        pic = ImageGrab.grab()
        pic.save(filepath + "/" + screenname + ".png")
        self.log(screenname + '.png' + ' is captured')
        # self.reportresult.append([self.casename, filepath + "/" + screenname + ".png", nowTime1])
        if group in self.reportresult.keys():
            temp = self.reportresult[group]
            temp.append(filepath + "/" + screenname + ".png")
            self.reportresult[group] = temp
        else:
            self.reportresult[group] = [filepath + "/" + screenname + ".png"]

    # 网页元素高亮
    def highlight_element(self, element):
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element,
                                   "border:2px solid red;")
        # self.log(element + ' has been highlight')
        time.sleep(1)

    def movetoelement(self, type, key):
        element = self.find_element(type, key)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)

    def movecursor(self, type, key):
        #Simulate mouse actions
        element = self.find_element(type, key)
        chains = ActionChains(self.driver)
        chains.move_to_element(element).perform()
        time.sleep(1)

    def wait(self, value):
        sleep(int(value))
        self.log('The process is sleeping for ' + value +' s')

    def back(self):
        self.driver.back()
        self.log('screen is back to the previous page')

    def close(self):
        self.driver.close()
        self.log('The window is closed')

    def NewURL(self, value):
        self.driver.get(value)
        self.log('The website is opened')

    def Window_size(self, value):
        if value == "Max":
            self.driver.maximize_window()
            self.log('The window is maximized')
        elif value == "Min":
            self.driver.set_window_size(400, 600)
            self.log('The window is small down')

    def Switch_window(self):
        h1 = self.driver.current_window_handle
        all_h = self.driver.window_handles
        for i in all_h:
            if i != h1:
                self.driver.switch_to.window(i)

    # 网页全屏截图
    def screenshot_page(self, group, screenname):
        sleep(5)
        num, pagename, scenario = group.split('_')
        screenname = screenname + '_' + num
        driver = self.driver
        filepath = self.outputpath

        page_height = driver.execute_script("return document.body.scrollHeight")  # 获取JS返回值为当前页面高度
        down = True
        while down:
            sleep(2)
            tempheight = driver.execute_script("return document.body.scrollHeight")
            if page_height == tempheight:
                down = False
            else:
                page_height = tempheight
        del down
        self.log('PageHight is ' + str(page_height))
        time.sleep(2)
        page_width = driver.execute_script("return document.body.scrollWidth")  # 获取JS返回值为当前页面宽度
        self.log('PageWidth is ' + str(page_width))

        time.sleep(2)

        if not os.path.exists(filepath):
            os.mkdir(filepath)
            self.log(filepath + ' is created')

        # 滚动到页面顶部
        js = "var q=document.documentElement.scrollTop=0"
        self.js_execution(js)
        time.sleep(2)

        # 截取当前第一张页面并且存储到内存变量basemat
        png = driver.get_screenshot_as_png()
        img_buffer = io.BytesIO(png)
        img1 = Image.open(img_buffer)
        width, height = img1.size
        window_height = height  # 将截取的第一屏幕高度赋给变量

        basemat = np.atleast_2d(img1)

        # 滚动截图
        scroll_number = page_height // window_height

        for i in range(scroll_number):
            scroll_height = window_height * i

            js = "var q=document.documentElement.scrollTop=" + str(scroll_height)
            self.js_execution(js)
            time.sleep(2)

            if i == 0:
                continue
            png = driver.get_screenshot_as_png()
            img_buffer = io.BytesIO(png)
            img2 = Image.open(img_buffer)
            mat = np.atleast_2d(img2)
            basemat = np.append(basemat, mat, axis=0)
            time.sleep(1)

        # 如果不是整数，截取最后一张屏并且截取Rangle某部分
        if (page_height % window_height) != 0:

            a = (page_height - (page_height // window_height) * window_height)  # 最后剩余部分

            # 定义最后一块截图区域
            left = 0
            right = page_width
            upper = window_height - a
            lower = window_height

            rangle = (left, upper, right, lower)

            # 滚动最后一次并截取最后一屏
            js = "var q=document.documentElement.scrollTop=" + str((window_height) * (scroll_number))
            self.js_execution(js)
            time.sleep(2)

            # 截取尾部图片
            temppng = driver.get_screenshot_as_png()
            temp_ori = Image.open(io.BytesIO(temppng))
            temp_crop = temp_ori.crop(rangle)

            # 完成拼接
            mat = np.atleast_2d(temp_crop)
            basemat = np.append(basemat, mat, axis=0)
            # time.sleep(1)

            # 输出最后拼接完成的图片
            Image.fromarray(basemat).save(filepath + "/" + screenname + ".png")

        else:
            # 恰好整除的话不用截取尾部图片，直接输出图片
            Image.fromarray(basemat).save(filepath + "/" + screenname + ".png")

        self.log(screenname + ".png is captrued")
        # self.reportresult.append([self.casename, filepath + "/" + screenname + ".png", nowTime1])
        if group in self.pagescreen.keys():
            temp = self.pagescreen[group]
            temp.append(filepath + "/" + screenname + ".png")
            self.pagescreen[group] = temp
        else:
            self.pagescreen[group] = [filepath + "/" + screenname + ".png"]

    # Wait Element
    def waitelement(self, function, keys):
        locatorMethod = {'xpath': By.XPATH, 'id': By.ID, 'name': By.NAME, 'css': By.CSS_SELECTOR,
                         'class': By.CLASS_NAME}
        try:
            locator = (locatorMethod[function], keys)
            WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located(locator))
            return True
        except:
            return False

    # Key Board Action
    def keyboard(self, type, keys, value):
        keyboardmethod = {'ENTER': Keys.ENTER, 'SHIFT': Keys.SHIFT, 'CONTROL': Keys.CONTROL, 'DELETE': Keys.DELETE,
                          'SelectAll': (Keys.CONTROL, 'a'), 'BACKSPACE': Keys.BACK_SPACE, 'OpenTab': (Keys.CONTROL, 't'),
                          'CloseTab': (Keys.CONTROL, 'w')}
        self.find_element(type, keys).send_keys(keyboardmethod[value])
        self.log(value + ' is clicked')

    # Check box
    # keys: 被操作checkbox的id
    # status： checkbox所需的勾选状态
    def checkbox_comm(self, keys, status):
        # status: true|false
        # print('321')
        js = "var el = document.getElementById('" + keys + "');el.checked = " + status + ";"
        self.js_execution(js)
        self.log(keys + ' checkbox is ' + status)

    def tableSelect(self, value):
        td = self.driver.find_elements_by_xpath('//td[contains(@id,"text")]')
        for tr in td:
            if tr.text == value:
                tr.click()

    # keys：滚动距离
    def scroll_comm(self, keys):
        sleep(3)
        js = "var q=document.documentElement.scrollTop=" + keys
        self.js_execution(js)
        sleep(0.5)
        self.log('Page has Scroll down:' + keys)

    # js: 需要被执行的js语句
    def js_execution(self, js):
        self.driver.execute_script(js)
        self.log('"' + js + '" executed')

    # option: 下拉菜单中的选项
    def dropdown(self, type, keys, option):
        s1 = Select(self.find_element(type, keys))
        s1.select_by_visible_text(option)
        self.log(option + 'is selected on ' + keys + ' dropdown.')

    # function: 定位元素的方式
    # keys：定位元素所需的值
    def find_element(self, type, keys):
        # tyep: {id, xpath, name, class, css_selector}
        func = getattr(self.driver, 'find_element_by_' + type)
        e = None
        try:  # 修复log中没找到元素却会输出找到的log信息
            e = func(keys)
            self.highlight_element(e)
            # self.movetoelement(e)
            self.log(keys + ' element is found by ' + type + ' method.')
        except:
            self.log(keys + ' element is not found by ' + type + ' method.')
        return e
        # elif type == 'css':
        #    return driver.find_element_by_css_selector(keys)

    # function: 定位元素的方式
    # keys：定位元素所需的值
    def find_elements(self, type, keys):
        func = getattr(self.driver, 'find_elements_by_' + type)
        e = None
        try:  # 修复log中没找到元素却会输出找到的log信息
            e = func(keys)
            self.highlight_element(e)
            self.log(keys + ' element is found by ' + type + ' method.')
        except:
            self.log(keys + ' element is not found by ' + type + ' method.')
        return e

    # Switch to iframe
    def switchtoframe(self, type, keys):
        self.driver.switch_to.frame(self.find_element(type, keys))
        sleep(5)
        self.log(keys + ' iframe is switched')

    # Switch back
    def swithback(self):
        self.driver.switch_to.default_content()
        self.log('screen is switch to default content')
        # driver.switch_to.parent_frame()

    # Common Input
    def input_comm(self, type, keys, value):
        if value == "clear":
            self.find_element(type, keys).clear()
            self.log('textbox is clear on ')
        else:
            self.find_element(type, keys).send_keys(value)
            self.log(value + ' is inputed on ')

    # Common Click
    def click_comm(self, type, *keys):
        if '' == keys[1]:
            key = keys[0]
        else:
            key = string.Template(keys[0]).safe_substitute({'value': keys[1]})
        self.find_element(type, key).click()
        self.log(key + ' is clicked')

    def report(self):
        # print(self.thred)
        # print(self.pagescreen)
        # print(self.reportresult)
        for t in self.thred:
            if t.is_alive():
                t.join()
                # print(t.is_alive())
        workbook = xlsxwriter.Workbook(self.casename + '.xlsx')
        worksheet = workbook.add_worksheet('Test Result')
        bold = workbook.add_format({'bold': True, 'border': 1})
        worksheet.write("A1", "Step No.", bold)
        worksheet.write("B1", "PageName", bold)
        worksheet.set_column('B:C', 15)
        worksheet.write("C1", "Scenario", bold)
        worksheet.write("D1", "Step Description", bold)
        worksheet.write("E1", "Expected Result ", bold)
        worksheet.set_column('D:E', 50)
        worksheet.write("F1", "CheckPoint", bold)
        worksheet.set_column('F:F', 30)
        worksheet.write("G1", "WindowScreen", bold)
        worksheet.write("H1", "PageScreen", bold)
        worksheet.set_column('G:H', 13)
        worksheet.write("I1", "Status", bold)
        worksheet.write("J1", "Comments", bold)
        worksheet.set_column('J:J', 30)

        bold = workbook.add_format({'text_h_align': 2, 'border': 1, 'text_v_align': 2})
        textWrap = workbook.add_format({'text_wrap': True, 'border': 1})

        row = 1
        for checkpoint in self.checkpoint.keys():
            startrow = row
            isnot = False
            screenlist = None
            pagesceenlist = None
            pageisnot = False
            num, page, scenario = checkpoint.split('_')
            if checkpoint in self.reportresult.keys():
                screenlist = self.reportresult[checkpoint]
                isnot = True
            if checkpoint in self.pagescreen.keys():
                pagesceenlist = self.pagescreen[checkpoint]
                pageisnot = True
            worksheet.write(row, 0, num, bold)  # A2
            worksheet.write(row, 1, page, bold)
            worksheet.write(row, 2, scenario, bold)
            worksheet.write(row, 5, self.checkpoint[checkpoint], bold)
            Scenarioscript = self.scenariostorage.find('./Page[@PageName="' + page + '"]/Scenario[@ScenarioName="' + scenario + '"]/script')
            if Scenarioscript is None:
                print('./' + page + '/' + scenario + '/script: is not find in ScenarioStorage file')
                sys.exit(1)
            for xmlobj in Scenarioscript:
                # print(xmlobj.attrib)
                worksheet.write(row, 3, xmlobj.attrib['description'], textWrap)
                worksheet.write(row, 4, xmlobj.attrib['result'], textWrap)
                worksheet.write(row, 8, 'NoRun', bold)
                worksheet.data_validation('I' + str(row), {'validate': 'list',
                                                           'source': ['Pass', 'Block', 'Failed', 'NoRun']})
                worksheet.write(row, 9, '', bold)

                if screenlist and isnot:
                    screenname = screenlist[0].split('/')
                    screen = screenname[-1:][0]
                    worksheet.write_url(row, 6, screen)
                    del screenlist[0]
                else:
                    worksheet.write_blank(row, 6, '', bold)
                if pagesceenlist and pageisnot:
                    pagesceenname = pagesceenlist[0].split('/')
                    pagepath = pagesceenname[-1:][0]
                    worksheet.write_url(row, 7, pagepath)
                    del pagesceenlist[0]
                else:
                    worksheet.write_blank(row, 7, '', bold)
                row += 1
            if row != startrow + 1:
                worksheet.merge_range(startrow, 0, row - 1, 0, num, bold)
                worksheet.merge_range(startrow, 1, row - 1, 1, page, bold)
                worksheet.merge_range(startrow, 2, row - 1, 2, scenario, bold)
                bold.set_text_wrap()
                worksheet.merge_range(startrow, 5, row - 1, 5, self.checkpoint[checkpoint], bold)
        workbook.close()
        self.log('Report is created')
        self.log(datetime.datetime.now() - self.begin)
        # self.log('The related log&Report is moved to output folder')
        filenames = self.casename.split('/')
        filename = filenames[-1:][0]
        if os.path.exists(self.outputpath + '/' + filename + '.xlsx'):
            # print('true')
            os.remove(self.outputpath + '/' + filename + '.xlsx')
        if os.path.exists(self.outputpath + '/' + filename + '.log'):
            # print('true')
            os.remove(self.outputpath + '/' + filename + '.log')
        shutil.move(self.casename + '.xlsx', self.outputpath)
        shutil.move(self.casename + '.log', self.outputpath)
        print('The related log&Report is moved to output folder')

    def log(self, message):
        # create a logger
        logger = logging.getLogger(self.casename)
        logger.setLevel(logging.DEBUG)

        # Create a handler for input log information
        filename = self.casename + '.log'
        fh = logging.FileHandler(filename)
        fh.setLevel(logging.DEBUG)

        # Create a handler for the output to the console
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Define the handler output format
        formatter = logging.Formatter('[%(asctime)s]-[%(module)s-%(funcName)s]:%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add a handler to the logger

        logger.addHandler(fh)
        logger.addHandler(ch)

        # Add a log
        logger.info(message)
        # Remove Handler
        logger.removeHandler(fh)
        logger.removeHandler(ch)


if __name__ == '__main__':
    # common = Common('', webdriver.Firefox())
    from collections import OrderedDict

    # dict = {'server':"aaaa",'aaa':"bbbb",'ccc':"no"}
    # print(dict.keys())
    # ScenarioScript = simplifyAutomation.pagescrnariomapping('XMLs/Scenario_Temp.xml')
    print(os.path.exists('Output/Catalog Selection Unavailable_20171129/Catalog Selection Unavailable.xlsx'))
    casename = 'C:/Users/chui/Documents/myproject/Output/Catalog Selection Unavailable.py'
    filenames = casename.split('/')
    filename = filenames[-1:]
    print(filename)
