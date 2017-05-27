import requests
from bs4 import BeautifulSoup
import MySQLdb
import unicodedata
import csv
"""
item url:      <div class="lvpicinner ... picW">  <a href=" (item_url) " >
item name:     <h3 class="lvtitle"> <a href=" "> (item_name) </a>             #nested inside an anchor
 |
price:         <span itemprop="price">(US $)</span>
seller score:  <span class="mbg-l">  <a href=""> (score) </a>
seller score:  <span class="vi-mbgds3-bkImg" title="feedback score: (score)">
watching:      <span class="vi-buybox-watchcount">(count)</span>
units sold?:   <span class="vi-qtyS">  <a href=""> # sold </a> </span>        ## try:check if contains the words "sold"
savings prcnt: <span id="youSaveSTP"> (##%&nbps;off) </span>
brand:         <span itempop="name"> (brand name) </span>
"""
#url http://www.ebay.com/sch/Wristwatches/31387/i.html?_udlo=1000&_fsrp=1&Gender=Men%2527s&LH_BIN=1&_pgn=1&_skc=0
class Scraper(object):
    def __init__(self):
        self.baseURL = "http://www.ebay.com/sch/Wristwatches/31387/i.html?_udlo=1000&_fsrp=1&Gender=Men%2527s&LH_BIN=1&_pgn="
        self.pageIndex = 1         ##starting page
        self.itemsShowing = 0      ##number items per page

        ##item data containers

        with open('results.csv', 'w') as csvfile:
            self.writer = csv.writer(csvfile)
            self.writer.writerow(["item_name", "brand", "price", "seller_score", "savings", "watching"])


    def scrape(self):
        #number of items
        n_items = 20                                    ##we want x entries
        while(self.itemsShowing < n_items):             ##while less than n_entries
            url = self.baseURL + str(self.pageIndex) + "&_skc=" + str(self.itemsShowing)  ##increment itemsshowing by x
            ##GET call on url
            req = requests.get(url)
            ##get contents
            soup = BeautifulSoup(req.content, "lxml")
            print "executed request"
            ##
            try:
                #self.itemName = [a.contents[0] for a in (hname.find('a') for hname in soup.find_all("h3", {"class":"lvtitle"})) if a]
                #print self.itemName
               # self.itemName = [unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore') for x in self.itemName]
                #print self.itemName
                self.itemURL = [a for a in soup.find_all("h3", {"class":"lvtitle"})]
                for a in self.itemURL:
                    self.InnerURL = a.find('a')['href']
                    self.itemData()
                    self.items = [d for d in zip(self.itemName, self.brand, self.price, self.sellerScore, self.savings,self.watching)]
                    with open('results.csv', 'a') as d:
                        self.writer = csv.writer(d)
                        try:
                            for e in self.items:
                                self.writer.writerow(e)
                        except:
                            pass
            except:
                pass
            self.itemsShowing += 20
        print "done"

    def itemData(self):
        try:
            ItemRequest = requests.get(self.InnerURL)
            soup = BeautifulSoup(ItemRequest.content, "lxml")
            self.itemName = [unicodedata.normalize('NFKD', a.contents[1]).encode('ASCII', 'ignore') for a in soup.find_all("h1", {"id": "itemTitle"})]
            self.price = [unicodedata.normalize('NFKD', a.span.contents[0].strip('US $')).encode('ASCII', 'ignore') for a in soup.find_all("div", {"id": "vi-mskumap-none"})]
            self.brand = [unicodedata.normalize('NFKD', a.span.contents[0]).encode('ASCII', 'ignore') for a in soup.find_all("h2", {"itemprop": "brand"})]
            self.sellerScore = [unicodedata.normalize('NFKD', a.contents[1].contents[0]).encode('ASCII', 'ignore') for a in soup.find_all("span", {"class": "mbg-l"})]
            ##score needs to be fixed, sometimes the list shows 2 scores
            try:
                self.watching = [unicodedata.normalize('NFKD', a.contents[0]).encode('ASCII', 'ignore') for a in soup.find_all("span", {"class":"vi-buybox-watchcount"})]
                if not self.watching:
                    self.watching.append(0)
            except:
                self.watching.append(0)
            try:
                self.savings = [unicodedata.normalize('NFKD', a.contents[0].strip('\n \t')).encode('ASCII', 'ignore') for a in soup.find_all("span", {"id": "youSaveSTP"})]
                ## savings format on the page: $ n  ( x% off)
                ##strip out everything except the % off, we can maybe look into finding the words inbetween ( and )
                ##i can look for the index of ( and the index of )
                ##and then take the characters inbetween the indexes and then strip % off
                for index, e in enumerate(self.savings):
                    startingIndex = e.index('(')+1
                    endingIndex = e.index(')')
                    x = e[startingIndex:endingIndex].strip('% off')
                    self.savings[0] = x
                if not self.savings:
                    self.savings.append(0)
            except:
                self.savings.append(0)
        except:
            pass
        #self.sellerScore = map(int, self.sellerScore)
        #self.watching = map(int, self.watching)
if __name__ == "__main__":
    s = Scraper()
    s.scrape()
    ##results = map(int, results) ##converts list of strings to int