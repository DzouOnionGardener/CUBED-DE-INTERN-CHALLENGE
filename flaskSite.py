from flask import Flask, render_template, request, url_for, redirect
from analyzer import *
from StoreToDB import *

username = raw_input("please enter your mysql username: ")
password = raw_input("please enter your mysql password: ")
app = Flask(__name__)
@app.route('/')
def index():
    ## home page, this program should only be executed after there is existing data in the SQL server,
    #  otherwise it will not work
    try:
        a = analyzer(username, password)
        correlation, ratio = a.ScoreCorrelations()
        abovePricePoint, belowPricePoint = a.WillingnessToPurchase()
        mostCommon = a.mostCommonBrand()[0]
        frequency = a.mostCommonBrand()[1]
    except:
        pass
    return render_template("home.html", Ratio = ratio, Correlation = correlation,
                           MostCommon = mostCommon, listed = frequency,
                           above = abovePricePoint, below = belowPricePoint)



@app.route('/login/', methods=['GET','POST'])
def login():
    #creates a path to the login page
    return render_template('login.html')

@app.route('/loginSQL/', methods=['POST'])
def getCred():
    #takes care of the form on the login that enables the creation and storage of data
    username = request.form['username']
    password = request.form['password']
    db = dataBase(username, password)
    db.createDatabase()
    db.ImportToDatabase()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)