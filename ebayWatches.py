import requests
from bs4 import BeautifulSoup
import unicodedata
from StoreToDB import *
import csv
import time

#url http://www.ebay.com/sch/Wristwatches/31387/i.html?_udlo=1000&_fsrp=1&Gender=Men%2527s&LH_BIN=1&_pgn=1&_skc=0

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
class Scraper(object):
    def __init__(self):
        self.baseURL = "http://www.ebay.com/sch/Wristwatches/31387/i.html?_udlo=1000&_fsrp=1&Gender=Men%2527s&LH_BIN=1&_pgn="
        self.pageIndex = 1         ##starting page
        self.itemsShowing = 0      ##number items per page
        self.db = dataBase()
        ##item data containers
        ##using csv temporarily, I'll move to push the data to the mySQL server later on
        with open('results.csv', 'w') as csvfile:
            self.writer = csv.writer(csvfile)
            self.writer.writerow(["item_name", "brand", "price", "seller_score", "savings", "has_units_sold", "units_sold", "watching"])


    def scrape(self):
        #number of items
        ##currently set low for debugging
        n_items = 2800                                    ##we want x entries
        while(self.itemsShowing < n_items):             ##while less than n_entries
            url = self.baseURL + str(self.pageIndex) + "&_skc=" + str(self.itemsShowing)  ##increment itemsshowing by x
            req = requests.get(url)
            soup = BeautifulSoup(req.content, "lxml")
            print "executed request"
            ##
            try:
                self.itemURL = [a for a in soup.find_all("h3", {"class":"lvtitle"})]
                for a in self.itemURL:
                    ##get the data from the contents of each item url
                    self.InnerURL = a.find('a')['href']
                    ##call the fcuntion/method that handles all of the internal data of each item
                    self.itemData()
                    self.items = [d for d in zip(self.itemName, self.brand, self.price, self.sellerScore, self.savings, self.hasUnitsSold, self.unitsSold, self.watching)]
                    with open('results.csv', 'a') as d:
                        self.writer = csv.writer(d)
                        try:
                            for e in self.items:
                                self.writer.writerow(e)
                        except:
                            pass
            except:
                pass
            self.pageIndex += 1
            self.itemsShowing += 20
        print "done"

    def itemData(self):
        time.sleep(1.5)
        try:
            ItemRequest = requests.get(self.InnerURL)
            soup = BeautifulSoup(ItemRequest.content, "lxml")
            self.itemName = [unicodedata.normalize('NFKD', a.contents[1]).encode('ASCII', 'ignore') for a in soup.find_all("h1", {"id": "itemTitle"})]
            self.itemName = [e.replace(",", "").replace(".", "").replace("-", "").replace("/", "").replace("\\", "").replace("_", "").replace("'", "") for e in self.itemName]
            self.price = [unicodedata.normalize('NFKD', a.span.contents[0].strip('US $')).encode('ASCII', 'ignore') for a in soup.find_all("div", {"id": "vi-mskumap-none"})]
            self.price = [e.replace(',', "") for e in self.price]
            self.price = map(float, self.price)
            self.brand = [unicodedata.normalize('NFKD', a.span.contents[0]).encode('ASCII', 'ignore') for a in soup.find_all("h2", {"itemprop": "brand"})]
            self.sellerScore = [unicodedata.normalize('NFKD', a.contents[1].contents[0]).encode('ASCII', 'ignore') for a in soup.find_all("span", {"class": "mbg-l"})]
            del self.sellerScore[1:]
            self.unitsSold = [unicodedata.normalize('NFKD', a.contents[1].contents[0].strip(' sold')).encode('ASCII', 'ignore') for a in soup.find_all("span", {"class": "vi-qtyS"})]
            self.unitsSold = map(int, self.unitsSold)
            self.hasUnitsSold = []
            self.hasUnitsSold.append("TRUE")
            if not self.unitsSold:
                self.unitsSold.append(0)
                self.hasUnitsSold[0] = "FALSE"
            try:
                self.watching = [unicodedata.normalize('NFKD', a.contents[0]).encode('ASCII', 'ignore') for a in soup.find_all("span", {"class":"vi-buybox-watchcount"})]
                if not self.watching:
                    self.watching.append(0)
            except:
                self.watching.append(0)
            self.watching = map(int,self.watching)
            try:
                self.savings = [unicodedata.normalize('NFKD', a.contents[0].strip('\n \t')).encode('ASCII', 'ignore') for a in soup.find_all("span", {"id": "youSaveSTP"})]
                ## % savings format on the page: $ n  ( x% off)
                ## strip out everything except the % off, we can maybe look into finding the words inbetween ( and )
                for index, e in enumerate(self.savings):
                    startingIndex = e.index('(')+1
                    endingIndex = e.index(')')
                    x = e[startingIndex:endingIndex].strip('% off')
                    self.savings[0] = x
                if not self.savings:
                    self.savings.append(0)
            except:
                self.savings.append(0)
            self.savings = map(int, self.savings)
        except:
            pass

    def MoveToDB(self):
        self.db.ImportToDatabase()
if __name__ == "__main__":
    s = Scraper()
    s.scrape()
    s.MoveToDB()