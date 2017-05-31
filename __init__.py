from ebayWatches import *
from StoreToDB import *
class main(object):
    def __init__(self):
        self.username = raw_input("what is your mysql username?: ")
        self.password = raw_input("what is your mysql password?: ")
        scraper = Scraper(self.username, self.password)
        scrapeEbay = raw_input("to scrape ebay and then import to mySQL press 1. To import csv directly to mysql press 2.")
        if scrapeEbay == '1':
            print("warning: this will take a while!")
            print("alternatively, you can just just run StoreToDB.py individually if you dont want to go through the scraping process")
            scraper.scrape()

        if scrapeEbay == '2':
            print("beginning import, make sure you have the csv in the same directory as this program")
            csvImporter = dataBase(self.username, self.password)
            csvImporter.createDatabase()
            csvImporter.ImportToDatabase()

        if scrapeEbay != '1' and scrapeEbay != '2':
            exit("invalid selection, exiting")

        print("you can now run flaskSite.py")

if __name__ == "__main__":
    run = main()