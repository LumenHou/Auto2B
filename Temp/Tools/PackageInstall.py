import os
packagelist = ['Pillow', 'XlsxWriter', 'numpy', 'selenium', 'xlrd', 'requests', 'json']

if __name__ == '__main__':
    pass
    for package in ['pip install ' + p for p in packagelist]:
        p = os.popen(package)
        print(package)
        print(p.read())