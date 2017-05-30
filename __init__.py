from ebayWatches import *

class main(object):
    def __init__(self):
        self.username = raw_input("what is your mysql username?: ")
        self.password = raw_input("what is your mysql password?: ")
        print("we're now going to scrape ebay! hang on this is going to take awhile")

        scraper = Scraper(self.username, self.password)
        scraper.scrape()


if __name__ == "__main__":
    run = main()