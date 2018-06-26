#coding=utf-8
__author__ = 'Lumen'

exPage = """
BrowserAction
LoginPage
GlobalHead
MyAccountPage
HomePage
UsersToApprovePage
QuoteListingPage
QuoteDetailsPage
SearchResultPage
ProductDetailsPage
CartConfirmationOverlay
CartPreviewOverlay
ShoppingCartPage
CheckoutPage
CategoryPage
Org_UsersPage
FavoriteListingPage
AddUserPage
SpecificationsTab
CustomerServicePage
BatchEditUsersPage
CreateNewFavoriteOverlay
FavoriteDetailPage
GenerateURLPage
RegistrationURLPage
UserApprovalDetailsPage
Order Listing Page
PaymentInformationPage
PRToApprovePage
PFPLoginPage
PFPHomePage
OrgCatalogAccessOverlay
"""

def bub(list): # 冒泡排序
    lenth = len(list)
    flage = True
    while flage:
        flage = False
        for item in range(lenth - 1):
            if list[item] > list[item + 1]:
                temp = list[item]
                list[item] = list[item + 1]
                list[item + 1] = temp
                flage = True
        lenth -= 1
        print(lenth)
    return list

def sel(list):
    lenth = len(list)
    # result = []
    index = 1
    for i in range(lenth - 1):
        min = list[i]
        # print(list[i])
        for item in list[i:]:
            j = 1
            if min > item:
                min = item
                del list[i+j]
            j += 1
        # print(index)
        list[index] = list[i]
        list[i] = min
    return list
if __name__ == '__main__':
    import xml.etree.cElementTree as ET
    root = ET.parse('../XMLs/ScenarioStorageV1.xml').getroot()
    for page in root:
        pagename = page.attrib['PageName']
        if pagename in exPage:
            continue
        print(page.attrib['PageName'])