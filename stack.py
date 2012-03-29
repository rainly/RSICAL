import csv
import urllib.request
import sys

__author__ = 'wbmark'



class Stock:
    def __init__(self):
        pass

    def getStockStr(self,value =''):
        return value[value.find('"')+1:value.find('";')]


    def writedata(self,value =[]):
        FIELDS = ['Name', 'Sex', 'E-mail', 'Blog']
        file = open("d:/stocks.csv", 'wb')
        writer = csv.DictWriter(file,fieldnames=FIELDS)
#        for item in value:
        writer.writerow(dict(zip(FIELDS, FIELDS)))

if __name__ == '__main__':
     url = "http://hq.sinajs.cn/list="
     wp = urllib.request.urlopen(url+'s_sh601006,s_sh600111')
     content = wp.read()
     valuestr = str(content,'gb2312')
     s = valuestr.split('\n')
     stock  = Stock()
#     for item in s:
     stock.writedata()
#     stock.writedata(stock.getStockStr(content))
#        print(stock.getStockStr(item))


