from __future__ import division
import MySQLdb
import pandas as pd
"""
create a correlation between high user scores and sales and or users watching
using this metric we can confidently conclude that user scores make a difference

we can also look at the savings and make a correlation between how many items were sold
and whether or not deep discounts equated to higher sales volumes
"""
class analyzer(object):
    def __init__(self, username="root", password="lollmao1@"):
        self.username = username
        self.password = password
        self.DB = MySQLdb.connect("localhost", self.username, self.password, "eBay")

    def ScoreCorrelations(self):
        ## extract a count of user scores higher where scores <= 2000
        ## count has_units_sold where scores <= 2000
        ## sum of units_sold where scores <= 2000
        data = pd.read_sql_query('SELECT eBay.watches.seller_score, eBay.watches.watching FROM eBay.watches WHERE eBay.watches.seller_score >= 2000', con=self.DB)
        self.score_to_watching = data['seller_score'].corr(data['watching'])
        #print self.score_to_watching

        soldData = pd.read_sql_query('SELECT count(eBay.watches.seller_score) as _count_, sum(eBay.watches.units_sold) as _total_ FROM eBay.watches WHERE eBay.watches.seller_score >= 2000 AND eBay.watches.has_units_sold = "TRUE"', con=self.DB)
        x1 = int(soldData['_count_'])
        y1 = int(soldData['_total_'])
        soldData = pd.read_sql_query('SELECT count(eBay.watches.seller_score) as _count_, sum(eBay.watches.units_sold) as _total_ FROM eBay.watches WHERE eBay.watches.seller_score <= 2000 AND eBay.watches.has_units_sold = "TRUE"', con=self.DB)
        x2 = int(soldData['_count_'])
        y2 = int(soldData['_total_'])
        self.Ratio = float(((x1*y2)/(y1*x2)))
        #print "There is a %.3f chance that a user with a score lower than 2000 will sell more than a user with a score higher than 2000" % self.Ratio
        return self.score_to_watching, self.Ratio


    def WillingnessToPurchase(self, pricePoint=3000):
        query1 = ('SELECT SUM(eBay.watches.units_sold) as sold, COUNT(eBay.watches.savings_percent) as savings FROM eBay.watches WHERE eBay.watches.has_units_sold = "TRUE" AND eBay.watches.price <= %s AND eBay.watches.savings_percent BETWEEN 0 AND 20' % pricePoint)
        query2 = ('SELECT SUM(eBay.watches.units_sold) as sold, COUNT(eBay.watches.savings_percent) as savings FROM eBay.watches WHERE eBay.watches.has_units_sold = "TRUE" AND eBay.watches.price <= %s AND eBay.watches.savings_percent BETWEEN 20 AND 40' % pricePoint)
        query3 = ('SELECT SUM(eBay.watches.units_sold) as sold, COUNT(eBay.watches.savings_percent) as savings FROM eBay.watches WHERE eBay.watches.has_units_sold = "TRUE" AND eBay.watches.price <= %s AND eBay.watches.savings_percent BETWEEN 40 AND 60' % pricePoint)
        Query1 = ('SELECT SUM(eBay.watches.units_sold) as sold, COUNT(eBay.watches.savings_percent) as savings FROM eBay.watches WHERE eBay.watches.has_units_sold = "TRUE" AND eBay.watches.price >= %s AND eBay.watches.savings_percent BETWEEN 0 AND 20' % pricePoint)
        Query2 = ('SELECT SUM(eBay.watches.units_sold) as sold, COUNT(eBay.watches.savings_percent) as savings FROM eBay.watches WHERE eBay.watches.has_units_sold = "TRUE" AND eBay.watches.price >= %s AND eBay.watches.savings_percent BETWEEN 20 AND 40' % pricePoint)
        Query3 = ('SELECT SUM(eBay.watches.units_sold) as sold, COUNT(eBay.watches.savings_percent) as savings FROM eBay.watches WHERE eBay.watches.has_units_sold = "TRUE" AND eBay.watches.price >= %s AND eBay.watches.savings_percent BETWEEN 40 AND 60' % pricePoint)
        # less than or equal to pricePoint
        q1 = pd.read_sql_query(query1, con=self.DB)
        self.r1 = q1['sold']/q1['savings']
        self.r1 = self.r1.values
        q2 = pd.read_sql_query(query2, con=self.DB)
        self.r2 = q2['sold'] / q2['savings']
        self.r2 = self.r2.values
        q3 = pd.read_sql_query(query3, con=self.DB)
        self.r3 = q3['sold'] / q3['savings']
        self.r3 = self.r3.values
        # greater than or equal to pricePoint
        Q1 = pd.read_sql_query(Query1, con=self.DB)
        self.R1 = Q1['sold'] / Q1['savings']
        self.R1 = self.R1.values
        Q2 = pd.read_sql_query(Query2, con=self.DB)
        self.R2 = Q2['sold'] / Q2['savings']
        self.R2 = self.R2.values
        Q3 = pd.read_sql_query(Query3, con=self.DB)
        self.R3 = Q3['sold'] / Q3['savings']
        self.R3 = self.R3.values
        #above and below price points
        self.belowPP = []
        self.abovePP = []
        self.belowPP.extend((self.r1[0], self.r2[0], self.r3[0]))
        self.abovePP.extend((self.R1[0], self.R2[0], self.R3[0]))
        return self.abovePP, self.belowPP

    def mostCommonBrand(self):
        query = ('SELECT eBay.watches.brand, count(eBay.watches.brand) as freq FROM eBay.watches GROUP BY eBay.watches.brand ORDER BY freq DESC')
        self.mostCommon = pd.read_sql_query(query, con=self.DB)
        x = self.mostCommon.iloc[0].values.tolist()
        return x

if __name__ == "__main__":
    k = analyzer()
    k.ScoreCorrelations()
    k.WillingnessToPurchase()
    k.mostCommonBrand()