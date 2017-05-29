import MySQLdb
import csv
class dataBase(object):
    def __init__(self, username="root", password="lollmao1@"):
        self.db_username = username
        self.db_password = password
        self.createDatabase()
        self.datafile = csv.reader(file("results.csv"))
        #CREATE SCHEMA `eBay` DEFAULT CHARACTER SET latin1 COLLATE latin1_bin

    def createDatabase(self):
        createSchema = raw_input("create table? (Y/N)")
        if createSchema == 'Y' or createSchema == 'y':
            DB = MySQLdb.connect("localhost", self.db_username, self.db_password, "eBay")
            cursor = DB.cursor()
            #item_name,brand,price,seller_score,savings_percent,units_sold,watching
            cursor.execute("CREATE TABLE eBay.watches (`item_name` VARCHAR(255) NULL,`brand` VARCHAR(255) NULL,`price` FLOAT NULL,`seller_score` INT NULL,`savings_percent` INT(2) NULL,`has_units_sold` VARCHAR(8) NULL,`units_sold` INT NULL,`watching` INT NULL);")
            DB.commit()
            DB.close()
        else:
            pass

    def ImportToDatabase(self):
        DB = MySQLdb.connect("localhost", self.db_username, self.db_password, "eBay")
        cursor = DB.cursor()
        #query= "INSERT INTO eBay.watches(item_name, brand, price, seller_score, savings_percent, watching) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        try:
            for rows in self.datafile:
                try:
                    cursor.execute("INSERT INTO eBay.watches(item_name, brand, price, seller_score, savings_percent, has_units_sold, units_sold, watching) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)", rows)
                    DB.commit()
                except:
                    pass
        except:
            pass

if __name__ == "__main__":
    db = dataBase()
    db.ImportToDatabase()

