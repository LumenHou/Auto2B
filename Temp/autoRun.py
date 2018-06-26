import configparser

__author__ = 'AutoMain'
# -*- coding: utf-8 -*-

from selenium import webdriver
import threading
import importlib
import Temp.Common as Common
import os


# 遍历字符串, 把为py结尾的文件动态导入进来, 并生成一个线程加入到线程组中. 最终把线程组返回
def threadsCases(cases, URL, elementmap):
    # print(elementmap)
    threads1 = []
    elementResource = configparser.ConfigParser().read(elementmap)
    for case in cases:
        if case[-2:] == 'py':
            case = case[:-3]
            moduleCase = importlib.import_module('Output.'+case)
            common = Common.Common(case, webdriver.Firefox())
            threads1.append(threading.Thread(target=moduleCase.main, args=(common,URL,elementResource,), name=case))
    #print('threadsCases is over')
    return threads1

def threadscontrol(list):
    if list.__len__() < 3:
        for t in list:
            t.setDaemon(True)
            t.start()
        for t in list:
            t.join()
    else:
        for t in list[:3]:
            t.setDaemon(True)
            t.start()
        for t in list:
            t.join()
        threadscontrol(list[4:])


if __name__ == '__main__':
    caseFile = os.listdir(r'Output')
    threads = threadsCases(caseFile, 'https://live.itg3.hp2b.hp.com', 'XMLs/ElementResult.ini')
    for t in threads:
        t.setDaemon(True)
        t.start()
    for t in threads:
        t.join()

    print('main_thread end!')