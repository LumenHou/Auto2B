__author__ = 'Lumen'
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import selenium.webdriver.support.expected_conditions as EC

import time, os, xlsxwriter, logging, io, shutil, string, threading, datetime, configparser
from PIL import Image  # , ImageGrab
import numpy as np
import xml.etree.cElementTree as ET

import Temp.client as client
# ini xpath存放文件的路径
# beanLogger logger对象
iniFileURL = "XMLs/ElementResult.ini"
beanLogger = logging.getLogger()


def logger(func):
    """
    :param func: 装饰器
    :return: NUll
    当初设想使用装饰器来实现log, 但是未尝试成功, 后搁置
    """

    def tmp(*args, **kargs):
        beanLogger.info('Start %s(%s, %s)...' % (func.__name__, args, kargs))
        return func(*args, **kargs)

    return tmp


class step:
    """
    # class step, 来保存每一步操作的对象(xml中每一个step标签就会解析为一个step对象)
    # actionFcun来保存xml中属性值对应的方法名, 直接来通过反省获取应执行的funcName
    # noElementlist 来保存不需要操作elemetn的一些方法名
    # screenshot方法, 会返回一个单元素list: [screenshot path], 然后scenario对象来保存所有的截图结果
    """
    actionFunc = {'click': 'click_comm', 'input': 'input_comm', 'switch_to': 'switchtoframe',
                  'screenshot': 'screenshot_window', 'pagescreen': 'screenshot_page', 'check': 'checkbox_comm',
                  'press': 'keyboard', 'scroll': 'scroll_comm', 'select': 'dropdown', 'tableSelect': 'tableSelect',
                  'find': 'find_element', 'movecursor': 'movecursor', 'viewmove': 'movetoelement',
                  'switch_default': 'swithback', 'sleep': 'sleep', 'clickblank': 'clickblank', 'browserBack': 'back'}
    noElementlist = ['switch_default', 'tableSelect', 'scroll', 'pagescreen', 'screenshot', 'sleep', 'clickblank',
                     'browserBack']

    def __init__(self):
        self.action = None
        self.key = None
        self.value = None
        self.type = None
        self.element = None
        # 当遇到需要操作元素的action时, 会找到相应元素并保存在这里
        self.parent = None
        # 父Scenario对象
        self.index = 0
        # 在Scenario中的顺序

    def setpageobj(self, value):
        self.action = 'pagescreen'
        self.value = value
        return self

    def run(self):
        # # print('in step run')
        if self.parent.parent.driver:
            self.driver = self.parent.parent.driver
        else:
            return 1

        index = 0
        while not self.pageReady():
            log('Page is loading...')
            # log(index)
            time.sleep(1)
            if index > 20:
                log('Page is loading more than 20s, break wating')
                break
            index += 1
            continue

        del index

        # while readytimes < 5:
        #     if index > 5:
        #         log('Page is loading more than 10s, break wating')
        #         break
        #     if self.pageReady():
        #         readytimes += 1
        #         log('Page is ready: ' + str(readytimes))
        #     else:
        #         index += 1
        #         log('Page is loading...')

        log('Page is ready...')

        # print(self.action)
        funcname = self.actionFunc[self.action]
        if self.action not in self.noElementlist:
            self.find_element()
        func = getattr(self, funcname)
        log(func.__name__ + ' is getted')
        return func()

    def sleep(self, s=None):
        if not s:
            s = 5
        if int(self.value):
            s = int(self.value)
        time.sleep(s)

    def screenshot_window1(self, arg1, arg2):
        """
        此函数是启用多线程函数, 是原来用来解决截取不到overlay的方案, 后因对象化而搁置
        :param arg1: 参数1
        :param arg2: 参数2
        :return: 启用线程
        """
        thed = threading.Thread(target=self.screenshot_window1, args=(arg1, arg2,))
        # thed.setDaemon(True)
        thed.start()
        time.sleep(2)
        # thed.join()
        # self.thred.append(thed)

    def pageReady(self):
        # 通过js来判断页面有没有加载完成
        status = self.driver.execute_script('return document.readyState')
        return status == 'complete'

    # Screen Shot
    def screenshot_window(self):
        # 以下注释内容为判断是否页面已经到达某个页面
        # 通过self.driver.title来判断是哪个页面
        # 如果确定使用此方法, 要确保截图方法的key为预期的页面名(或者创建其他属性来判断)

        # for i in range(5):
        #     if self.key == self.driver.title and self.pageReady():
        #         print(self.key, self.driver.title, ' is same')
        #         break
        #     else:
        #         print('sleep 5')
        #         time.sleep(5)
        filepath = self.parent.parent.outputpath
        screenname = self.value + '_' + str(self.parent.index)

        self.driver.get_screenshot_as_file(filepath + "/" + screenname + ".png")
        # pic = ImageGrab.grab()
        # pic.save(filepath + "/" + screenname + ".png")

        log('window is captured ' + filepath + "/" + screenname + ".png")
        return [filepath + "/" + screenname + ".png"]

    # 网页元素高亮
    def highlight_element(self):
        # 通过js来改变elemetn的显示格式, 可以更改此方法来修改想要highlight的样式
        # 在find element的时候会自动调用此方法
        self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", self.element,
                                   "border:2px solid red;")
        log(self.key + ' is highlight')

    def movetoelement(self):
        # 同上
        # 此方法暂时没有使用
        self.driver.execute_script("arguments[0].scrollIntoView();", self.element)
        log(self.key + ' is moved')

    def movecursor(self):
        # 移动鼠标至元素位置
        chains = ActionChains(self.driver)
        chains.move_to_element(self.element).perform()
        time.sleep(1)

    def clickblank(self):
        # 默认页面左上角为空白点
        # 点击页面左上角以完成点击空白处操作
        chains = ActionChains(self.driver)
        chains.move_by_offset(0, 0).click().perform()

    def back(self):
        # 模拟browser back的操作
        self.driver.back()
        log('screen is back to the previous page')

    # 网页全屏截图
    def screenshot_page(self):
        time.sleep(5)
        screenname = self.value + str(self.parent.index)
        driver = self.driver
        filepath = self.parent.parent.outputpath

        index = 0
        while not self.pageReady():
            log('Page is loading...')
            # log(index)
            time.sleep(1)
            if index > 20:
                log('Page is loading more than 20s, break wating')
                break
            index += 1
            continue

        del index

        page_height = driver.execute_script("return document.body.scrollHeight")  # 获取JS返回值为当前页面高度
        # down = True
        # while down:
        #     time.sleep(0.5)
        #     tempheight = driver.execute_script("return document.body.scrollHeight")
        #     if page_height == tempheight:
        #         down = False
        #     else:
        #         page_height = tempheight
        # del down
        log('PageHight is ' + str(page_height))

        # 滚动到页面顶部
        js = "var q=document.documentElement.scrollTop=0"
        self.js_execution(js)
        time.sleep(1)

        # 截取当前第一张页面并且存储到内存变量basemat
        png = driver.get_screenshot_as_png()
        img_buffer = io.BytesIO(png)
        img1 = Image.open(img_buffer)
        width, window_height = img1.size
        # window_height = height  # 将截取的第一屏幕高度赋给变量

        basemat = np.atleast_2d(img1)

        # 滚动截图
        scroll_number = page_height // window_height
        # log('ScrollNumber is ' + str(scroll_number))
        # log('window_height is '+ str(window_height))

        for i in range(1, scroll_number):
            scroll_height = window_height * i

            js = "var q=document.documentElement.scrollTop=" + str(scroll_height)
            self.js_execution(js)
            time.sleep(1)

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
            # right = page_width
            right = width
            upper = window_height - a
            lower = window_height

            rangle = (left, upper, right, lower)

            # 滚动最后一次并截取最后一屏
            # js = "var q=document.documentElement.scrollTop=" + str((window_height) * (scroll_number))
            js = "var q=document.documentElement.scrollTop=" + str(page_height)
            self.js_execution(js)
            time.sleep(2)

            # 截取尾部图片
            temppng = driver.get_screenshot_as_png()
            temp_ori = Image.open(io.BytesIO(temppng))
            temp_crop = temp_ori.crop(rangle)

            # 完成拼接
            mat = np.atleast_2d(temp_crop)
            basemat = np.append(basemat, mat, axis=0)

            # 输出最后拼接完成的图片
        #     Image.fromarray(basemat).save(filepath + "/" + screenname + ".png")
        # else:
        # 恰好整除的话不用截取尾部图片，直接输出图片
        Image.fromarray(basemat).save(filepath + "/" + screenname + ".png")

        log(screenname + ".png is captrued")
        return [filepath + "/" + screenname + ".png"]

    # Wait Element
    def waitelement(self):
        locatorMethod = {'xpath': By.XPATH, 'id': By.ID, 'name': By.NAME, 'css': By.CSS_SELECTOR,
                         'class': By.CLASS_NAME}
        # locator = (locatorMethod['xpath'], '//div[@id="_widget_wfx_"]')
        # if 'iframe' in self.key:
        locator = (locatorMethod[self.type], self.key)
        try:
            WebDriverWait(self.driver, 20, 0.5).until(EC.presence_of_element_located(locator))
            log(locator)
            log(self.key)
        except Exception as e:
            log(e)

    # Key Board Action
    def keyboard(self):
        keyboardmethod = {'ENTER': Keys.ENTER, 'SHIFT': Keys.SHIFT, 'CONTROL': Keys.CONTROL, 'DELETE': Keys.DELETE,
                          'SelectAll': (Keys.CONTROL, 'a'), 'BACKSPACE': Keys.BACK_SPACE}
        self.element.send_keys(keyboardmethod[self.value])
        log(self.value + ' is clicked')

    # Check box
    # keys: 被操作checkbox的id
    # status： checkbox所需的勾选状态
    def checkbox_comm(self):
        js = "var el = document.getElementById('" + self.key + "');el.checked = " + self.value + ";"
        self.js_execution(js)

    def tableSelect(self):
        # 此方法比较特殊, 用于操作以table为标签实现的dropdown list的select操作
        # 原理为寻找页面所有td标签, 并for循环遍历出包含期望值的选项并选择
        # 当找不到时, 应当raise一个elementNotFound error(未验证, 若发生bug, 把else注释掉即可)
        td = self.driver.find_elements_by_xpath('//td[contains(@id,"text")]')
        for tr in td:
            if tr.text == self.value:
                tr.click()
                break
        else:
            raise NoSuchElementException(self.value)
        log(self.value + ' is selected')

    # keys：滚动距离
    def scroll_comm(self):
        # 问题, self自己调用时, value不一定为期望的Value值
        # time.sleep(3)
        js = "var q=document.documentElement.scrollTop=" + self.value
        self.js_execution(js)
        time.sleep(0.5)

    # js: 需要被执行的js语句
    def js_execution(self, js):
        self.driver.execute_script(js)
        log(js + ' is executed')

    # option: 下拉菜单中的选项
    def dropdown(self):
        s1 = Select(self.element)
        s1.select_by_visible_text(self.value)
        log(self.value + ' is selected')

    # function: 定位元素的方式
    # keys：定位元素所需的值
    def find_element(self):
        if '$' in self.key:
            self.key = string.Template(self.key).safe_substitute({'value': self.value})

        func = getattr(self.driver, 'find_element_by_' + self.type)
        try:  # 修复log中没找到元素却会输出找到的log信息
            self.element = func(self.key)
            log(self.key + ' is find')
            self.highlight_element()
        except:
            log(self.key + ' is not find')
            raise
        return self.element

    # function: 定位元素的方式
    # keys：定位元素所需的值
    def find_elements(self, type, keys):
        func = getattr(self.driver, 'find_elements_by_' + type)
        e = None
        try:  # 修复log中没找到元素却会输出找到的log信息
            e = func(keys)
            self.highlight_element()
            # self.log(keys + ' element is found by ' + type + ' method.')
        except:
            pass
            # self.log(keys + ' element is not found by ' + type + ' method.')
        return e

    # Switch to iframe
    def switchtoframe(self):
        self.driver.switch_to.frame(self.element)
        time.sleep(2)
        log(self.key + ' iframe is switched')

    # Switch back
    def swithback(self):
        self.driver.switch_to.default_content()
        log('swithback to default window')

    # Common Input
    def input_comm(self):
        if self.value == "clear":
            self.element.clear()
        else:
            self.element.send_keys(self.value)
        time.sleep(1)
        log(self.value + ' is inputted')

    # Common Click
    def click_comm(self):
        self.element.click()
        log(self.key + ' is clicked')
        time.sleep(1)
        self.swithback()
        return self.element


class scenario:
    """
    # Class scenario, 来保存每一组操作的对象(xml中每一个scenario标签就会解析为一个scenario对象)
    # setcheckpoint 保存checkpoint到一个scenario对象中, 一个scenario只会有一个checkpoint
    # result = {'checkpoint': '', 'WindowsScreen': [], 'PageScreen': [], 'steps': ''}
    # result来保存所有report中需要的元素, 解析时会保存Checkpoint, 运行run时会保存相应的screenshot路径
    """

    # {Checkpoint: xxx, windowsScreen: [], pageScreen: []}
    def __init__(self, page, name):
        self.index = 0
        self.name = name
        self.page = page
        self.steps = []
        self.parent = None
        self.result = {'checkpoint': '', 'WindowsScreen': [], 'PageScreen': []}

    # append的时候会设置子元素的index和parent
    def append(self, object):
        object.parent = self
        object.index = len(self.steps) + 1
        return self.steps.append(object)

    def insert(self, ind, object):
        # 用于page方法的插入
        object.parent = self
        object.index = len(self.steps) + 1
        self.steps.insert(ind, object)
        return self.steps

    def _setcheckpoint(self, checkpoint):
        """
        设置checkpoint
        :param checkpoint: Str
        :return: None
        """
        self.result['checkpoint'] = checkpoint

    def _setSteps(self, list):
        """
        设置description和result
        :param list:
        :return:
        """
        temp = self.result.get('steps', [])
        temp.append(list)
        self.result['steps'] = temp
        return self.result['steps']

    def run(self):
        # 在run方法内部来判断screenshot应该存放的位置
        # http://192.168.1.42:8001/
        # 如果是本地运行的话则不会上传到server端, 并使最终report的link为正确的
        for step in self.steps:
            result = step.run()
            dic = None

            if step.action == 'screenshot':
                dic = 'WindowsScreen'

            if step.action == 'pagescreen':
                dic = 'PageScreen'

            if dic:
                # 在report方法中, 会根据 '|' 字符来切割字符串, [0]会作为路径, [1]会作为显示的名字
                # 故此方法在替换字符串的时候会有 '|' 字符
                severPath = 'http://{IP}:8001/{path}|{oldName}'
                if not self.parent.online:
                    self.result[dic].append('{p}|{r}'.format(r=result[0], p=result[0].split('/')[-1]))
                else:
                    tempPath = client.postPic(self.parent.T_Cid, result[0])
                    if tempPath:
                        self.result[dic].append(
                            severPath.format(path=tempPath, oldName=result[0], IP=client.getServerIP()))

        return self.result


class script:
    """
    # Class scenario, 来保存每一组操作的对象(xml中每一个scenario标签就会解析为一个scenario对象)
    # setcheckpoint 保存checkpoint到一个scenario对象中, 一个scenario只会有一个checkpoint
    # result = {'checkpoint': '', 'WindowsScreen': [], 'PageScreen': [], 'steps': ''}
    # result来保存所有report中需要的元素, 解析时会保存Checkpoint, 运行run时会保存相应的screenshot路径
    """

    def report(self):
        """
        遍历Scenario中的result来获取结果并最终输出到report中
        :return: Null
        """
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
        num = 1
        for scenario in self.scenarios:
            startrow = row
            page = scenario.page
            scenarioname = scenario.name

            worksheet.write(row, 0, num, bold)  # A2
            worksheet.write(row, 1, page, bold)
            worksheet.write(row, 2, scenarioname, bold)
            worksheet.write(row, 5, scenario.result['checkpoint'], bold)
            if not scenario.result.get('steps', None):
                print('./' + page + '/' + scenarioname + '/script: is not find in ScenarioStorage file')
                scenario.result['steps'] = ['defaultStep', 'defaultResult']
            for descript in scenario.result['steps']:
                worksheet.write(row, 3, descript[0], textWrap)
                worksheet.write(row, 4, descript[1], textWrap)
                worksheet.write(row, 8, 'NoRun', bold)
                worksheet.data_validation('I' + row.__str__(), {'validate': 'list',
                                                                'source': ['Pass', 'Block', 'Failed', 'NoRun']})
                worksheet.write(row, 9, '', bold)

                if scenario.result['WindowsScreen']:
                    screenname = scenario.result['WindowsScreen'][0].split('|')
                    screen = screenname[1].split('/')[-1]
                    worksheet.write_url(row, 6, screenname[0], string=screen)
                    del scenario.result['WindowsScreen'][0]
                else:
                    worksheet.write_blank(row, 6, '', bold)
                if scenario.result['PageScreen']:
                    pagesceenname = scenario.result['PageScreen'][0].split('|')
                    pagepath = pagesceenname[1].split('/')[-1]
                    worksheet.write_url(row, 7, pagesceenname[0], string=pagepath)
                    del scenario.result['PageScreen'][0]
                else:
                    worksheet.write_blank(row, 7, '', bold)
                row += 1
            if row != startrow + 1:
                worksheet.merge_range(startrow, 0, row - 1, 0, num, bold)
                worksheet.merge_range(startrow, 1, row - 1, 1, page, bold)
                worksheet.merge_range(startrow, 2, row - 1, 2, scenarioname, bold)
                bold.set_text_wrap()
                worksheet.merge_range(startrow, 5, row - 1, 5, scenario.result['checkpoint'], bold)
            num += 1
        workbook.close()
        log('Report is created')
        log(datetime.datetime.now() - self.begin)

    def __init__(self, casename):
        self.casename = casename
        self.url = ''
        self.outputpath = self.casename + "_" + time.strftime("%Y%m%d")
        self.scenarios = []
        self.result = {}
        self.T_Cid = 0  # TasktoCase ID
        self.status = True  # 执行是否完成的标记, 如果run过程中报错, 则会修改为False
        self.retry = False  # 判断reTry的次数, 是否需要reTry的判断在Method: Run中
        self.online = False  # 当在client端运行时会修改为True

    def ISonline(self):
        self.online = True
        return self.online

    def setuploger(self):
        """
        初始化Logger的设置
        将Handler保存到self对象用, 并在最终销毁对象时remove相应的handler
        防止log会记录多次log
        :return: None
        """
        loger = beanLogger
        loger.setLevel(logging.INFO)

        self.fn = logging.FileHandler(self.casename + '.log')
        self.fn.setLevel(logging.INFO)

        self.ch = logging.StreamHandler()
        self.ch.setLevel(logging.INFO)

        formatter = logging.Formatter('[%(asctime)s]-[%(module)s-%(funcName)s]:%(message)s')
        self.fn.setFormatter(formatter)
        self.ch.setFormatter(formatter)

        loger.addHandler(self.fn)
        loger.addHandler(self.ch)

    def append(self, object):
        object.parent = self
        object.index = len(self.scenarios) + 1
        return self.scenarios.append(object)

    def insert(self, ind, object):
        self.scenarios.insert(ind, object)

    def end(self):
        """
        结束时运行的方法, 把Log, report放入到相应文件夹中.
        :return:
        """
        filenames = self.casename.split('/')
        filename = filenames[-1:][0]
        if os.path.exists(self.outputpath + '/' + filename + '.xlsx'):
            os.remove(self.outputpath + '/' + filename + '.xlsx')
        if os.path.exists(self.outputpath + '/' + filename + '.log'):
            os.remove(self.outputpath + '/' + filename + '.log')
        beanLogger.removeHandler(self.fn)
        beanLogger.removeHandler(self.ch)
        logging.shutdown()
        if os.path.exists(self.casename + '.xlsx'):
            shutil.move(self.casename + '.xlsx', self.outputpath)
        if os.path.exists(self.casename + '.log'):
            shutil.move(self.casename + '.log', self.outputpath)
        print('The related log&Report is moved to output folder')
        self.driver.close()

    def run(self):
        self.setuploger()
        log(self.casename + ' is running')
        if not os.path.exists(self.outputpath):
            os.mkdir(self.outputpath)
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.driver.get(self.url)
        log(self.url + ' is Opened')
        self.begin = datetime.datetime.now()
        try:
            for scenario in self.scenarios:
                scenario.run()

        except TimeoutException as te:
            log('TimeoutException occures')
            log(te)
            self.retry = True
            self.status = False

        except NoSuchElementException as ne:
            log('NoSuchElementException occures')
            log(ne)
            self.retry = True
            self.status = False

        except Exception as e:
            log('error is occures')
            log(e)
            self.status = False
            # raise
        self.report()
        self.end()


def xmlTobean(XMLpath, inipath):
    """
    :param XMLpath: xml路径或xml对象
    :param inipath: ini文件的路径
    :return: 自动把xml完全解析为一个script对象并返回
    """
    if isinstance(XMLpath, ET.Element):
        root = XMLpath
        ET.ElementTree(root).write(root.attrib['name'] + '.xml')
    else:
        try:
            root = ET.parse(XMLpath).getroot()
        except Exception:
            raise FileNotFoundError

    elementResource = configparser.ConfigParser()
    elementResource.read(inipath)

    testScript = script(root.attrib['name'])
    print(testScript.casename, ' is created')
    if not root.find('website'):  # website
        testScript.url = root.find('website').text
    else:
        testScript.url = 'https://live.itg3.hp2b.hp.com'

    testScript.T_Cid = int(root.get('tasktocase', 0))

    pagename = ''
    for Scenario in root.findall('Scenario'):
        scenarioTem = scenario(Scenario.attrib['name'], Scenario.attrib['Scenario'])

        testScript.append(scenarioTem)
        for Step in Scenario:
            if Step.tag == 'CheckPoint':
                scenarioTem._setcheckpoint(Step.attrib['value'])
                continue
            stepTem = step()
            if 'action' in Step.attrib:
                stepTem.action = Step.attrib['action']
            if 'special' in Step.attrib:
                stepTem.action = Step.attrib['special']
            if 'type' in Step.attrib:
                stepTem.type = Step.attrib['type']
            if 'keys' in Step.attrib:
                if 'type' not in Step.attrib:
                    stepTem.key = Step.attrib['keys']
                else:
                    str = Step.attrib['keys'] + Step.attrib['type']
                    stepTem.key = elementResource[Scenario.attrib['name']][str]
            if 'value' in Step.attrib:
                stepTem.value = Step.attrib['value']
            if 'description' in Step.attrib and 'expectResult' in Step.attrib:
                scenarioTem._setSteps([Step.attrib['description'], Step.attrib['expectResult']])
            scenarioTem.append(stepTem)
            if pagename not in (scenarioTem.page, 'BrowserAction') and 'Overlay' not in scenarioTem.page:
                pagename = scenarioTem.page
                pageobj = step().setpageobj(pagename)
                scenarioTem.insert(0, pageobj)
    return testScript


# 在logger setup好之后, 就使用此方法来保存log信息
def log(message):
    beanLogger.info(message)


if __name__ == '__main__':
    testscrript = xmlTobean(r'CaseXmls/R1_Place+Order_Confirmation+Mini+Cart.xml',
                            r'XMLs/ElementResult.ini')
    # for t in testscrript.scenarios:
    #     print(t.name)
    #     for s in t.steps:
    #         print('  ',s.action)

    testscrript.run()
