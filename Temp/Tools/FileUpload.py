#coding=utf-8
__author__ = 'changsong.li'

import urllib
import os
import json
import requests

def postFile(filepath,fileName):
    html=None
    if(os.path.exists(filepath)):
        try:
            data = {'fileName': fileName }
            files = {'file': open(filepath, 'rb')}

            response = requests.post('http://192.168.1.42/FileSave.ashx', data=data, files=files)
            html=response.text
            dict1 =json.loads(html) 
            if(dict1["result"] == "-1"):
                print (dict1["msg"])
                return None
            else:
                print (dict1["path"])
        except:
            print ("err")
            pass
    else:
        raise IOError("file is not exists!")

if __name__ == '__main__':
    postFile("D.txt","Web1111.config")
    pass
