import pymysql

__author__ = 'Lumen'
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import xlrd, json, string
import configparser
import pip

jsonstr = """{
    "sites": [
        {"name": "菜鸟教程", "url": "www.runoob.com"},
        {"name": "google", "url": "www.google.com"},
        {"name": "微博", "url": "www.weibo.com"}
    ]
}"""

inipath = r'\\192.168.1.42\09_Temp\Lumen\1\ElementResult.ini'

scenariolist = """BrowserAction CloseBrowser,PRListingPage SelectStartDate,PRListingPage SelectEndDate,PRListingPage ClickClearResultButton,PRListingPage SelectViewOptionMenu,PRToApprovePage SelectStartDate,PRToApprovePage SelectEndDate,PRToApprovePage ClickSearchButton,PRToApprovePage ClickSearchOptionsExpansion,PRToApprovePage ClickClearResultButton,PRToApprovePage SelectViewOptionMenu,GlobalHead SelectSearchTypeDropdown,PSPunchOutPage ClickVisitmystorebutton,FavoriteDetailPage UpdateFavoriteName,CustomerServicePage SelectEnableUserOption,CheckoutPage InputEmailNotificationComment"""


# test1()

def log(func):
    def wrapper(*args, **kwargs):
        print('call %s' % func.__name__)
        print('in log ', *args, **kwargs)
        return func(*args, **kwargs)

    # print('end of %s' % func.__name__)
    return wrapper


@log
def test(a):
    print(a)


"""
SELECT
	*
FROM
	casetoscen
WHERE
	casetoscen.CaseCode = (
		SELECT
			caseinfo. CODE
		FROM
			caseinfo
		WHERE
			caseinfo.Title = 'R1_Search for products_No Search Results'
	)
"""


def getNotpad(path):
    f = open(path)
    list = f.readlines()
    f.close()
    return list


def analyXML():
    path = r'../test.xml'
    root = ET.parse(path).getroot()

    script = root.find('result').text

    # script = root.find('contain/Script')

    print(script)


END = '$'


def make_trie(words):
    trie = {}

    for word in words:
        t = trie
        for c in word:
            if c not in t:
                t[c] = {}
            t = t[c]
        t[END] = {}
    return trie


def check_fuzzy(trie, word, path='', tol=1):
    if word == '':
        return [path] if END in trie else []
    else:
        p0 = []
        if word[0] in trie:
            p0 = check_fuzzy(trie[word[0]], word[1:], path + word[0], tol)
        p1 = []
        if tol > 0:
            for k in trie:
                if k != word[0]:
                    p1.extend(check_fuzzy(trie[k], word[1:], path + k, tol - 1))
        return p0 + p1


def spiralOrder(matrix):
    if len(matrix[0]) == 1:
        return matrix[0]

    if len(matrix[0]) == 2:
        return matrix[0].extend(matrix[1][::-1])

    result = []

    result1 = matrix[0]
    result2 = []
    result4 = []
    result3 = matrix[-1]

    del matrix[0]
    del matrix[-1]

    for items in matrix:
        result2.append(items[-1])
        result4.append(items[0])
        del [items[-1]]
        del [items[0]]

    result.extend(result1)
    result.extend(result2)
    result.extend(result3[::-1])
    result.extend(result4[::-1])
    result.extend(spiralOrder(matrix))

    return result


def twoSum(numbers, target):
    # result = []
    # rlist = []
    # for i, num in enumerate(numbers):
    #     if num > target:
    #         break
    #     result = target - num
    #     i += 1
    #     if result in numbers[i:]:
    #         return [numbers.index(num) + 1, numbers[i:].index(result) + i + 1]
    for i in range(target):
        result = target - i
        if result in numbers and i in numbers:
            return [numbers.index(i) + 1, numbers[i:].index(result) + i + 1]


def removeElement(nums, val):
    lens = 0
    for i in range(len(nums)):
        if nums[lens] == val:
            del nums[lens]
        else:
            lens += 1
    return lens


def selfDividingNumbers(left, right):
    result = []
    for i in range(left, right + 1):
        # print(i)
        if i < 10:
            result.append(i)
            continue

        list = str(i)
        DividingNumbers = True
        for j in list:
            # print(j)
            if int(j) == 0:
                print(i)
                DividingNumbers = False
                break
            if i % int(j) != 0:
                DividingNumbers = False
                break
        if DividingNumbers:
            result.append(i)
    return result

    pass


def checkNumber(num):
    list = 1
    result = []

    for i in range(2, int(num / 2) + 1):
        if num % i == 0:
            yushu = int(num / i)
            if yushu in result:
                print(yushu)
                break
            list += i
            list += yushu
            result.extend([yushu, i])
    if list == num:
        return True
    return False
    pass


def rotale(nums, k):
    if k == 0:
        print(nums)
        return
    l = len(nums)
    if k > l:
        k = k % l
    for i in range(l - k):
        nums.insert(l, nums[0])
        del nums[0]
    return nums
    pass


def rotale2(matrix):
    result = []
    for m in matrix:
        result.extend([])

    pass


def remove(nums):
    if not nums:
        return 0
    temp = nums[0]
    index = 1
    for i in range(len(nums) - 1):
        if temp == nums[index]:
            del nums[index]
        else:
            temp = nums[index]
            index += 1
    # print(nums)
    print(nums)
    return len(nums)


def containsDuplicate(nums):
    temp = {}
    for num in nums:
        # if num in temp:
        if 1 == temp.get(num, 0):
            return True
        else:
            temp[num] = 1
    return False


def plusone(digits):
    result = [d+1 for d in digits]
    resutl2 = []

    for r in result:
        print(r)
    pass

if __name__ == '__main__':
    # rotale([1,2,3,4,5,6,7], 3)
    # a = range(10)
    # print(list(a))

    # nums = [
    #     [11, 12, 13, 14],
    #     [21, 22, 23, 24],
    #     [31, 32, 33, 34],
    #     [41, 42, 43, 44]
    # ]
    # b = [
    #     [41, 31, 21, 11],
    #     [42, 32, 22, 12],
    #     [43, 33, 23, 13],
    #     [44, 34, 24, 14]
    # ]
    #
    # # [[] for a,b,c,d in nums]
    # # print([[e, d, c, b] for b, c, d, e in a])
    # a = -1230
    # a = list(str(a))
    # print(a[::-1])
    pass
