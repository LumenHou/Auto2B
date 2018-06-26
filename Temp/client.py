import json
from time import sleep
import os, socket
import requests
import xml.etree.cElementTree as ET

import Temp.bean as bean

__author__ = 'Lumen'
# -*- coding: utf-8 -*-


inipath = r"XMLs/ElementResult.ini"


def getxmlfile():
    """
    使用requests库模拟HTTP的get方法, 执行HTTP请求, 获取server端GETXml api的执行结果
    :return: <xml><result [状态标识]></><contain><Script[关键部分]> <...结束标签>
    <result resultcode = num /> 当num == 0 时, 代表获取成功并解析script部分并返回script对象
                                当num == 1 时, 代表获取失败, 直接返回错误信息
    """
    API = r'http://{IP}:8001/API.ashx?action=ApiGetXML'
    try:
        # 执行HTTP请求
        r = requests.get(API.format(IP=getServerIP()), stream=True)
    except Exception as e:
        print(e)
        return 'Get Failed'
    # 解析返回文本为element 对象<root>
    root = ET.fromstring(r.text)
    if r.status_code != requests.codes.ok:
        return 'URL get failed.'
    result = root.find('result')
    resultcode = result.get('resultcode', 1)
    if resultcode == '0':
        # 当状态码为0时, 正常解析script标签并返回script对象
        return bean.xmlTobean(root.find('contain/Script'), inipath)
    if resultcode == '1':
        # 当状态码为1时, 直接返回错误信息
        return result.text
    return 'Get Failed'


def putresult(filepath):
    url = r'http://192.168.1.42/'
    files = {'file': open(filepath, 'rb')}
    r = requests.post(url, files=files)
    print(r.status_code)


def postPic(Taskid, picFile):
    """
    上传图片的api, 该方法会在case运行期被调用, 每个scenario运行完后会上传保存的图片到server端且保存在result属性中
    :param Taskid:任务id
    :param picFile: 图片路径
    :return: 上传完成后server端的保存路径
    """
    API = 'http://{IP}:8001/API.ashx?action=ApiUploadPic'
    if os.path.exists(picFile):
        try:
            data = {'TasktoCase_ID': Taskid}
            files = {'FilePic': open(picFile, 'rb')}

            response = requests.post(API.format(IP=getServerIP()), data=data, files=files)
            resultDic = json.loads(response.text)

            savePath = resultDic.get('path', None)
        except:
            savePath = None
    else:
        raise IOError('File is not exists!')
    return savePath


def postReport(Taskid, reportFile, HostName, Status):
    """
    case执行完成后会上传相应的report到server端
    :param Taskid: 任务id
    :param reportFile: report文件路径
    :param HostName: 客户端hostname
    :param Status: case执行状态
    :return: 返回上传到server端的路径
    """
    API = 'http://{IP}:8001/API.ashx?action=ApiUploadReport'
    if os.path.exists(reportFile):
        files = {'FileReport': open(reportFile, 'rb')}
    else:
        files = ''
    try:
        data = {'TasktoCase_ID': Taskid,
                'HostName': HostName,
                'Status': Status
                }
        response = requests.post(API.format(IP=getServerIP()), data=data, files=files)
        resultDic = json.loads(response.text)
        savePath = resultDic.get('path', None)
    except:
        savePath = None
    return savePath


def postFile(filepath, fileName):
    if (os.path.exists(filepath)):
        try:
            data = {'fileName': fileName}
            files = {'file': open(filepath, 'rb')}

            response = requests.post('http://192.168.1.42/FileSave.ashx', data=data, files=files)
            html = response.text
            dict1 = json.loads(html)
            if (dict1["result"] == "-1"):
                print(dict1["msg"])
                return None
            else:
                print(dict1["path"])
        except:
            print("err")
            pass
    else:
        raise IOError("file is not exists!")


def main():
    """
    主函数, 获取server端xml并运行最后上传结果到server端
    当连续get fail times次后, 会结束运行
    :return: None
    """
    hostname = socket.gethostname()
    retrylist = {}
    times = 0
    while times < 10:
        try:
            result = getxmlfile()
        except Exception as e:
            result = str(e)
        if isinstance(result, str):
            print(result)
            if result == '缓存中无可执行数据':
                sleep(5)
            if result == '数据暂无可用,请稍后重试。':
                sleep(300)
            print('get xml again')
            times += 1
            continue
        outputfile = result.outputpath + '/' + result.casename + '.xlsx'
        try:
            # 设置result为在线运行, 在scenario对象用对判断此属性来判断是否需要上传图片到server端
            result.ISonline()
            result.run()
        except Exception as e:
            result.end()
            print('Error occures during test case running...', e)
            continue

        # 判断是否需要retry
        if result.retry:
            # 默认传递状态为1(让server端将case放置待执行区)
            # 并保存到retrylist里面
            status = 1
            trytimes = retrylist.get(result.casename, 0)
            if trytimes > 3:
                # 当重试的次数超过3次时 就传递状态为3(让server端标记case fail)
                status = 3
            retrylist[result.casename] = trytimes + 1
            print(result.casename, trytimes + 1)
        else:
            # 不需要retry就通过判断status来决定上传的status code
            status = 2 if result.status else 3
        serverpath = postReport(result.T_Cid, outputfile, hostname, status)
        print(result.casename, status, serverpath)
        times = 0


def getServerIP():
    # 链接vpn后 IP地址会变化, 导致无法使用以下方法获取正确的本地ip, 故注释掉

    # hostname = socket.gethostname()
    # IPAddress = socket.gethostbyname(socket.getfqdn(hostname))
    # print(IPAddress)
    # if '10.12.47' in IPAddress:
    #     return '10.12.47.187'
    #
    # if '192.168.1' in IPAddress:
    #     return '192.168.1.42'

    return '192.168.1.42'


if __name__ == '__main__':
    # hp
    main()
    # print(getServerIP())
    # print(getServerIP())
