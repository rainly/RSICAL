import re
import urllib.request
from  html.parser import HTMLParser
__author__ = 'wbmark'

url="http://vip.stock.finance.sina.com.cn/q/go.php/vIR_RatingUp/index.phtml?p="
url2="http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/qgqp/index.phtml?t=sh_a&p="
url3="http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/qgqp/index.phtml?t=sz_a&p="
regex1 = r"...=stock"
regex2 = r"...q=..."
class MyParse(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            if len(attrs) == 0 :pass
            else:
                for(varaiable, value) in attrs:
                    if varaiable == 'href':
                        match = re.search(regex2,value)
                        if match :
                            code = self.getStockCode(value)
                            if self.links.count(code) == 0:
                                self.links.append(code)

    def getStockCode(self, value):
        index = value.index('q=')+2
        return value[index:index+8]

    def writeStocks(self,filename):
        file = open(filename,"w+")
        for line in self.links:
         file.write(line[2:]+'\n')
        file.close()

        
if __name__  == "__main__":
#    hp = MyParse()
#    for i in range(1,23):
#        response = urllib.request.urlopen(url2+str(i))
#        content =  response.read()
#        hp.feed(str(content,'gb2312'))
#    hp.writeStocks("d:/stocks/shstocks.txt")
    
    hp2 = MyParse()
    for i in range(1,36):
        response = urllib.request.urlopen(url3+str(i))
        content =  response.read()
        hp2.feed(str(content,'gb2312'))
    hp2.writeStocks("d:/stocks/szstocks.txt")
