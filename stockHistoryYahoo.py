from html.parser import HTMLParser
from math import fabs
import string
import urllib.request
import time

__author__ = 'wbmark'


base_url = "http://finance.cn.yahoo.com/mark/history.php?code=sh600000&type=history"
sina_hist_url="http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/"
nday = 5
class StockHist(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.selected = ("tr","td","div","a")
        self.tags = []
        self.values = []
        self.datedivs = []
        self.line = 0
        self.cols = 0
        self.todayvalue = 0

    def reset(self):
        HTMLParser.reset(self)
        self.tags = []


    def handle_starttag(self, tag, attrs):
        if tag in self.selected  :
           if tag == "tr" :
               self.line += 1
               self.col = 0
               self.values = []
           elif tag == "td":
               self.col +=1
               if self.col == 4 and self.isValiate():
                   self.datedivs.append(self.values)
           self.tags.append(tag)

    def isValiate(self):
        if self.line > 2 and self.line <= 17:
            return True
        else:
            return False



    def handle_endtag(self, tag):
        if self.tags \
        and tag in self.selected \
        and tag == self.tags[-1]:
            self.tags.pop()

    def handle_data(self, data):
        if "/".join(self.selected) in (
             'table/tr/td/div/a') and self.isValiate() and data.strip() != '':
                self.values.append(data.strip())

    def calcRsi(self,row):
        days = stockhist.datedivs
        a = 0
        b = 0
        for i in range(0,row):
          d = float(days[i][3]) - float(days[i+1][3])
          if d > 0:
              a = a +d
          elif  d < 0:
              b = b + d
        return a/(a + fabs(b) ) * 100



if __name__ == "__main__":
    file = open("d:/stocks/szstocks.txt")
    i = 0
    for stock in file:
        if not i % 50:
            time.sleep(20)
            print("sleeping 20 s")
        stockhist = StockHist()
        content = ""
        try:
            content = urllib.request.urlopen(sina_hist_url +str(stock.strip())+".phtml").read()
        except :
            time.sleep(50)

        htmlstr = str(content,"gb2312")
        index = htmlstr.find('<table id="FundHoldSharesTable">')
        part2 = htmlstr[index:]
        index2 = part2.find("</table>")
        stockhist.feed(part2[:index2+8])
        if len(stockhist.datedivs) < 15 :continue
        rsi6 = stockhist.calcRsi(6)
        rsi12 = stockhist.calcRsi(12)
        rsiv = rsi6 - rsi12
        if fabs(rsiv) < 1 and rsi6 < 40:
            print(stockhist.calcRsi(14))
            print("cross stock is  :", stock)
        stockhist.close()
        i +=1
    file.close()
